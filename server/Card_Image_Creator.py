from PIL import Image

from GameClasses import PlayingCard
from GameClasses import JokerCard

class SpriteSheet:
    def __init__(self, _map, _dim, _fp):
        self.map = _map
        self.dim = _dim
        self.fp = _fp

    def get_sub_image(self, code):

        if code not in self.map:
            print(f"Code {code} not found in sprite map.")
            return None

        # load the image as a file
        try:
            img = Image.open(self.fp)
        except IOError as e:
            print(f"Error opening image file {self.fp}: {e}")
            return None
                
        img_width, img_height = img.size
        card_width = img_width // self.dim["W"]
        card_height = img_height // self.dim["H"]

        # calculate the position of the card in the sprite sheet
        index = self.map.index(code)
        row = index // self.dim["W"]
        col = index % self.dim["W"]
        x = col * card_width
        y = row * card_height

        # Create a new image for the sub-image
        sub_image = Image.new("RGBA", (card_width, card_height))
        # Paste the sub-image from the sprite sheet 
        sub_image.paste(img.crop((x, y, x + card_width, y + card_height)), (0, 0))

        return sub_image

base_fp = "G:\\!Programming\\Lua\\BalatroDataExtractionTest\\server\\assets\\"

deck_map = [
    "H_2",
    "H_3",
    "H_4",
    "H_5",
    "H_6",
    "H_7",
    "H_8",
    "H_9",
    "H_T",
    "H_J",
    "H_Q",
    "H_K",
    "H_A",
    "C_2",
    "C_3",
    "C_4",
    "C_5",
    "C_6",
    "C_7",
    "C_8",
    "C_9",
    "C_T",
    "C_J",
    "C_Q",
    "C_K",
    "C_A",
    "D_2",
    "D_3",
    "D_4",
    "D_5",
    "D_6",
    "D_7",
    "D_8",
    "D_9",
    "D_T",
    "D_J",
    "D_Q",
    "D_K",
    "D_A",
    "S_2",
    "S_3",
    "S_4",
    "S_5",
    "S_6",
    "S_7",
    "S_8",
    "S_9",
    "S_T",
    "S_J",
    "S_Q",
    "S_K",
    "S_A"
]
deck_dim = {
    "H": 4,
    "W": 13
}
deck_fp = base_fp + "8BitDeck.png"

enhancers_list = [
    "red_back",
    "c_base",
    "gold_seal",
    "nebula",
    "locked",
    "stone",
    "gold",
    "soul",
    "bonus",
    "mult",
    "wild",
    "lucky",
    "glass",
    "steel",
    "blue_back",
    "yellow_back",
    "green_back",
    "black_back",
    "plasma_back",
    "odd_back",
    "ghost_back",
    "magic_back",
    "checkerboard_back",
    "erratic_back",
    "abandoned_back",
    "painted_back",
    "no_joker",
    "missing",
    "maze_back",
    "other_back",
    "anaglyph_back",
    "zodiac_back",
    "purple_seal",
    "red_seal",
    "blue_seal"
]
enhancers_dim = {
    "H": 5,
    "W": 7
}
enhancers_fp = base_fp + "Enhancers.png"

editions_list = [
    "base",
    "foil",
    "holographic",
    "polychrome",
    "debuffed"
]
editions_dim = {
    "H": 1,
    "W": 5
}
editions_fp = base_fp + "Editions.png"

