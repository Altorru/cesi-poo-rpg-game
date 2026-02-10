from base import Hero, Enemy, Boss, Weapon
import random
from observer import GameObserver

class HeroFactory:
    def create_character(self, name):
        starting_weapon = WeaponFactory().create_weapon("Iron Sword", 18)
        hero = Hero(name, "warrior", 80, 15)
        hero.inventory.append(starting_weapon)
        hero.add_observer(GameObserver())
        return hero

class WeaponFactory:
    def create_weapon(self, name, damage):
        return Weapon(name, damage)
    
class EnemyFactory:
    def create_enemy(self, hero):
        enemy_names = ["Bandit", "Wolf", "Spider", "Skeleton", "Goblin"]
        enemy_types = ["warrior", "beast", "undead", "monster"]
        
        name = random.choice(enemy_names)
        enemy_type = random.choice(enemy_types)
        exp_multiplier = random.uniform(0.7, 1.0)
        enemy_exp = int(hero.exp * exp_multiplier)
        
        pv = 80 + (enemy_exp // 15)
        damage = random.randint(12, 18)
        
        enemy = Enemy(name, enemy_type, pv, damage, enemy_exp)
        enemy.add_observer(GameObserver())
        
        if random.random() > 0.6:
            enemy.inventory.append(WeaponFactory().create_weapon("Rusty Sword", random.randint(15, 20)))
        
        print(f"\n{'='*50}")
        print(f"👹 A wild {name} ({enemy_type}) appears!")
        print(f"   HP: {pv} | DMG: {damage} | EXP: {enemy_exp} | Speed: {enemy.speed}")
        print(f"{'='*50}")
        
        return enemy

class BossFactory:
    def create_boss(self, hero):
        boss_names = ["Demon Lord", "Ancient Dragon", "Lich King", "Dark Sorcerer", "Giant Troll"]
        boss_name = random.choice(boss_names)   
        boss = Boss(boss_name, hero)
        boss.add_observer(GameObserver())
        return boss