import random
from .room_names import name_desc

room_types = ['Cave', 'Antechamber', 'Lanai', 'Armory', 'Den', 'Storeroom', 'Rec-room', 'Kitchen',
              'Bedroom', 'Bathroom', 'Mud Room', 'Great Hall', 'Office', 'Library', 'Nursery', 'Dressing Room',
              'Ballroom', 'Drawing Room', 'Sitting Room', 'Game Room', 'Breakfast Nook', 'Study', 'Closet', 'Basement']
adjectives = ['Brutal', 'Frozen', 'Impostor', 'Invisible', 'Savage', 'Treacherous', 'Ruthless',
              'Ferocious', 'Hapless', 'Traitorous', 'Perfidious', 'Duplicitous', 'Precarious', 'Malignant',
              'Wicked', 'Menacing', 'Perilous', 'Unscrupulous', 'Sneaky', 'Oozing', 'Scraggly', 'Odoriferous']
nouns = ['Orc', 'Phoenix', 'Army', 'Tombs', 'Elf', 'Goblin', 'Kobold', 'Dwarf', 'Gremlin', 'Bolrog', 'Demigorgon',
         'Halfling', 'Gnome', 'Giant', 'Treant', 'Dragon-born', 'Ent', 'Mermaid', 'Troll', 'Satyr', 'T-Rex',
         'Bandersnatch', 'Sphinx']


def make_name():
    name = f"{random.choice(room_types)} of the {random.choice(adjectives)} {random.choice(nouns)}"
    return name


def adj_noun():
    name = f"{random.choice(adjectives)} {random.choice(nouns)}"
    return name


def make_name_desc(i):
    rand = name_desc[i - 1]
    name, desc = rand[0], rand[1]
    return name, desc
