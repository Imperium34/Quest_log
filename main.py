from questmaster import QuestMaster
import subprocess

def clear_screen():
    subprocess.run('clear')

def print_hud(player):
    print("=" * 40)
    print(f"  HERO: {player.name}  |  LVL: {player.lvl}")
    print(f"  XP:   {player.xp}/{player.get_xp_until_next()}  |  GOLD: {player.gold}")
    print("=" * 40)

def main():
    name = input("Enter your Hero's name: ")
    game = QuestMaster(name)
    game.load()
    
    while True:
        clear_screen()
        print_hud(game.player)
        
        print("\n--- QUEST BOARD ---")
        if not game.quests:
            print("  (No active quests. Go find some work!)")
        else:
            for i, q in enumerate(game.quests, 1):
                status = "[x]" if q.completed else "[ ]"
                print(f"  {i}. {status} {q.name} ({q.type}) - {q.diff} pts")

        print("\n--- ACTIONS ---")
        print("[n] New Quest")
        print("[c] Complete Quest")
        print("[r] Remove Quest")
        print("[s] Save & Quit")
        
        choice = input("\n>> ").lower().strip()

        if choice == 'n':
            game.create_quest()

        elif choice == 'c':
            q_num = input("Quest # to complete: ")
            if q_num.isdigit():
                idx = int(q_num) - 1
                if 0 <= idx < len(game.quests):
                    quest = game.quests[idx]
                    if not quest.completed:
                        quest.complete(game.player)
                        input("\nQuest Complete! Press Enter...")
                    else:
                        input("\nAlready done! Press Enter...")
                else:
                    input("\nInvalid number. Press Enter...")

        elif choice == 'r':
            q_num = input("Quest # to remove: ")
            if q_num.isdigit():
                idx = int(q_num) - 1
                if 0 <= idx < len(game.quests):
                    game.delete_quest(idx)
                    input("\nQuest Removed! Press Enter...")
                else:
                    input("\nInvalid number. Press Enter...")

        elif choice == 's':
            game.dump()
            print("\nGame Saved. See you next time, Hero.")
            break

if __name__ == "__main__":
    main()