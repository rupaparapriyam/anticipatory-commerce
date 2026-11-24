"""Words to catalogue values: the closed vocabulary this agent reads.

The catalogue has 16 categories, 16 colours, 18 brands and 18 sizes. A shopper says
them in many more ways than that, so every phrase a shopper might use is mapped to the
one value the catalogue stores. Phrases are matched longest-first, so "navy blue" is
read as navy and never as blue, and "olive green" as olive.
"""

# ---------------------------------------------------------------- categories
CATEGORY = {
    "running shoes": "running shoes", "running shoe": "running shoes",
    "runners": "running shoes", "jogging shoes": "running shoes",
    "running sneakers": "running shoes", "jogging shoe": "running shoes",
    "sneakers": "sneakers", "sneaker": "sneakers", "casual shoes": "sneakers",
    "casual sneakers": "sneakers", "casual shoe": "sneakers", "trainers": "sneakers",
    "sandals": "sandals", "sandal": "sandals", "slides": "sandals",
    "floaters": "sandals", "chappals": "sandals", "chappal": "sandals",
    "t shirt": "t-shirts", "t-shirt": "t-shirts", "tshirt": "t-shirts",
    "t shirts": "t-shirts", "t-shirts": "t-shirts", "tshirts": "t-shirts",
    "tee": "t-shirts", "tees": "t-shirts",
    "shirt": "shirts", "shirts": "shirts", "formal shirt": "shirts",
    "hoodie": "hoodies", "hoodies": "hoodies", "hooded sweatshirt": "hoodies",
    "sweatshirt": "hoodies", "hooded top": "hoodies",
    "jacket": "jackets", "jackets": "jackets",
    "jeans": "jeans", "denims": "jeans", "denim": "jeans",
    "pair of jeans": "jeans",
    "track pants": "track pants", "trackpants": "track pants",
    "joggers": "track pants", "track pant": "track pants",
    "kurta": "kurtas", "kurtas": "kurtas",
    "dress": "dresses", "dresses": "dresses",
    "backpack": "backpacks", "backpacks": "backpacks", "bag pack": "backpacks",
    "rucksack": "backpacks", "bagpack": "backpacks",
    "cap": "caps", "caps": "caps", "hat": "caps",
    "headphones": "headphones", "headphone": "headphones", "headset": "headphones",
    "earphones": "headphones",
    "watch": "watches", "watches": "watches", "wrist watch": "watches",
    "wristwatch": "watches",
    "wallet": "wallets", "wallets": "wallets",
    # Wordings the development set does not use, added so an unseen synonym on the
    # hidden set does not cost a whole request.
    "sports shoes": "running shoes", "running trainers": "running shoes",
    "jogger shoes": "running shoes", "marathon shoes": "running shoes",
    "trail shoes": "running shoes", "running footwear": "running shoes",
    "keds": "sneakers", "canvas shoes": "sneakers", "lifestyle shoes": "sneakers",
    "casual footwear": "sneakers", "plimsolls": "sneakers", "kicks": "sneakers",
    "flip flops": "sandals", "sliders": "sandals", "slippers": "sandals",
    "sliders sandals": "sandals", "open footwear": "sandals", "slipper": "sandals",
    "half sleeve tee": "t-shirts", "crew neck": "t-shirts", "crewneck": "t-shirts",
    "round neck": "t-shirts", "polo": "t-shirts", "polo tee": "t-shirts",
    "formal shirts": "shirts", "casual shirt": "shirts", "button down": "shirts",
    "button up": "shirts", "office shirt": "shirts",
    "pullover": "hoodies", "hoody": "hoodies", "sweat shirt": "hoodies",
    "hooded jacket": "hoodies", "zip hoodie": "hoodies",
    "windcheater": "jackets", "bomber": "jackets", "bomber jacket": "jackets",
    "coat": "jackets", "overcoat": "jackets", "puffer": "jackets",
    "jeans pant": "jeans", "denim pants": "jeans", "jean": "jeans",
    "sweat pants": "track pants", "lower": "track pants", "lowers": "track pants",
    "track suit": "track pants", "tracks": "track pants", "pyjama": "track pants",
    "jogger pants": "track pants", "trackpant": "track pants",
    "kurta top": "kurtas", "ethnic top": "kurtas", "kurti": "kurtas",
    "gown": "dresses", "frock": "dresses", "one piece": "dresses",
    "maxi": "dresses", "midi dress": "dresses",
    "haversack": "backpacks", "school bag": "backpacks", "laptop bag": "backpacks",
    "back pack": "backpacks", "bag": "backpacks",
    "baseball cap": "caps", "snapback": "caps", "topi": "caps",
    "ear phones": "headphones", "ear buds": "headphones", "earbuds": "headphones",
    "cans": "headphones", "over ear headphones": "headphones",
    "hand watch": "watches", "analog watch": "watches", "digital watch": "watches",
    "ghadi": "watches",
    "purse": "wallets", "card holder": "wallets", "batua": "wallets",
}

