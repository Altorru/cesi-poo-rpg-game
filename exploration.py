import random
from questionary import select
from factories import EnemyFactory, WeaponFactory, BossFactory


class PathEvent:
    """Représente un événement aléatoire sur un chemin"""
    def __init__(self, event_type, value=None):
        self.event_type = event_type  # "combat", "exp", "weapon", "heal"
        self.value = value
    
    def execute(self, hero, event_callback=None):
        """Exécute l'événement et retourne (needs_combat, enemy) si un combat doit avoir lieu"""
        if self.event_type == "combat":
            print("\n⚔️  You encounter an enemy on this path!")
            enemy = EnemyFactory().create_enemy(hero)
            if event_callback:
                return event_callback("combat", enemy)
            return (True, enemy)
        
        elif self.event_type == "exp":
            exp_gain = self.value or random.randint(15, 30)
            before_level = hero.get_xp_level()
            hero.exp += exp_gain
            print(f"\n✨ You found a magical artifact! +{exp_gain} EXP! Total: {hero.exp}")
            if hero.get_xp_level() > before_level:
                hero.level_up()
        
        elif self.event_type == "weapon":
            if self.value:
                weapon = self.value
            else:
                # Générer une arme avec un nom aléatoire et des dégâts variés
                weapon_names = [
                    ("Magic Blade", 25, 35),
                    ("Flaming Sword", 28, 38),
                    ("Ice Staff", 22, 32),
                    ("Thunder Axe", 30, 40),
                    ("Shadow Dagger", 20, 30),
                    ("Holy Mace", 26, 36),
                    ("Poison Spear", 24, 34),
                    ("Crystal Bow", 27, 37)
                ]
                name, min_dmg, max_dmg = random.choice(weapon_names)
                weapon = WeaponFactory().create_weapon(name, random.randint(min_dmg, max_dmg))
            hero.inventory.append(weapon)
            print(f"\n🗡️  You found a {weapon.name}! ({weapon.damage} DMG)")
        
        elif self.event_type == "heal":
            heal_amount = self.value or random.randint(20, 40)
            hero.heal(heal_amount)
        
        return False


class Path:
    """Représente un chemin d'exploration"""
    def __init__(self, name, description, difficulty="normal"):
        self.name = name
        self.description = description
        self.difficulty = difficulty  # "easy", "normal", "hard"
        self.event = None
    
    def generate_event(self):
        """Génère un événement aléatoire basé sur la difficulté"""
        # Probabilités selon la difficulté
        if self.difficulty == "easy":
            weights = {"exp": 0.35, "heal": 0.25, "weapon": 0.25, "combat": 0.15}
        elif self.difficulty == "hard":
            weights = {"combat": 0.5, "weapon": 0.3, "exp": 0.2}
        else:  # normal
            weights = {"combat": 0.3, "weapon": 0.25, "exp": 0.25, "heal": 0.2}
        
        event_type = random.choices(
            list(weights.keys()),
            weights=list(weights.values())
        )[0]
        
        self.event = PathEvent(event_type)
        return self.event
    
    def __str__(self):
        difficulty_emoji = {
            "easy": "🟢",
            "normal": "🟡",
            "hard": "🔴"
        }
        return f"{difficulty_emoji.get(self.difficulty, '⚪')} {self.name} - {self.description}"


class ExplorationZone:
    """Représente une zone d'exploration complète"""
    def __init__(self, name, hero, num_stages=3):
        self.name = name
        self.hero = hero
        self.num_stages = num_stages
        self.current_stage = 0
        self.paths_history = []
    
    def generate_paths(self):
        """Génère 2-4 chemins aléatoires"""
        num_paths = random.randint(2, 4)
        
        path_templates = [
            ("Dark Forest", "A gloomy path through ancient trees", "normal"),
            ("Mountain Pass", "A treacherous climb up rocky slopes", "hard"),
            ("Riverside Trail", "A peaceful path along a flowing river", "easy"),
            ("Abandoned Mine", "A dark tunnel full of mysteries", "hard"),
            ("Meadow Path", "A sunny trail through open fields", "easy"),
            ("Ancient Ruins", "Crumbling stones of a forgotten civilization", "normal"),
            ("Cave System", "A network of dark underground passages", "hard"),
            ("Village Road", "A well-traveled path near settlements", "easy"),
        ]
        
        selected = random.sample(path_templates, min(num_paths, len(path_templates)))
        paths = [Path(name, desc, diff) for name, desc, diff in selected]
        
        return paths
    
    def explore_stage(self, combat_callback=None):
        """Explore un étage de la zone"""
        self.current_stage += 1
        
        # Si on a dépassé le nombre de stages, c'est le boss
        if self.current_stage > self.num_stages:
            return self._boss_fight(combat_callback)
        
        print(f"\n{'='*60}")
        print(f"🗺️  EXPLORATION - Stage {self.current_stage}/{self.num_stages}")
        print(f"   Zone: {self.name}")
        print(f"{'='*60}\n")
        
        paths = self.generate_paths()
        
        print("Available paths:\n")
        path_choices = [str(path) for path in paths]
        choice = select("Choose your path:", choices=path_choices).ask()
        
        chosen_path = paths[path_choices.index(choice)]
        self.paths_history.append(chosen_path.name)
        
        print(f"\n🚶 You take the {chosen_path.name}...")
        event = chosen_path.generate_event()
        
        # Exécute l'événement
        result = event.execute(self.hero, combat_callback)
        
        # Si c'est un combat, result est (True, enemy), sinon c'est False
        if isinstance(result, tuple):
            return result
        return (False, None)
    
    def _boss_fight(self, combat_callback=None):
        """Combat de boss final"""
        print(f"\n{'='*60}")
        print("👑 BOSS FIGHT!")
        print(f"{'='*60}\n")
        
        boss = BossFactory().create_boss(self.hero)
        
        print(f"💀 {boss.name} appears!")
        print(f"   HP: {boss.max_pv} | DMG: {boss.damage} | EXP: {boss.exp}")
        print("\n⚠️  This will be a legendary battle!\n")
        
        if combat_callback:
            return combat_callback("boss", boss)
        
        return True, boss
    
    def is_complete(self):
        """Vérifie si l'exploration est terminée"""
        return self.current_stage > self.num_stages
