import json
from datetime import datetime
from player import Player
from quest import Quest

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

        if final_type == "Boss Battle":
            due_date = input("When is the deadline? (YYYY-MM-DD): ").strip()
            desc = f"[DUE: {due_date}] {desc}"

        print("\nHow difficult is it?")
        print("1. Easy | 2. Medium | 3. Hard | 4. Impossible")
        
        d_choice = input("Choose (1-4): ").strip()
        while not d_choice.isdigit() or not (1 <= int(d_choice) <= 4):
            print("Please enter a number between 1 and 4.")
            d_choice = input("Choose (1-4): ").strip()

        final_diff = int(d_choice)

        self.quests.append(Quest(name, desc, final_type, final_diff))
        print(f"\n[+] Quest '{name}' added!")

    def delete_quest(self, i):
        self.quests.pop(i)

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
                    q_data["difficulty"]
                )
                new_quest.completed = q_data["completed"]
                new_quest.pinned = q_data["pinned"]
                
                self.quests.append(new_quest)
                
            print("Save file loaded successfully.")
            for i in range(len(self.quests)):
                if self.quests[i].time_limit < datetime.now().isoformat():
                    self.delete_quest(i)

        except FileNotFoundError:
            print("No save file found. Starting new game.")
