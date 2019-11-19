# from django.contrib.auth.models import User
import sys
sys.path.append('../adventure')
from adventure.models import Player, Room, Item, Container

Room.objects.all().delete()

r_outside = Room(title="Outside Cave Entrance",
                 description="North of you, the cave mount beckons")

r_foyer = Room(title="Foyer", description="""Dim light filters in from the south. Dusty
passages run north and east.""")

r_overlook = Room(title="Grand Overlook", description="""A steep cliff appears before you, falling
into the darkness. Ahead to the north, a light flickers in
the distance, but there is no way across the chasm.""")

r_narrow = Room(title="Narrow Passage", description="""The narrow passage bends here from west
to north. The smell of gold permeates the air.""")

r_treasure = Room(title="Treasure Chamber", description="""You've found the long-lost treasure
chamber! Sadly, it has already been completely emptied by
earlier adventurers. The only exit is to the south.""")

r_outside.save()
r_foyer.save()
r_overlook.save()
r_narrow.save()
r_treasure.save()

# Link rooms together
r_outside.connect_rooms(r_foyer, "n")
r_foyer.connect_rooms(r_outside, "s")

r_foyer.connect_rooms(r_overlook, "n")
r_overlook.connect_rooms(r_foyer, "s")

r_foyer.connect_rooms(r_narrow, "e")
r_narrow.connect_rooms(r_foyer, "w")

r_narrow.connect_rooms(r_treasure, "n")
r_treasure.connect_rooms(r_narrow, "s")

# Adding items to rooms.
Item.objects.all().delete()
thing = Item(name='thing', description='just a thing')
thing.save()
r_outside.add_item(thing)

players = Player.objects.all()
for p in players:
    p.currentRoom = r_outside.id
    p.save()

print('World Created!! Good Job!')