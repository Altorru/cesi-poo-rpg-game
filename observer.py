from abc import ABC, abstractmethod

class Observer(ABC):
    @abstractmethod
    def notify(self, subject, event_type, data):
        """Mise à jour de l'observateur en fonction de l'événement"""
        pass

class GameObserver(Observer):
    @staticmethod
    def notify(subject, event_type, data):
        """Affiche les événements de combat et d'exploration"""
        if event_type == "increase_hp":
            print(
                f"❤️ Max HP increased by {data}! Current HP: {subject._pv}/{subject.max_pv}"
            )
        elif event_type == "damage_taken":
            print(
                f"💔 {subject.name} takes {data} damage! {subject.get_health_bar()} {subject._pv}/{subject.max_pv}"
            )
        elif event_type == "damage_increased":
            print(f"⚔️ Damage increased! Current Damage: {subject.damage}")
        elif event_type == "xp_gained":
            print(f"⭐ {subject.name} gains {data} EXP! Total EXP: {subject.exp}")
        elif event_type == "attack":
            print(
                f"\n{subject.name} attacks {data['target'].name} with {data['weapon'].name if data['weapon'] else 'no weapon'}!"
            )
        elif event_type == "death":
            print(f"💀 {subject.name} has been defeated!")
        elif event_type == "heal":
            print(
                f"\n{subject.name} heals for {data} HP! {subject.get_health_bar()} {subject._pv}/{subject.max_pv}"
            )
        elif event_type == "boss_double_attack":
            print(f"💥 {subject.name} performs a DOUBLE ATTACK!")
        elif event_type == "pass":
            print(f"\n{subject.name} decides to pass this turn.")
        elif event_type == "exit_game":
            print(f"\n{subject.name} has chosen to exit the game. Thanks for playing!")
        elif event_type == "invalid_choice":
            print("Invalid choice! Turn skipped.")
        elif event_type == "level_up":
            print(f"🎉 {subject.name} leveled up to Level {data}!")
        elif event_type == "battle_start":
            print(f"\n{'='*50}")
            print(f"⚔️  {data['battle_type']}! {data['starter'].name} goes first!")
            print(f"{'='*50}\n")
        elif event_type == "battle_end":
            print(f"\n{'='*50}")
            print(f"📊 BATTLE END - {subject.name}: {subject._pv}/{subject.max_pv} HP | {subject.exp} EXP")
            print(f"{'='*50}")
        elif event_type == "exploration_start":
            print(f"\n🎮 Starting exploration of the {data['zone_name']}!")
            print(f"   You will traverse {data['num_stages']} stages before facing the final boss.\n")
        elif event_type == "battle_stats":
            print(f"   Final stats: {subject.exp} EXP | {data['battles_won']} battles won")
            print(f"   Defeated at {data['stage_msg']}")
        elif event_type == "exploration_victory":
            print(f"\n🎉 VICTORY! You have conquered the {data['zone_name']}!")
        elif event_type == "start_classic_mode":
            print("\n🎮 Starting Classic Mode! Endless battles await...\n")
        elif event_type == "end_classic_mode":
            if data['win'] == True:
                print("\n🎉 Thanks for playing! Final stats:")
            else:
                print(f"\n💀 GAME OVER! {subject.name} has been defeated!")
            print(f"   Final stats: {subject.exp} EXP | {data['battles_won']} battles won")
