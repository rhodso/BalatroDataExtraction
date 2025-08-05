
import json

class Helpers:
    @staticmethod
    def pre_deserialize(_data):
        if not _data:
            raise ValueError("No data provided for Game pre-deserialization")
        
        # If data is a string, parse it as JSON
        if isinstance(_data, str):
            _data = json.loads(_data)

        # Validate the input data
        if not isinstance(_data, dict):
            raise ValueError("Invalid data format for Game pre-deserialization")

        return _data

class PlayingCard:

    def __init__(self):
        self.key = None
        self.name = None
        self.pos = None
        self.seal = None
        self.type = None
        self.rank = None
        self.suit = None

    @staticmethod
    # Returns the rank and suit of a card as an array from the card key
    def get_card_info(_card_name):
        if not _card_name:
            return None, None

        info = _card_name.split(' of ')

        if len(info) != 2:
            raise ValueError(f"Invalid card key format: {_card_name}. Expected format is '`rank` of `suit`'.")

        # Extract the rank and suit from the card key
        rank = info[0]
        suit = info[1]

        return rank, suit

    @staticmethod
    # Returns severl PlayingCard objects as an array
    def deserialize(_data):
        data = Helpers.pre_deserialize(_data)
        data = data.get('hand', {})
        objects = []

        # # Extract and assign attributes from the data dictionary
        for card_itm in data:
            c = PlayingCard()
            c.key = card_itm.get('card_key')
            c.name = card_itm.get('card_name')
            c.pos = card_itm.get('card_pos')
            c.seal = card_itm.get('card_seal')
            c.type = card_itm.get('card_type')

            # Get the rank and suit from the card key
            c.rank, c.suit = PlayingCard.get_card_info(c.name)

            objects.append(c)

        # Sort the objects by their position
        objects.sort(key=lambda x: x.pos)

        return objects
    
    def __str__(self):
        return f"{self.type} {self.rank} of {self.suit} ({self.key}) with {self.seal} seal"

class JokerCard:
    def __init__(self):
        self.type = None
        self.pos = None
        self.edition = None
        self.edition_key = None

    @staticmethod
    # Returns several JokerCard objects as an array
    def deserialize(_data):
        data = Helpers.pre_deserialize(_data)
        data = data.get('jokers', {})
        objects = []

        # Extract and assign attributes from the data dictionary
        for jkr in data:
            j = JokerCard()
            j.type = jkr.get('card_type')
            j.pos = jkr.get('card_pos')
            j.edition = jkr.get('card_ed')
            if j.edition is None or j.edition == []:
                j.edition = {}
                j.edition_key = ""
            else:
                j.edition = jkr.get('card_ed')
                j.edition_key = " " + j.edition.get('key') 
            objects.append(j)

        # Sort the objects by their position
        # objects.sort(key=lambda x: x.pos)

        return objects

    def __str__(self):
        return f"{self.edition_key} {self.type}"

class PlayedHand:
    def __init__(self):
        self.name = None
        self.chips = None
        self.level = None
        self.mult = None
        self.order = None
        self.played = None
        self.played_this_round = None

    @staticmethod
    # Returns several PlayedHand objects as an array
    def deserialize(_data):
        data = Helpers.pre_deserialize(_data)
        data = data.get('hands', {})
        objects = []

        # The key of each object is the name of the hand
        for key, value in data.items():
            hand = PlayedHand()
            hand.name = key
            hand.chips = value.get('chips')
            hand.level = value.get('level')
            hand.mult = value.get('mult')
            hand.order = value.get('order')
            hand.played = value.get('played')
            hand.played_this_round = value.get('played_this_round')
            objects.append(hand)       

        # Sort the objects by their order
        objects.sort(key=lambda x: x.order) 

        return objects

    def __str__(self):
        return f"{self.name} (Level: {self.level}) Scores {self.chips} chips and {self.mult}x mult. Played: {self.played}"

class Blind:
    def __init__(self):
        self.name = ""
        self.chips = -1
    
    @staticmethod
    # Returns a Blind object
    def deserialize(_data):
        data = Helpers.pre_deserialize(_data)
        
        # Extract and assign attributes from the data dictionary
        b = Blind()
        b.name = {}
        b.name = data.get('blind')
        b.name = b.name[0].get('name') if b.name else "UNKNOWN"
        b.chips = data.get('blind_chip')

        return b

class Game:
    def __init__(self):
        # Simple game attributes
        self.seed = None
        self.skips = None
        self.stake = None
        self.chips = None
        self.dollars = None
        self.hands_played = None
        self.hands_left = None
        self.discards_left = None

        # More complex game attributes
        self.Hand = []   # List of PlayingCard objects
        self.Jokers = [] # List of JokerCard objects
        self.Hands = [] # List of PlayedHand objects
        self.Blind = None # Blind object

    def deserialize(self, _data):
        data = Helpers.pre_deserialize(_data)

        # Extract simple game attributes
        self.seed = data.get('seed')
        self.skips = data.get('skips')
        self.stake = data.get('stake')
        self.chips = data.get('chips')
        self.dollars = data.get('dollars')
        self.hands_played = data.get('hands_played')

        d = data.get('current_round')
        if d:
            self.hands_left = d[0].get('hands_left')
            self.discards_left = d[0].get('discards_left')
        else:
            # If current_round is not present, set hands_left and discards_left to None
            self.hands_left = None
            self.discards_left = None

        # Extract and deserialize Other objects
        self.Hand = PlayingCard.deserialize(data)
        self.Jokers = JokerCard.deserialize(data)
        self.Hands = PlayedHand.deserialize(data)
        self.Blind = Blind()
        self.Blind = Blind.deserialize(data)

    def __str__(self):
        s = f"Game Seed: {self.seed}\n"
        s += f"Current score: {self.chips} chips, {self.dollars} dollars\n"
        s += f"Player has {self.hands_left} hands left and {self.discards_left} discards left\n"
        
        if self.Blind == None or self.Blind.name == None or self.Blind.chips == None:
            s += "Blind: Unknown needs 0 chips\n"
        else:        
            s += f"Blind: {self.Blind.name} needs {self.Blind.chips} chips\n"
        
        s += f"\n{len(self.Hand)} card in hand:\n"
        for card in self.Hand:
            s += f"  {str(card)}\n"
        
        s += f"\n{len(self.Jokers)} jokers in play:\n"
        for joker in self.Jokers:
            s += f"  {str(joker)}\n"
        
        s += f"\n{self.hands_played} hands played:\n"
        for hand in self.Hands:
            s += f"  {str(hand)}\n"

        return s

if __name__ == "__main__":
    # Test useage

    # Load a sample JSON file at "../json_dump.json"
    with open("G:\\!Programming\\Lua\\BalatroDataExtractionTest\\json_dump.json", "r", encoding="utf-8") as f:
        file_data = f.read()

    # print(file_data)  

    # Deserialize the data
    game = Game()
    game.deserialize(file_data)

    # Ensure the objects are created correctly
    if not game.Hand or not game.Jokers or not game.Hands or not game.Blind:
        print("Error: One or more objects were not created correctly.")
        exit(1)

    # Print some sample information about the game
    print(game)
    print("Objects created successfully!")

