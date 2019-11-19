import random

room_types = ['Cave', 'Antechamber', 'Lanai', 'Armory', 'Den', 'Storeroom', 'Recroom', 'Kitchen',
              'Bedroom', 'Bathroom', 'Mud Room', 'Great Hall', 'Office', 'Library', 'Nursery', 'Dressing Room',
              'Ballroom', 'Drawing Room', 'Sitting Room', 'Game Room']
adjectives = ['Brutal', 'Frozen', 'Imposter', 'Invisible', 'Savage', 'Treacherous', 'Ruthless',
              'Ferocious', 'Hapless', 'Traiterous', 'Perfidious', 'Duplicitous', 'Precarious', 'Malignant',
              'Wicked', 'Menacing', 'Perilous']
nouns = ['Orc', 'Phoenix', 'Army', 'Tombs', 'Elf', 'Goblin', 'Kobold', 'Dwarf', 'Gremlin',
         'Halfling', 'Gnome', 'Giant', 'Treant', 'Dragonborn', 'Ent', 'Mermaid', 'Troll', 'Satyr',
         'Bandersnatch', 'Sphinx']


def make_name():
    name = f"{random.choice(room_types)} of the {random.choice(adjectives)} {random.choice(nouns)}"
    return name
