# Sample Python code that can be used to generate rooms in
# a zig-zag pattern.
#
# You can modify generate_rooms() to create your own
# procedural generation algorithm and use print_rooms()
# to see the world.
from adventure.models import Item, Container, Room, Player
from .name_generation import make_name, adj_noun
from collections import deque
import random


class World:
    def __init__(self):
        self.grid = None
        self.width = 0
        self.height = 0
        self.room_count = 1

    def generate_rooms(self, size_x, size_y, num_rooms):
        # Initialize the grid
        self.grid = [None] * size_y
        self.width = size_x
        self.height = size_y
        for i in range(len(self.grid)):
            self.grid[i] = [None] * size_x

        mid_y = (size_y // 2)
        mid_x = (size_x // 2)

        first = Room(title=make_name(), x=mid_x, y=mid_y)
        first.save()
        self.grid[first.y][first.x] = first.id
        queue = deque()
        queue.append(first)
        print('I am first', first.id)
        while self.room_count < num_rooms:
            current_room = queue.popleft()
            for direction, delta_x, delta_y in zip(['n', 'w', 's', 'e'], [0, 1, 0, -1], [-1, 0, 1, 0]):
                if not eval(f'current_room.{direction}_to'):
                    new_y = current_room.y + delta_y
                    if not size_y > new_y >= 0:
                        continue

                    new_x = current_room.x + delta_x
                    if not size_x > new_x >= 0:
                        continue

                    if not self.grid[new_y][new_x]:
                        next_room = Room(title=make_name(), x=new_x, y=new_y)
                        next_room.save()
                        self.grid[new_y][new_x] = next_room.id
                        current_room.connect_rooms(next_room, direction)
                        queue.append(next_room)
                        self.room_count += 1

    def print_rooms(self):
        """
        Print the rooms in room_grid in ascii characters.
        """

        # Add top border
        string = "# " * ((3 + self.width * 5) // 2) + "\n"

        for row in self.grid:
            # PRINT NORTH CONNECTION ROW
            string += "#"
            for room in row:
                if room and Room.objects.filter(id=room)[0].n_to != 0:
                    string += "  |  "
                else:
                    string += "     "
            string += "#\n"
            # PRINT ROOM ROW
            string += "#"
            for room in row:
                if room and Room.objects.filter(id=room)[0].w_to != 0:
                    string += "-"
                else:
                    string += " "
                if room is not None:
                    string += f"{Room.objects.filter(id=room)[0].id}".zfill(3)
                else:
                    string += "   "
                if room and Room.objects.filter(id=room)[0].e_to != 0:
                    string += "-"
                else:
                    string += " "
            string += "#\n"
            # PRINT SOUTH CONNECTION ROW
            string += "#"
            for room in row:
                if room and Room.objects.filter(id=room)[0].s_to != 0:
                    string += "  |  "
                else:
                    string += "     "
            string += "#\n"

        # Add bottom border
        string += "# " * ((3 + self.width * 5) // 2) + "\n"

        # Print string
        print(string)

    def seed_items(self, num_chest=5):
        # pick a chest to put the treasure in

        for i in range(num_chest):
            # create chest/key pairs
            name = adj_noun()
            key_name = "Key of the " + name
            chest_name = "Chest of the " + name
            k = Item(name=key_name,
                     description="Maybe it opens a chest!",
                     room=Room.objects.filter(id=random.randint(1, self.room_count))[0],
                     is_key=True)
            c = Container(name=chest_name,
                          description="Maybe there's treasure inside!",
                          key=k,
                          room=Room.objects.filter(id=random.randint(1, self.room_count))[0])
            k.save()
            c.save()

        # put the treasure in the lucky chest
        # Choose lucky number after making all keys and chests to keep primary keys between them equal.
        lucky_chest_number = random.randint(1, num_chest)
        the_treasure = Item(name="The Treasure",
                            description="That thing you want",
                            container=Container.objects.filter(id=lucky_chest_number)[0])
        the_treasure.save()


w = World()
num_rooms = 100
width = 12
height = 12
w.generate_rooms(width, height, num_rooms)
w.print_rooms()
w.seed_items(num_chest=10)

players = Player.objects.all()
start_room = random.randint(1, w.room_count)
for p in players:
    p.currentRoom = start_room
    p.save()

print('World Created!! Good Job!')
print(f"\n\nWorld\n  height: {height}\n  width: {width},\n  num_rooms: {w.room_count}\n")
