from abc import ABC, abstractmethod
import random
from questionary import select

class Weapon:
    def __init__(self, name, damage):
        self.name = name
        self.damage = damage
    
    def __str__(self):
        return f"{self.name} (DMG: {self.damage})"

class Consumable(ABC):
    def __init__(self, name, value):
        self.name = name
        self.value = value
    
    def __str__(self):
        return f"{self.name} (Value: {self.value})"
    
    @abstractmethod
    def use(self, character):
        pass

class HealPotion(Consumable):
    def use(self, character):
        character.heal(self.value)

class Character(ABC):
    def __init__(self, name, type, pv=100, damage=10, exp=0):
        self._pv = pv
        self._max_pv = pv
        self.name = name
        self.damage = damage
        self.type =  type
        self.inventory = []
        self.exp = exp
        self.upgrades = {"pv":0, "damage":0}
        self.speed = random.randint(1, 20)  # Vitesse aléatoire pour déterminer l'ordre des tours
        self.observers = []
    
    @property
    def max_pv(self):
        return (self._max_pv + self.upgrades["pv"]) 
    
    @max_pv.setter
    def max_pv(self, value):
        increase = value - self.max_pv
        if increase > 0:
            self.upgrades["pv"] += increase
            self._pv += increase  # Heal the hero by the increase amount
            self.notify_observers("increase_hp", increase)
        else:
            print("Max HP cannot be decreased!")

    @staticmethod
    def randomize(damage):
        return random.randint(int(damage * 0.9), int(damage * 1.1))
    
    def get_health_bar(self, bar_length=20):
        """Generate a visual health bar based on current PV/max PV ratio"""
        ratio = self._pv / self.max_pv if self.max_pv > 0 else 0
        filled_length = int(bar_length * ratio)
        empty_length = bar_length - filled_length
        
        # Choose color based on health percentage
        if ratio > 0.6:
            bar_char = '█'  # Full health - green
        elif ratio > 0.3:
            bar_char = '▓'  # Medium health - yellow/orange
        else:
            bar_char = '░'  # Low health - red
        
        bar = bar_char * filled_length + '░' * empty_length
        return f"{bar}"
    
    def take_damage(self, damage):
        self._pv -= damage
        if self._pv < 0:
            self._pv = 0
            self.notify_observers("death", None)
        self.notify_observers("damage_taken", damage)

    def get_xp_level(self):
        # Level calculation based on exponential growth, level 1 at 0 EXP, level 2 at 20 EXP, level 3 at 50 EXP, etc.
        level = 1
        exp_thresholds = [20, 50, 100, 200, 500, 1000, 2000, 5000, 10000]
        for threshold in exp_thresholds:
            if self.exp >= threshold:
                level += 1
            else:
                break
        return level

    def drop_xp_deafeated(self, xp):
        before_level = self.get_xp_level()
        gained_exp = 20
        self.exp += gained_exp
        self.notify_observers("xp_gained", gained_exp)
        if self.get_xp_level() > before_level:
            self.level_up()
    
    def attack(self, target, weapon=None):
        if weapon:
            damage = self.randomize(weapon.damage + self.damage)
            self.notify_observers("attack", {"target": target, "weapon": weapon})
        else:
            damage = self.randomize(self.damage)
            self.notify_observers("attack", {"target": target, "weapon": None})
        target.take_damage(damage)
        if target._pv <= 0:
            self.drop_xp_deafeated(target.exp)
            
    def heal(self, amount):
        self._pv += amount
        if self._pv > self.max_pv:
            self._pv = self.max_pv
        self.notify_observers("heal", amount)
    
    def is_alive(self):
        return self._pv > 0

    @abstractmethod
    def perform_turn(self, targets):
        pass

    def add_observer(self, observer):
        if observer not in self.observers:
            self.observers.append(observer)
    
    def remove_observer(self, observer):
        if observer in self.observers:
            self.observers.remove(observer)
    
    def notify_observers(self, event_type, data):
        for observer in self.observers:
            observer.notify(self, event_type, data)

