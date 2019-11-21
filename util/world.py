# """Create a game world of interconnected rooms to navigate.
# Scatter treasure chests and keys throughout the world.
# Place treasure in one chest as the goal of the game."""

from adventure.models import Item, Container, Room, Player
from .name_generation import make_name, adj_noun, make_name_desc
from collections import deque
import random


class World:
    """Define a game world with rooms connected on a 2D grid.

    Rooms are stored as their integer id, otherwise, grid members are None.

    :var width: The width of the grid, in number of rooms.
    :var height: The height of the grid, in number of rooms.
    :var num_rooms: The number of rooms to add.
    :var num_chests: The number of chests to hide.

    """

    def __init__(self, width: int, height: int, num_rooms: int, num_chests: int):
        self.width = width
        self.height = height
        self.num_rooms = num_rooms
        self.num_chests = num_chests
        self.grid = None
        self.room_count = 1

    def generate_rooms(self):
        """Make a series of interconnected hallways radiating from a central point."""
        # Initialize the grid
        self.grid = [None] * self.height
        for i in range(len(self.grid)):
            self.grid[i] = [None] * self.width

        # Start in the middle of the grid.
        mid_y = (self.height // 2)
        mid_x = (self.width // 2) - 1

        # Make the first room to add to our world. Place it in the center of the grid.
        name, desc = make_name_desc(1)
        first = Room(title=name,
                     description=desc,
                     x=mid_x,
                     y=mid_y)
        first.save()
        self.grid[first.y][first.x] = first.id

        # Place room number one in a queue.
        queue = deque()
        queue.append(first)

        # Keep making rooms until we've reached our desired number.
        while self.room_count < self.num_rooms:
            current_room = queue.popleft()

            # Connect another room to the current one in each available direction.
            for direction, delta_x, delta_y in zip(['n', 'w', 's', 'e'], [0, 1, 0, -1], [-1, 0, 1, 0]):

                # If there's already a room this direction, keep going.
                if not eval(f'current_room.{direction}_to'):

                    # Check that we're still on the grid.
                    new_y = current_room.y + delta_y
                    if not self.height > new_y >= 0:
                        continue

                    new_x = current_room.x + delta_x
                    if not self.width > new_x >= 0:
                        continue

                    # Check that this grid space is open.
                    if not self.grid[new_y][new_x]:
                        # Make a new room, save it, connect it to the current room,
                        # and add it into the queue so we can add more rooms to it.
                        name, desc = make_name_desc(Room.objects.count() + 1)
                        next_room = Room(title=name,
                                         description=desc,
                                         x=new_x,
                                         y=new_y)
                        next_room.save()
                        self.grid[new_y][new_x] = next_room.id
                        current_room.connect_rooms(next_room, direction)
                        queue.append(next_room)
                        self.room_count += 1
        for row in self.grid:
            row.reverse()

    def print_rooms(self):
        """Print the rooms in self.grid in ascii characters."""
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
        """Create chests and their keys in pairs with matching id."""
        for i in range(self.num_chests):
            # Make a hilarious name for the pair.
            name = adj_noun()
            key_name = "Key of the " + name
            chest_name = "Chest of the " + name
            k = Item(name=key_name,
                     description=f"Maybe it opens the {chest_name}?!",
                     room=None)
            c = Container(name=chest_name,
                          description="Maybe there's treasure inside!",
                          key=k,
                          room=None)
            k.save()
            c.save()


def seed_items(num_chests, num_rooms):
    """Move keys and chests to random rooms.
    Put the treasure in the lucky chest.
    Remove keys from players.
    """
    # Create the required number of chests and keys.
    for i in range(1, num_chests):
        key = Item.objects.get(id=i)
        chest = Container.objects.get(id=i)
        key.player = None
        chest.player = None
        key.room = Room.objects.get(id=random.randint(1, num_rooms))
        chest.room = Room.objects.get(id=random.randint(1, num_rooms))
        key.save()
        chest.save()

    # Creat a treasure and hide it in a random chest.
    lucky_chest_number = random.randint(1, num_chests)
    the_treasure = Item(name="The Treasure",
                        description="That thing you want",
                        container=Container.objects.get(id=lucky_chest_number))
    the_treasure.save()


def seed_players(num_rooms):
    """Move all players to a random room to start the hunt again."""
    start_room = random.randint(1, num_rooms)
    for player in Player.objects.all():
        player.current_room = start_room
        player.save()


def main():
    """Run script to populate database with rooms and items."""
    num_rooms = 10
    width = 5
    height = 5
    num_chest = 5

    w = World(width, height, num_rooms, num_chest)
    w.generate_rooms()
    w.print_rooms()
    w.create_items()
    seed_items(num_chests=num_chest,
               num_rooms=num_rooms)
    seed_players(num_rooms=num_rooms)

    print('World Created!! Good Job!')
    print(f"\n\nWorld\n  height: {height}\n  width: {width},\n  num_rooms: {w.room_count}\n")


if __name__ == "__main__":
    main()
