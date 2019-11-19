# Sample Python code that can be used to generate rooms in
# a zig-zag pattern.
#
# You can modify generate_rooms() to create your own
# procedural generation algorithm and use print_rooms()
# to see the world.
from adventure.models import Item, Container, Room
from .name_generation import make_name
from collections import deque


class World:
    def __init__(self):
        self.grid = None
        self.width = 0
        self.height = 0

    def generate_rooms(self, size_x, size_y, num_rooms):
        # Initialize the grid
        self.grid = [None] * size_y
        self.width = size_x
        self.height = size_y
        for i in range(len(self.grid)):
            self.grid[i] = [None] * size_x

        mid_y = size_y // 2
        mid_x = size_x // 2

        first = Room(title=make_name(), x=mid_x, y=mid_y)
        first.save()
        self.grid[first.y][first.x] = first.id
        queue = deque()
        queue.append(first)
        print('I am first', first.id)
        room_count = 1
        while room_count < num_rooms:
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
                        room_count += 1

    def print_rooms(self):
        """
        Print the rooms in room_grid in ascii characters.
        """

        # Add top border
        string = "# " * ((3 + self.width * 5) // 2) + "\n"

        # The console prints top to bottom but our array is arranged
        # bottom to top.
        #
        # We reverse it so it draws in the right direction.
        reverse_grid = list(self.grid)  # make a copy of the list
        reverse_grid.reverse()
        for row in reverse_grid:
            # PRINT NORTH CONNECTION ROW
            string += "#"
            for room in row:
                if room is not None and Room.objects.filter(id=room)[0].n_to is not None:
                    string += "  |  "
                else:
                    string += "     "
            string += "#\n"
            # PRINT ROOM ROW
            string += "#"
            for room in row:
                if room is not None and Room.objects.filter(id=room)[0].w_to is not None:
                    string += "-"
                else:
                    string += " "
                if room is not None:
                    string += f"{Room.objects.filter(id=room)[0].id}".zfill(3)
                else:
                    string += "   "
                if room is not None and Room.objects.filter(id=room)[0].e_to is not None:
                    string += "-"
                else:
                    string += " "
            string += "#\n"
            # PRINT SOUTH CONNECTION ROW
            string += "#"
            for room in row:
                if room is not None and Room.objects.filter(id=room)[0].s_to is not None:
                    string += "  |  "
                else:
                    string += "     "
            string += "#\n"

        # Add bottom border
        string += "# " * ((3 + self.width * 5) // 2) + "\n"

        # Print string
        print(string)


w = World()
num_rooms = 15
width = 15
height = 15
w.generate_rooms(width, height, num_rooms)
w.print_rooms()

print(f"\n\nWorld\n  height: {height}\n  width: {width},\n  num_rooms: {num_rooms}\n")
