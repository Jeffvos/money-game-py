import random
import json

class Game:
    def __init__(self):
        with open("board.json") as board:
            self.game_board = json.load(board)
        with open("actions.json") as game_actions:
            self.game_actions = json.load(game_actions)
        self.current_location = 0
        self.player = {"name":"", "profession":"", "money":0, "assets":{},"loans":{}}
        self.create_player()

    def create_player(self):
        self.player["name"] = input("whats your name?: ")
        professions = []
        for profession in self.game_actions["professions"]:
            professions.append(profession)
        self.player["profession"] = professions[random.randrange(0, (len(professions)))]
        print(self.player)
        
    def calculate_current_position(self, dice):
        board_size = self.get_board_size()
        new_position = dice + self.current_location
        if new_position > (board_size - 1):
            self.current_location = (dice + self.current_location) - (board_size - 1)
            self.payday()
        else:
            self.current_location = dice + self.current_location
        print(self.current_location)

    def payday(self):
        current_pay = self.calculate_payday()
        self.player["money"] = self.player["money"] + current_pay

    def calculate_payday(self):
        salary = self.game_actions["professions"][self.player["profession"]]["salary"]
        asset_payout = 0
        payday = 0
        if len(self.player['assets']) > 0:
            for asset in self.player['assets']:
                payday = payday + asset['payout']
        if len(self.player['loans']) > 0:
            for loan in self.player['loans']:
                payday = payday - loan
        payday = salary + asset_payout - self.game_actions["professions"][self.player["profession"]]['expenses']
        return payday
    
    def calculate_tax(self):
        tax_percentage = self.game_actions['tax']
        tax_amount = self.calculate_payday() * tax_percentage / 100
        print(f"You need to pay $ {tax_amount} tax")
        return tax_amount

    def output_money(self):
        money = self.player["money"]
        print(f"current balance $ {money}")

    def deduct_tax(self):
        tax = self.calculate_tax()
        self.player["money"] = self.player["money"] - tax

    def dice(self):
        dice1 = random.randrange(1,6)
        dice2 = random.randrange(1,6)
        combined = dice1 + dice2
        print(combined)
        self.calculate_current_position(combined)
        return combined
    
    def get_board_size(self):
        board_len = len(self.game_board)
        return board_len
    
    def play(self):
        while True:
            throw_dice = input("Throw dice? Y / N ")
            if throw_dice.upper() == "Y" or throw_dice == "":
                print(self.player)
                self.dice()
                board = self.game_board[str(self.current_location)]
                print(board)
                if board['name'] == "Tax":
                    self.deduct_tax()
                    self.output_money()
            else:
                quit()

play = Game()
play.play()