import sys
sys.path.append('../adventure')
from adventure.models import Player, Room, Item, Container
import numpy
Room.objects.all().delete()

locations = [['n', 's'], ['e', 'w']]
# range = [range(1000)]
rooms = []

def create_rooms():
    n = 1000
    r = Room(title=i,
        description=i+2)
    


# Create Root
# Iterate 
for i in range(1000):
    r = Room(title=i,
                 description=i+2
                 )
    rooms.append(r)
    r.save()

for j in rooms:
    room_1 = numpy.random.choice(rooms)
    rooms.remove(room_1)

    room_2 = numpy.random.choice(rooms)
    rooms.remove(room_2)

    if numpy.random.choice([0,1]) == 0:
        room_3 = numpy.random.choice(rooms)
        loc =  locations[0]
        loc_1 = loc[0]
        loc_2 = loc[1]


        room_2.connect_rooms(room_1, loc_1)
        room_1.connect_rooms(room_2, loc_2)
        loc =  locations[1]
        loc_1 = loc[0]
        loc_2 = loc[1]

        room_3.connect_rooms(room_1, loc_1)
        room_1.connect_rooms(room_3, loc_2)

    else:
        loc =  locations[numpy.random.choice([0,1])]
        loc_1 = loc[0]
        loc_2 = loc[1]


        room_2.connect_rooms(room_1, loc_1)
        room_1.connect_rooms(room_2, loc_2)

Item.objects.all().delete()
thing = Item(name='thing', description='just a thing')
thing.save()
room_1.add_item(thing)

players = Player.objects.all()
for p in players:
    p.currentRoom = room_1.id
    p.save()

print('World Created!! Good Job!')