class Enemy(Character):
    def __init__(self, name, type, pv=100, damage=10, exp=0):
        super().__init__(name, type, pv, damage, exp)

    def perform_turn(self, targets):
        action = random.choice(["attack", "heal"])
        if action == "attack":
            weapon = random.choice([item for item in self.inventory if isinstance(item, Weapon)] + [None])
            target = random.choice(targets)
            self.attack(target, weapon)
        else:
            self.heal(15)

class Boss(Enemy):
    """Classe pour les boss de fin d'exploration"""
    def __init__(self, name, hero):
        exp = int(hero.exp * 1.1)
        pv = int(hero.max_pv * 1.2)
        damage = int(hero.damage * 1)
        super().__init__(name, "boss", pv, damage, exp)
        
        # Le boss a toujours une bonne arme
        boss_weapon = Weapon("Legendary Axe", damage + 15)
        self.inventory.append(boss_weapon)
        
        # Le boss est plus résistant
        self.upgrades["pv"] = int(pv * 0.3)
    
    def perform_turn(self, targets):
        """Le boss est plus agressif"""
        action = random.choices(["attack", "heal"], weights=[0.8, 0.2])[0]
        if action == "attack":
            weapon = random.choice([item for item in self.inventory if isinstance(item, Weapon)] + [None])
            target = random.choice(targets)
            self.attack(target, weapon)
            # Le boss a une chance de double attaque
            if random.random() > 0.7:
                self.notify_observers("boss_double_attack", target)
                self.attack(target, weapon)
        else:
            self.heal(25)

class Hero(Character):
    def __init__(self, name, type, pv=100, damage=10):
        super().__init__(name, type, pv, damage)

    def perform_turn(self, targets):
        possibilities = ["attack", "pass", "heal", "use item", "exit game"]
        weapons = [item for item in self.inventory if isinstance(item, Weapon)]
        choice = select(f"{self.name}'s turn! Choose an action:", choices=possibilities).ask()
        if choice == possibilities[0]:  # attack
            targetted_enemy = select("Choose a target:", choices=[f"{enemy.name} (HP: {enemy._pv}/{enemy.max_pv})" for enemy in targets]).ask()
            target = next(enemy for enemy in targets if enemy.name in targetted_enemy)
            if weapons:
                weapon_choices = [f"Hands (no weapon) (DMG: {self.damage})"] + [str(weapon) for weapon in weapons]
                weapon_choice = select("Choose a weapon:", choices=weapon_choices).ask()
                if weapon_choice == weapon_choices[0]:
                    self.attack(target)
                else:
                    weapon_index = weapon_choices.index(weapon_choice) - 1
                    self.attack(target, weapons[weapon_index])
            else:
                self.attack(target)
        elif choice == possibilities[1]:  # pass
            self.notify_observers("pass", None)
        elif choice == possibilities[2]:  # heal
            self.heal(20)
        elif choice == possibilities[3]:  # use item
            consumables = [item for item in self.inventory if isinstance(item, Consumable)]
            if not consumables:
                self.notify_observers("no_items", None)
                return self.perform_turn(targets)  # Go back to action selection
            else:
                consumable_choice = select("Choose an item to use:", choices=[str(item) for item in consumables]).ask()
                consumable = next(item for item in consumables if str(item) == consumable_choice)
                consumable.use(self)
                self.inventory.remove(consumable)
        elif choice == possibilities[4]:  # exit game
            self.notify_observers("exit_game", None)
            exit()
        else:
            self.notify_observers("invalid_choice", None)
    
    def level_up(self):
        self.notify_observers("level_up", self.get_xp_level())
        choice = select("Choose an upgrade:", choices=["Increase Max HP", "Increase Damage"]).ask()
        if choice == "Increase Max HP":
            self.max_pv += 20
            self._pv = self.max_pv  # Heal to full on level up
        else:
            self.damage += 5
            self.notify_observers("damage_increased", self.damage)

class Team:
    def __init__(self, name):
        self.name = name
        self.members = []
    
    def add_member(self, character):
        self.members.append(character)
    
    def remove_member(self, character):
        if character in self.members:
            self.members.remove(character)
    
    def is_defeated(self):
        return all(member._pv <= 0 for member in self.members)
    
    def get_alive_members(self):
        return [member for member in self.members if member._pv > 0]