# ---------------------------------------------------------------- colours
COLOUR = {
    "black": "black", "kaala": "black", "kala": "black",
    "white": "white", "safed": "white",
    "navy blue": "navy", "navy": "navy",
    "blue": "blue", "neela": "blue", "neeli": "blue",
    "grey": "grey", "gray": "grey", "slate": "grey",
    "olive green": "olive", "olive": "olive",
    "green": "green", "hara": "green", "hara": "green",
    "red": "red", "laal": "red", "lal": "red",
    "maroon": "maroon",
    "beige": "beige", "cream": "beige",
    "brown": "brown", "bhura": "brown",
    "yellow": "yellow", "peela": "yellow",
    "pink": "pink", "gulabi": "pink",
    "tan": "tan",
    "golden": "gold", "gold": "gold",
    "silver": "silver", "silvery": "silver",
    # Further colour words, including Hindi ones the development set does not use.
    "jet black": "black", "charcoal": "grey", "ash": "grey", "gunmetal": "grey",
    "off white": "white", "ivory": "white", "chalk": "white",
    "navy blue colour": "navy", "midnight blue": "navy", "dark blue": "navy",
    "royal blue": "blue", "sky blue": "blue", "aqua": "blue", "neela rang": "blue",
    "bottle green": "green", "forest green": "green", "hari": "green",
    "military green": "olive", "army green": "olive",
    "crimson": "red", "scarlet": "red", "laal rang": "red",
    "wine": "maroon", "burgundy": "maroon", "oxblood": "maroon",
    "sand": "beige", "khaki": "beige", "nude": "beige", "oatmeal": "beige",
    "chocolate": "brown", "coffee": "brown", "camel": "tan", "caramel": "tan",
    "mustard": "yellow", "lemon": "yellow", "peeli": "yellow",
    "rose": "pink", "blush": "pink", "magenta": "pink", "gulaabi": "pink",
    "rose gold": "gold", "sona": "gold", "chandi": "silver", "grey silver": "silver",
    "kaali": "black", "safeda": "white",
}

# ---------------------------------------------------------------- brands
BRANDS = ("Urbanyx", "Pacevo", "Loomsy", "Strydo", "Northweft", "Tanaro",
          "Zentrail", "Kudova", "Mehrin", "Kesar Loom", "Wavlo", "Carrafel",
          "Audora", "Packwise", "Sonquil", "Horavo", "Tikkra", "Ledgerly")
BRAND = {b.lower(): b for b in BRANDS}