jokers_list = [
    "joker",
    "chaos_the_clown",
    "jolly_joker",
    "zany_joker",
    "mad_joker",
    "crazy_joker",
    "droll_joker",
    "half_joker",
    "merry_andy",
    "stone_joker",
    "juggler",
    "drunkard",
    "acrobat",
    "sock_and_buskin",
    "mime",
    "credit_card",
    "greedy_joker",
    "j_lusty_joker",
    "wrathful_joker",
    "gluttonous_joker",
    "troubadour",
    "banner",
    "mystic_summit",
    "marble_joker",
    "loyalty_card",
    "hack",
    "misprint",
    "steel_joker",
    "raised_fist",
    "golden_joker",
    "blueprint",
    "glass_joker",
    "scary_face",
    "abstract_joker",
    "delayed_gratification",
    "golden_ticket",
    "pareidolia",
    "cartomancer",
    "even_steven",
    "odd_todd",
    "wee_joker",
    "business_card",
    "j_supernova",
    "mr_bones",
    "seeing_double",
    "the_duo",
    "the_trio",
    "the_family",
    "the_order",
    "the_tribe",
    "8_ball",
    "fibonacci",
    "joker_stencil",
    "space_joker",
    "matador",
    "ceremonial_dagger",
    "showman",
    "fortune_teller",
    "hit_the_road",
    "swashbuckler",
    "flowerpot",
    "ride_the_bus",
    "shoot_the_moon",
    "scholar",
    "smeared_joker",
    "j_oops",
    "four_fingers",
    "gros_michel",
    "stuntman",
    "hanging_chad",
    "driver_license",
    "invisible_joker",
    "astronomer",
    "burnt_joker",
    "dusk",
    "throwback",
    "idol",
    "brainstorm",
    "satelite",
    "rough_gen",
    "bloodstone",
    "arrowhead",
    "onyx_agate",
    "canio_base",
    "triboulet_base",
    "yorick_base",
    "chicot_base",
    "perkeo_base",
    "certificate",
    "bootstrap",
    "blank1",
    "blank2",
    "hologram_face",
    "canio_face",
    "triboulet_face",
    "yorick_face",
    "chicot_face",
    "perkeo_face",
    "locked",
    "unknown",
    "egg",
    "burglar",
    "blackboard",
    "runner",
    "j_ice_cream",
    "j_dna",
    "splash",
    "blue_joker",
    "sixth_sense",
    "constellation",
    "hiker",
    "faceless_joker",
    "green_joker",
    "superposition",
    "todo",
    "cavendish",
    "card_sharp",
    "red_card",
    "madness",
    "square_joker",
    "seance",
    "riff-raff",
    "vampire",
    "shortcut",
    "hologram_base",
    "vagabond",
    "baron",
    "cloud_9",
    "rocket",
    "obelisk",
    "midas_mask",
    "Luchador",
    "photograph",
    "gift_card",
    "turtle_bean",
    "erosion",
    "reserved_parking",
    "mail-in_rebate",
    "to_the_moon",
    "hallucination",
    "sly_joker",
    "wily_joker",
    "clever_joker",
    "devious_joker",
    "crafty_joker",
    "lucky_cat",
    "baseball_card",
    "bull",
    "diet_cola",
    "trading_card",
    "flash_card",
    "popcorn",
    "ramen",
    "seltzer",
    "spare_trousers",
    "campfire",
    "smiley_face",
    "ancient_joker",
    "walkie_talkie",
    "castle"
]
jokers_dim = {
    "H": 16,
    "W": 10
}
jokers_fp = base_fp + "Jokers.png"

deck_sheet = SpriteSheet(deck_map, deck_dim, deck_fp)
enhancers_sheet = SpriteSheet(enhancers_list, enhancers_dim, enhancers_fp)
editions_sheet = SpriteSheet(editions_list, editions_dim, editions_fp)
jokers_sheet = SpriteSheet(jokers_list, jokers_dim, jokers_fp)

sprite_sheets = {
    "deck": deck_sheet,
    "enhancers": enhancers_sheet,
    "editions": editions_sheet,
    "jokers": jokers_sheet
}

class ImageLayer:
    def __init__(self, _name, _code):
        self.sheet_name = _name,
        self.code = _code

        if isinstance(self.sheet_name, tuple):
            self.sheet_name = str(self.sheet_name[0])
        if isinstance(self.code, tuple):
            self.code = str(self.code[0])
    
