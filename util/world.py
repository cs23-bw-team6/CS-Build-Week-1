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
    def __init__(self, size_x, size_y, num_rooms, num_chests):
        self.grid = None
        self.width = size_x
        self.height = size_y
        self.room_count = 1
        self.num_rooms = num_rooms
        self.num_chests = num_chests

    def generate_rooms(self):
        # Initialize the grid
        self.grid = [None] * self.height
        for i in range(len(self.grid)):
            self.grid[i] = [None] * self.width

        mid_y = (self.height // 2)
        mid_x = (self.width // 2) - 1

        first = Room(title=make_name(), x=mid_x, y=mid_y)
        first.save()
        self.grid[first.y][first.x] = first.id
        queue = deque()
        queue.append(first)
        while self.room_count < num_rooms:
            current_room = queue.popleft()
            for direction, delta_x, delta_y in zip(['n', 'w', 's', 'e'], [0, 1, 0, -1], [-1, 0, 1, 0]):
                if not eval(f'current_room.{direction}_to'):
                    new_y = current_room.y + delta_y
                    if not self.height > new_y >= 0:
                        continue

                    new_x = current_room.x + delta_x
                    if not self.width > new_x >= 0:
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
            row = list(reversed(row))
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

    def create_items(self):
        # pick a chest to put the treasure in

        for i in range(self.num_chests):
            # create chest/key pairs
            name = adj_noun()
            key_name = "Key of the " + name
            chest_name = "Chest of the " + name
            k = Item(name=key_name,
                     description=f"Maybe it opens the {chest_name}!",
                     room=None,
                     is_key=True)
            c = Container(name=chest_name,
                          description="Maybe there's treasure inside!",
                          key=k,
                          room=None)
            k.save()
            c.save()

    def seed_items(self):
        """Add keys and chests to random rooms.
        Put the treasure in the lucky chest.
        """
        for i in range(1, self.num_chests):
            key = Item.objects.get(id=i)
            chest = Container.objects.get(id=i)
            key.room = Room.objects.get(id=random.randint(1, self.num_rooms))
            chest.room = Room.objects.get(id=random.randint(1, self.num_rooms))
            key.save()
            chest.save()

        lucky_chest_number = random.randint(1, self.num_chests)
        the_treasure = Item(name="The Treasure",
                            description="That thing you want",
                            container=Container.objects.get(id=lucky_chest_number))
        the_treasure.save()

    def seed_players(self):
        players = Player.objects.all()
        start_room = random.randint(1, self.num_rooms)
        for p in players:
            p.currentRoom = start_room
            p.save()


num_rooms = 10
width = 5
height = 5
num_chest = 5

w = World(width, height, num_rooms, num_chest)
w.generate_rooms()
w.print_rooms()
w.create_items()
w.seed_items()
w.seed_players()

print('World Created!! Good Job!')
print(f"\n\nWorld\n  height: {height}\n  width: {width},\n  num_rooms: {w.room_count}\n")