# ---------------------------------------------------------------- sizes
LETTER_SIZE = {
    "xs": "XS", "extra small": "XS", "x small": "XS", "xsmall": "XS",
    "s": "S", "small": "S",
    "m": "M", "medium": "M", "med": "M",
    "l": "L", "large": "L", "lrg": "L",
    "xl": "XL", "extra large": "XL", "x large": "XL", "xlarge": "XL",
    "xxl": "XXL", "double xl": "XXL", "2xl": "XXL", "double extra large": "XXL",
    "xx large": "XXL", "xxlarge": "XXL",
    # Other ways shoppers say a size.
    "extra extra large": "XXL", "xx-large": "XXL", "triple xl": "XXL",
    "x-small": "XS", "x-large": "XL", "sm": "S", "md": "M", "lg": "L",
    "chhota": "S", "bada": "L", "mota": "XL",
}
# Spelled-out numbers that can be a shoe size or a waist.
NUMBER_SIZE = {
    "six": "6", "seven": "7", "eight": "8", "nine": "9", "ten": "10",
    "eleven": "11", "twenty eight": "28", "thirty": "30", "thirty two": "32",
    "thirty four": "34", "thirty six": "36",
}
SHOE_SIZES = {"6", "7", "8", "9", "10", "11"}
WAIST_SIZES = {"28", "30", "32", "34", "36"}

# Categories measured in shoe sizes rather than letters.
SHOE_CATEGORIES = {"running shoes", "sneakers", "sandals"}
WAIST_CATEGORIES = {"jeans"}
# Categories that have no size at all in the catalogue.
SIZELESS_CATEGORIES = {"backpacks", "caps", "headphones", "watches", "wallets"}

# ---------------------------------------------------------------- numbers
UNITS = {"zero": 0, "one": 1, "two": 2, "three": 3, "four": 4, "five": 5,
         "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10,
         "eleven": 11, "twelve": 12, "thirteen": 13, "fourteen": 14,
         "fifteen": 15, "sixteen": 16, "seventeen": 17, "eighteen": 18,
         "nineteen": 19}
TENS = {"twenty": 20, "thirty": 30, "forty": 40, "fourty": 40, "fifty": 50,
        "sixty": 60, "seventy": 70, "eighty": 80, "ninety": 90}
SCALES = {"hundred": 100, "sau": 100, "thousand": 1000, "hazaar": 1000,
          "hazar": 1000, "k": 1000, "lakh": 100000}
# Hindi number words and the halves.
HINDI_UNITS = {"ek": 1, "do": 2, "teen": 3, "char": 4, "chaar": 4, "paanch": 5,
               "panch": 5, "chhe": 6, "cheh": 6, "saat": 7, "aath": 8,
               "nau": 9, "das": 10, "gyarah": 11, "barah": 12, "terah": 13,
               "chaudah": 14, "pandrah": 15, "solah": 16, "satrah": 17,
               "atharah": 18, "unnees": 19, "bees": 20, "pachees": 25,
               "tees": 30, "chalees": 40, "pachaas": 50, "pachas": 50,
               "saath": 60, "sattar": 70, "assi": 80, "nabbe": 90}
HINDI_HALF = {"saadhe": 0.5, "sadhe": 0.5}      # saadhe teen = 3.5
HINDI_SPECIAL = {"dedh": 1.5, "derh": 1.5, "adhai": 2.5, "dhai": 2.5,
                 "sawa": 1.25}

# Words that mean "the number coming next is a ceiling on the price".
BUDGET_CUES_BEFORE = ("under", "below", "less than", "lesser than", "within", "max",
                      "maximum", "up to", "upto", "budget", "not more than",
                      "nothing over", "no more than", "at most", "cheaper than",
                      "around", "about", "for under", "price", "costing")
# Hindi-style cues that come AFTER the number: "2000 tak", "pandrah sau se kam".
BUDGET_CUES_AFTER = ("tak", "se kam", "ke andar", "ke neeche", "se neeche", "tk",
                     "se jyada nahi", "ke under", "or less", "or below")
BUDGET_CUES = BUDGET_CUES_BEFORE + BUDGET_CUES_AFTER
# Words that say the next number is a size.
SIZE_CUES = ("size", "uk", "waist", "number", "uk size", "size uk", "naap",
             "size no", "eu")
# Words that retract whatever was said before them.
CORRECTION_CUES = ("oops", "sorry", "no wait", "wait", "i mean", "i meant",
                   "scratch that", "change that to", "make that", "actually",
                   "no no", "nope", "not", "instead", "hmm", "um", "uh", "er",
                   "rather", "correction", "my bad", "nahi", "nahin")
