import random
from base import Weapon, Boss, Hero, Team
from questionary import text, confirm, select
from scores import save_score, display_top_scores
from exploration import ExplorationZone
from factories import HeroFactory, EnemyFactory

# Display top scores at start
display_top_scores()

hero_name = text("Enter your hero's name:").ask()
hero = HeroFactory().create_character(hero_name)
hero_team = Team("Hero Team")
hero_team.add_member(hero)

battles_won = 0

def play_game(hero_team, enemy_team, is_boss=False):
    """Gère un combat entre le héros et un ennemi"""
    characters = hero_team.members + enemy_team.members
    characters.sort(key=lambda c: c.speed, reverse=True)  # Tri par vitesse pour déterminer l'ordre des tours
    turn = 1
    # Emoji and color for starter
    starter = characters[0]
    starter_emoji = "🦸" if isinstance(starter, Hero) else "👹"
    # ANSI color codes
    color = "\033[92m" if isinstance(starter, Hero) else "\033[91m"
    reset = "\033[0m"
    print(f"\nStarter: {color}{starter_emoji} {starter.name} (Speed: {starter.speed}){reset}\n")
    
    battle_type = "BOSS BATTLE" if is_boss else "BATTLE START"

    hero.notify_observers("battle_start", {"battle_type": battle_type, "starter": characters[0]})
    
    while not hero_team.is_defeated() and not enemy_team.is_defeated():
        print(f"\n--- Turn {turn} ---")
        for character in characters:
            if character._pv <= 0:
                continue  # Skip if already defeated
            if isinstance(character, Hero):
                character.perform_turn(enemy_team.get_alive_members())
            else:
                character.perform_turn(hero_team.get_alive_members())
        turn += 1
    
    hero.notify_observers("battle_end", None)
    
    return not hero_team.is_defeated()  # Return True if hero won

# Choix du mode de jeu
mode_choices = ["🗺️  Exploration Mode", "⚔️  Classic Mode (Endless Battles)"]
mode = select("Choose game mode:", choices=mode_choices).ask()

if mode == mode_choices[0]:  # Exploration Mode
    zone_names = ["Cursed Forest", "Dragon's Lair", "Undead Catacombs", "Frozen Peaks", "Shadow Realm"]
    zone_name = random.choice(zone_names)
    num_stages = 10
    
    hero.notify_observers("exploration_start", {"zone_name": zone_name, "num_stages": num_stages})

    exploration = ExplorationZone(zone_name, hero, num_stages)
    
    # Boucle d'exploration
    while not exploration.is_complete():
        # Restaurer les PV du héros entre les stages (mais pas complètement)
        heal_amount = min(hero.max_pv - hero._pv, hero.max_pv // 3)
        if heal_amount > 0:
            hero._pv += heal_amount
            hero.notify_observers("heal", heal_amount)
        
        result = exploration.explore_stage()
        
        # Si l'événement est un combat avec un ennemi
        if isinstance(result, tuple) and len(result) > 1 and result[1] is not None:
            enemy = result[1]
            is_boss = isinstance(enemy, Boss)
            
            enemy_team = Team("Enemy Team")
            enemy_team.add_member(enemy)
            
            # Si c'est un boss, ajouter deux ennemis faibles à l'équipe
            if is_boss:
                weak_enemy_1 = EnemyFactory().create_enemy(hero)
                weak_enemy_2 = EnemyFactory().create_enemy(hero)
                enemy_team.add_member(weak_enemy_1)
                enemy_team.add_member(weak_enemy_2)
            
            hero_won = play_game(hero_team=hero_team, enemy_team=enemy_team, is_boss=is_boss)
            
            if not hero_won:
                hero.notify_observers("death", hero)
                stage_msg = "the boss fight" if is_boss else f"stage {exploration.current_stage}/{exploration.num_stages}"
                hero.notify_observers("battle_stats", {"battles_won": battles_won, "stage_msg": stage_msg})
                save_score(hero.name, hero.exp, battles_won)
                break
            else:
                battles_won += 1
                if is_boss:
                    hero.notify_observers("victory", {"zone_name": zone_name})
                    save_score(hero.name, hero.exp, battles_won)
                    break
    
else:  # Classic Mode
    hero.notify_observers("start_classic_mode", None)    
    while True:
        # Reset hero PV for new battle
        hero._pv = hero.max_pv
        
        enemy = EnemyFactory().create_enemy(hero)
        
        if random.random() > 0.5:
            enemy.inventory.append(Weapon("Random Weapon", random.randint(20, 30)))
        
        enemy_team = Team("Enemy Team")
        enemy_team.add_member(enemy)
        
        hero_won = play_game(hero_team=hero_team, enemy_team=enemy_team)
        
        if hero_won:
            battles_won += 1
            if not confirm("Play again?").ask():
                hero.notify_observers("end_classic_mode", {"win": True, "battles_won": battles_won})
                save_score(hero.name, hero.exp, battles_won)
                break
        else:
            hero.notify_observers("end_classic_mode", {"win": False, "battles_won": battles_won})
            save_score(hero.name, hero.exp, battles_won)
            break