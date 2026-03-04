from datetime import datetime

REWARD_CONFIG = {
    "type_multipliers": {
        "Main Quest": [2.5, 1],
        "Side Quest": [0.5, 1],
        "Training": [1.5, 0.1],
        "Guild Work": [1, 1],
        "Boss Battle": [5, 5],
        "Emergency": [1, 0.5]
    },
    "base_rewards": {
        1: {"xp": 50, "gold": 10},
        2: {"xp": 100, "gold": 25},
        3: {"xp": 200, "gold": 60},
        4: {"xp": 500, "gold": 150}
    }
}

class Quest:
    def __init__(self, name, desc, quest_type, difficulty, time_limit=None):
        self.name = name
        self.desc = desc
        self.type = quest_type
        self.diff = difficulty
        self.issued = datetime.now().isoformat()
        self.time_completed = None
        self.time_limit = time_limit
        self.completed = False
        self.pinned = False

        base = REWARD_CONFIG["base_rewards"][difficulty]
        multiplier = REWARD_CONFIG["type_multipliers"][quest_type]
        self.xp = int(base["xp"] * multiplier[0])
        self.gold = int(base["gold"] * multiplier[1])

    def get_status(self):
        if self.completed:
            return "Completed"
        else:
            return "Not completed"

    def get_diff(self):
        match (self.diff):
            case 1:
                return "Easy"
            case 2:
                return "Medium"
            case 3:
                return "Hard"
            case 4:
                return "Impossible"
            case _:
                return ""

    def get_issued(self):
        return self.issued

    def get_info(self):
        print(f"\nName: {self.name}\nType: {self.type}\nDifficulty: {self.get_diff()} \nDescription: {self.desc}\nReward: {self.xp}xp\nStatus: {self.get_status()}\n")

    def complete(self, player):
        if self.completed:
            raise ValueError("This quest is already completed!")
        print(f"You have completed {self.name}!\nYou have gained {self.xp} xp!")
        self.time_completed = datetime.now().isoformat()
        player.gain_xp(self.xp)
        self.completed = True

    def pin(self):
        self.pinned = True

    def to_dict(self):
        return {
            "name": self.name,
            "description": self.desc,
            "type": self.type,
            "difficulty": self.diff,
            "issued_time": self.issued,
            "completed_time": self.time_completed,
            "completed": self.completed,
            "pinned": self.pinned
            }