class CardImageCreator:
    fp_root = "server/assets/" 

    @staticmethod
    def build_image(_ImageLayer_list):
        if not _ImageLayer_list:
            raise ValueError("ImageLayer list cannot be empty.")
        if not isinstance(_ImageLayer_list, list):
            raise TypeError("Expected a list of ImageLayer objects.")

        # Create a new blank image with RGBA mode
        base_image = Image.new("RGBA", (71, 95), (0, 0, 0, 0))

        for layer in _ImageLayer_list:
            if not isinstance(layer, ImageLayer):
                raise TypeError("All items in the list must be ImageLayer objects.")

            # Get the sprite sheet for the layer
            sheet = sprite_sheets.get(str(layer.sheet_name))
            if not sheet:
                raise ValueError(f"Sprite sheet '{layer.sheet_name}' not found.")

            # Get the sub-image from the sprite sheet
            sub_image = sheet.get_sub_image(layer.code)
            if sub_image is None:
                raise ValueError(f"Sub-image for code '{layer.code}' not found in sprite sheet '{layer.sheet_name}'.")

            # Paste the sub-image onto the base image
            base_image.paste(sub_image, (0, 0), sub_image)

        return base_image

    @staticmethod
    def translate_playing_card(_card):
        if not isinstance(_card, PlayingCard):
            raise TypeError("Expected a PlayingCard object.")
        
        # Ensure that the type, key, and seal are valid
        if _card.type not in enhancers_list:
            print(f"Invalid card type: {_card.type}")
            _card.type = "base"  # Default to base if invalid
        if _card.key not in deck_map:
            print(f"Invalid card key: {_card.key}")
            _card.key = "H_2"  # Default to H_2 if invalid
        if _card.seal not in enhancers_list and _card.seal != "no":            
            print(f"Invalid card seal: {_card.seal}")
            _card.seal = ""

        card_details = [
            ImageLayer(str("enhancers"), _card.type),
            ImageLayer(str("deck"), _card.key),
        ]

        if _card.seal != "" and _card.seal != "no":
            card_details.append(ImageLayer(str("enhancers"), _card.seal))

        # Create the image using the build_image method
        card_image = CardImageCreator.build_image(card_details)
        return card_image

    @staticmethod
    def translate_joker_card(_card):
        if not isinstance(_card, JokerCard):
            raise TypeError("Expected a JokerCard object.")
        
        # Get the type and edition of the joker card
        joker_type = _card.type
        joker_edition = _card.edition_key

        # Ensure that the type and edition are valid
        if joker_type not in jokers_list:
            print(f"Invalid joker type: {joker_type}")
            _card.type = "joker"  # Default to joker if invalid
        if joker_edition not in editions_list:
            print(f"Invalid joker edition: {joker_edition}")
            _card.edition_key = "base"  # Default to base if invalid

        if _card.edition_key == "" or _card.edition_key is None:
            _card.edition_key = "base"

        card_details = []

        # Specific rules for certain jokers
        match _card.type:
            case "canio"|"triboulet"|"yorick"|"chicot"|"perkeo"|"hologram":
                card_details.append(ImageLayer(str("jokers"), f"{_card.type}_base"))
                card_details.append(ImageLayer(str("jokers"), f"{_card.type}_face"))
            case _:
                card_details.append(ImageLayer(str("jokers"), f"{_card.type}"))
                        
        card_details.append(ImageLayer(str("editions"), _card.edition_key))

        # Create the image using the build_image method
        card_image = CardImageCreator.build_image(card_details)
        return card_image

if __name__ == "__main__":

    c = PlayingCard()
    c.key = str("S_A")
    c.type = str("steel")
    c.seal = str("blue_seal")

    img = CardImageCreator.translate_playing_card(c)
    img.save("test_playing_card.png", "PNG")
    print("Card image created and saved as 'test_card.png'")

    j = JokerCard()
    j.type = str("photograph")
    j.edition_key = str("base")

    img = CardImageCreator.translate_joker_card(j)
    img.save("test_joker_card.png", "PNG")
    print("Joker card image created and saved as 'test_joker_card.png'")

