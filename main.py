import random
import json
import player

class Game:
    def __init__(self):
        with open("board.json") as board:
            self.game_board = json.load(board)
        with open("actions.json") as game_actions:
            self.game_actions = json.load(game_actions)
        with open("player.json") as player_attribute:
            self.player = json.load(player_attribute)
        self.current_location = 0
        self.current_player = player.Player()
        
    def calculate_current_position(self, dice):
        board_size = self.get_board_size()
        new_position = dice + self.current_location
        if new_position > (board_size - 1):
            self.current_location = (dice + self.current_location) - (board_size - 1)
            self.payday()
        else:
            self.current_location = dice + self.current_location
        return self.current_location
    
    def calculate_tax(self):
        tax_percentage = self.game_actions['tax']
        tax_amount = self.current_player.calculate_payday() * tax_percentage / 100
        print(f"You need to pay $ {tax_amount} tax")
        return tax_amount

    def calculate_charity(self):
        charity_percentage = self.game_actions['charity']
        payday = self.current_player.calculate_payday()
        charity_amount = payday * charity_percentage / 100
        return charity_amount

    def check_game(self):
        game_status = self.current_player.check_game()
        if game_status:
            print('You won the game')
            quit()
        return game_status
    
    def check_keyboard_input(self, msg):
        keyboard_input = input(msg)
        if keyboard_input.upper() == "Y" or keyboard_input == "":
            return True
        else:
            return False

    def payday(self):
        current_pay = self.current_player.calculate_payday()
        self.current_player.payment(current_pay)
        return current_pay

    def output_money(self):
        money = self.current_player.get_player()["finances"]["cash"]
        print(f"current balance $ {money}")
    
    def output_stats(self):
        player = self.current_player.get_player()
        print(f"Name: {player['name']}")
        print(f"Profession: {player['profession']}")
        print(f"Salary: ${player['finances']['salary']}")
        print(f"Cash: ${player['finances']['cash']}")
        print(f"Expenses ${player['expenses']['other']}")

    def deduct_tax(self):
        tax = self.calculate_tax()
        deducted = self.current_player.deduct_amount(tax)
        self.output_money()
        return deducted

    def dice(self):
        dice1 = random.randrange(1,6)
        dice2 = random.randrange(1,6)
        combined = dice1 + dice2
        self.calculate_current_position(combined)
        return combined
    
    def get_board_size(self):
        board_len = len(self.game_board)
        return board_len
    
    def play(self):
        while True:
            self.check_game()
            
            self.output_stats()
            if self.check_keyboard_input("Throw dice? Y / N "):
                self.dice()
                board = self.game_board[str(self.current_location)]
                print(board["name"])
                if board['name'] == "Tax":
                    self.deduct_tax()
                elif board["name"] == "Charity":
                    charity_amount = self.calculate_charity()
                    self.current_player.deduct_amount(charity_amount)
            else:
                quit()

play = Game()
play.play()