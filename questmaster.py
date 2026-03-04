import json
from datetime import date
from player import Player
from quest import Quest
from data import DAILY_POOL
import random

class QuestMaster:
    def __init__(self, player_name):
        self.player = Player(player_name)
        self.quests = [] 

    def create_quest(self):
        name = input("Enter quest name: ").strip()
        while not name:
            print("Name cannot be empty.")
            name = input("Enter quest name: ").strip()
        
        desc = input(f"Enter a description for {name}: ")

        print(f"\nWhat type of quest is '{name}'?")
        print("1. Main Quest  (Big Projects)")
        print("2. Side Quest  (Chores/Errands)")
        print("3. Training    (Study/Skill Up)")
        print("4. Guild Work  (Social/Family)")
        print("5. Boss Battle (Deadlines/Exams)")
        print("6. Emergency   (Unexpected Fixes)")   

        type_map = {
            "1": "Main Quest",
            "2": "Side Quest",
            "3": "Training",
            "4": "Guild Work",
            "5": "Boss Battle",
            "6": "Emergency"
        }

        t_choice = input("Choose (1-6): ").strip()
        while t_choice not in type_map:
            print("Invalid choice. Please type a number between 1 and 6.")
            t_choice = input("Choose (1-6): ").strip()
        
        final_type = type_map[t_choice]
        time_limit = None

        if final_type == "Boss Battle":
            time_limit = input("When is the deadline? (YYYY-MM-DD): ").strip()
            desc = f"[DUE: {time_limit}] {desc}"

        print("\nHow difficult is it?")
        print("1. Easy | 2. Medium | 3. Hard | 4. Impossible")
        
        d_choice = input("Choose (1-4): ").strip()
        while not d_choice.isdigit() or not (1 <= int(d_choice) <= 4):
            print("Please enter a number between 1 and 4.")
            d_choice = input("Choose (1-4): ").strip()

        final_diff = int(d_choice)

        self.quests.append(Quest(name, desc, final_type, final_diff, time_limit))
        print(f"\n[+] Quest '{name}' added!")

    def delete_quest(self, i):
        self.quests.pop(i)

    def check_daily_reset(self):
        today = date.today().isoformat()
        
        if getattr(self.player, 'last_login', None) != today:
            print("\n[SYSTEM] A new day has dawned. Refreshing Daily Quests...")
            
            self.quests = [q for q in self.quests if not (q.type == "Daily Quest" and not q.completed)]
            
            self.generate_dynamic_quest() 
            self.player.last_login = today

    def generate_dynamic_quest(self):
        for _ in range(5):
            category = random.choice(list(DAILY_POOL.keys()))
            template, desc, diff_dict = random.choice(DAILY_POOL[category])
            
            chosen_diff = random.choice([1, 2, 3, 4])
            amount = diff_dict[chosen_diff]
            final_name = template.format(amount=amount)
            
            new_quest = Quest(final_name, desc, "Daily Quest", chosen_diff)
            self.quests.append(new_quest)

    def dump(self):
        data = {
            "player_data": self.player.to_dict(),
            "quest_list": [q.to_dict() for q in self.quests]
        }
        
        with open("user_data.json", "w") as file:
            json.dump(data, file, indent=4)

    def load(self):
        try:
            with open("user_data.json", "r") as file:
                data = json.load(file)
                
            p_data = data["player_data"]
            reborn_player = Player(p_data["name"])

            reborn_player.last_login = p_data["last_login"]
            reborn_player.lvl = p_data["level"]
            reborn_player.xp = p_data["xp"]
            reborn_player.gold = p_data["gold"]
            
            self.player = reborn_player

            self.quests = []
            for q_data in data["quest_list"]:
                new_quest = Quest(
                    q_data["name"],
                    q_data["description"],
                    q_data["type"],
                    q_data["difficulty"],
                    q_data["time_limit"]
                )
                new_quest.completed = q_data["completed"]
                new_quest.pinned = q_data["pinned"]
                
                self.quests.append(new_quest)
                
            print("Save file loaded successfully.")
            current_time = date.today().isoformat()
            
            self.quests = [
                q for q in self.quests 
                if q.time_limit is None or q.time_limit >= current_time
            ]
            self.check_daily_reset()


        except FileNotFoundError:
            print("No save file found. Starting new game.")
