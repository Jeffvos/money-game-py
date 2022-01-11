import json
import random

class Player:
    def __init__(self):
        with open("player.json") as player_attribute:
            self.player = json.load(player_attribute)
        with open("actions.json") as game_actions:
            self.game_actions = json.load(game_actions)
        self.player["name"] = input("whats your name?: ")
        professions = []
        for profession in self.game_actions["professions"]:
            professions.append(profession)
        current_profession = professions[random.randrange(0, (len(professions)))]
        self.player["profession"] = current_profession
        self.player["finances"]["salary"] = self.game_actions['professions'][current_profession]['salary']
        self.player["expenses"]["other"] = self.game_actions['professions'][current_profession]['expenses']

    def get_player(self):
        player = self.player
        return player
    
    def calculate_payday(self):
        salary = self.player["finances"]["salary"]
        asset_payout = 0
        payday = 0
        if len(self.player['assets']) > 0:
            for asset in self.player['assets']:
                payday = payday + asset['payout']
        if len(self.player['finances']['loans']) > 0:
            for loan in self.player['loans']:
                payday = payday - loan
        payday = salary + asset_payout - self.game_actions["professions"][self.player["profession"]]['expenses']
        return payday
    
    def payment(self, amount):
        self.player["finances"]["cash"] = self.player["finances"]["cash"] + amount
        self.output_transaction(f"+${amount}")
        return self.player["finances"]["cash"]

    def deduct_amount(self, amount):
        full_amount = self.player["finances"]["cash"] - amount
        self.player["finances"]["cash"] = self.player["finances"]["cash"] - amount
        self.output_transaction(f"-${amount}")
        return self.player["finances"]["cash"]
    
    def output_transaction(self, transaction):
        print(f"transaction of {transaction}")
        return transaction