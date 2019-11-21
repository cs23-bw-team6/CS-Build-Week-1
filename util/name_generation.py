import random

room_types = ['Cave', 'Antechamber', 'Lanai', 'Armory', 'Den', 'Storeroom', 'Rec-room', 'Kitchen',
              'Bedroom', 'Bathroom', 'Mud Room', 'Great Hall', 'Office', 'Library', 'Nursery', 'Dressing Room',
              'Ballroom', 'Drawing Room', 'Sitting Room', 'Game Room', 'Breakfast Nook', 'Study', 'Closet', 'Basement']
adjectives = ['Brutal', 'Frozen', 'Impostor', 'Invisible', 'Savage', 'Treacherous', 'Ruthless',
              'Ferocious', 'Hapless', 'Traitorous', 'Perfidious', 'Duplicitous', 'Precarious', 'Malignant',
              'Wicked', 'Menacing', 'Perilous', 'Unscrupulous', 'Sneaky', 'Oozing', 'Scraggly', 'Odoriferous']
nouns = ['Orc', 'Phoenix', 'Army', 'Tombs', 'Elf', 'Goblin', 'Kobold', 'Dwarf', 'Gremlin', 'Bolrog', 'Demigorgon',
         'Halfling', 'Gnome', 'Giant', 'Treant', 'Dragon-born', 'Ent', 'Mermaid', 'Troll', 'Satyr', 'T-Rex',
         'Bandersnatch', 'Sphinx']
wall_things = ['Tapestries', 'Burning torches in iron sconces', 'Cobwebs', 'Damaged mosaics of heroic deeds', 
'Rusting spikes', 'Giant manacles and chains', 'Tiny manacles and chains', 'Suspicious slimes', 
'Portraits of lords and ladies', 'Skulls', 'Weapons', 'Coats of armor', 'Rudimentary drawings', ]
room_state = ['is a corpse on the floor', 'is a pit of spikes set into the floor', 'is a rotting feast on long tables with skeletons in the seats', 
'is nice furniture that is strangely clean for a dungeon', 'a rug that really ties the room together', 'is a bunch of trash on the floor', 
'is a race of tiny humanoids building a futuristic metropolis with skyscrapers that come up to your ankle', 'is broken furniture strewn about', 
'is a lonely Treant who appears eager to start a conversation', 'is a family of gnomes who want you to stop disturbing their dinner',
'is a warband of Kobolds making threatening gestures', 'is an old wizard using prestidigitation to clean his robes', 
'is an unhinged looking warlock trying to use eldritch blast on rats', 'is a talking mirror with an attitude problem', 
'is a bubbling cauldron that appears unattended...for now', 'is a strange bit of jewelry that seems to psychically whisper to you', 
'is a wizard that seems to be having some sort of dispute with a large fire demon', 
]


def make_name():
    name = f"{random.choice(room_types)} of the {random.choice(adjectives)} {random.choice(nouns)}"
    description = f"You are in the {name}. {random.choice(wall_things)} line the walls and there {random.choice(room_state)}."
    return name, description


def adj_noun():
    name = f"{random.choice(adjectives)} {random.choice(nouns)}"
    return name
