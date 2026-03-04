class Player:
    def __init__(self, name):
        self.name = name
        self.xp = 0
        self.lvl = 1
        self.gold = 0

    def get_xp_until_next(self):
        return (self.lvl * 1000)

    def get_xp(self):
        return self.xp

    def get_gold(self):
        return self.gold

    def gain_xp(self, amount):
        levelled_up = False
        self.xp += amount
        while self.xp >= int(self.get_xp_until_next()):
            self.xp -= self.get_xp_until_next()
            print("Level up!")
            self.lvl += 1
            levelled_up = True
        if levelled_up:
            print(f"You have reached level {self.lvl}")

    def gain_gold(self, amount):
        self.gold += amount

    def spend_gold(self, amount):
        if self.gold - amount < 0:
            print("Not enough money!")
            return
        self.gold -= amount
    
    def to_dict(self):
        return {
            "name": self.name,
            "level": self.lvl,
            "xp": self.xp,
            "gold": self.gold
            }