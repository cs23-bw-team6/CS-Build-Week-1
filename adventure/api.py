from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
# from pusher import Pusher
from django.http import JsonResponse
from decouple import config
from django.contrib.auth.models import User
from util.world import seed_players, seed_items
from .models import *
from rest_framework.decorators import api_view
import json


# instantiate pusher
# pusher = Pusher(app_id=config('PUSHER_APP_ID'),
#                 key=config('PUSHER_KEY'),
#                 secret=config('PUSHER_SECRET'),
#                 cluster=config('PUSHER_CLUSTER'))

# @csrf_exempt
@api_view(["GET"])
def spawn(request):
    """Move all players to a random room and scatter keys and chests about dungeon."""
    seed_items(num_rooms=Room.objects.count(), num_chests=Container.objects.count())
    seed_players(num_rooms=Room.objects.count())
    return JsonResponse({"World": "re-spawned."}, safe=True)


# @csrf_exempt
@api_view(["GET"])
def rooms(request):
    """Return dict of room ids and room dicts."""
    rooms_ = {room.id: room.dictionary() for room in Room.objects.all()}
    return JsonResponse({'rooms': rooms_}, safe=True)


# @csrf_exempt
@api_view(["GET"])
def initialize(request):
    """Place an active user in the map.

    Reset player score to 0.
    """
    user = request.user
    print('user', user)
    player = user.player
    player_id = player.id
    uuid = player.uuid
    room = player.room()
    player.score = 0
    player.save()
    return JsonResponse(
        {'uuid': uuid,
         'name': player.user.username,
         'title': room.title,
         'description': room.description,
         'items': [item.name for item in room.item_set.all()],
         'containers': [container.name for container in room.container_set.all()],
         'players': room.player_names(player_id)},
        safe=True)


# @csrf_exempt
@api_view(["POST"])
def use_item(request):
    """Use a key to open a chest.

    Keys only work in the room the chest is in.
    If the chest has the treasure, we have a winner.
    """
    player = request.user.player
    data = json.loads(request.body)
    item = Item.objects.get(name=data['item'])

    # Make sure the player has this item.
    if item.player == player:
        chest = Container.objects.get(id=item.id)

        # Make sure the chest is in this room.
        if player.current_room == chest.room.id:

            # Check if there's an item. If so, we have our winner!
            if len(chest.item_set.all()) > 0:
                player.score += 1

                # Update high score if necessary.
                if player.score > player.high_score:
                    player.high_score = player.score
                    player.save()
                    return JsonResponse({'name': player.user.username,
                                         'score': player.score,
                                         'high_score': player.high_score,
                                         'msg': 'You won!!\nNew Personal High Score!!'},
                                        safe=True)
                player.save()
                return JsonResponse({'name': player.user.username,
                                     'score': player.score,
                                     'high_score': player.high_score,
                                     'msg': 'You won!!'},
                                    safe=True)

            return JsonResponse({"name": player.user.username,
                                 'score': player.score,
                                 'high_score': player.high_score,
                                 'msg': 'Keep searching for the treasure!'},
                                safe=True)

        return JsonResponse({"name": player.user.username,
                             'score': player.score,
                             'high_score': player.high_score,
                             'msg': 'The chest for this key is not in here!'},
                            safe=True)

    return JsonResponse({"error_msg": "You don't have that item."}, safe=True)


# @csrf_exempt
@api_view(["POST"])
def get_item(request):
    """Pick up an item in the current room."""
    player = request.user.player
    data = json.loads(request.body)
    item = Item.objects.get(name=data['item'])
    # Check that the item is in the player's current room.
    if item.room:
        item.room = None
        item.player = player
        item.save()
        return JsonResponse({'name': player.user.username,
                             'item': item.name,
                             'description': item.description,
                             'error_msg': "Error in get_item"},
                            safe=True)
    return JsonResponse({'error_msg': "I don't see that here"}, safe=True)


# @csrf_exempt
@api_view(["POST"])
def move(request):
    """Move the player in the given direction.

    Return an error message if no passage exists in that direction.
    Contains logic for Pusher messaging.
    """
    print(request.user.player)
    # dirs = {"n": "north", "s": "south", "e": "east", "w": "west"}
    # reverse_dirs = {"n": "south", "s": "north", "e": "west", "w": "east"}
    player = request.user.player
    # player_id = player.id
    # player_uuid = player.uuid
    data = json.loads(request.body)
    direction = data['direction']
    room = player.room()

    next_room_id = None
    if direction == "n":
        next_room_id = room.n_to
    elif direction == "s":
        next_room_id = room.s_to
    elif direction == "w":
        next_room_id = room.e_to
    elif direction == "e":
        next_room_id = room.w_to
    if next_room_id:
        next_room = Room.objects.get(id=next_room_id)
        player.current_room = next_room_id
        player.save()

        # Below is all pusher stuff.

        # current_player_uui_ds = room.player_UUIDs(player_id)
        # next_player_uui_ds = next_room.player_UUIDs(player_id)
        # for p_uuid in current_player_uui_ds:
        #     pusher.trigger(f'p-channel-{p_uuid}', u'broadcast',
        #                    {'message': f'{player.user.username} has walked {dirs[direction]}.'})
        # for p_uuid in next_player_uui_ds:
        #     pusher.trigger(f'p-channel-{p_uuid}', u'broadcast',
        #                    {'message': f'{player.user.username} has entered from the {reverse_dirs[direction]}.'})

        return JsonResponse(
            {'name': player.user.username,
             'title': next_room.title,
             'description': next_room.description,
             'items': [item.name for item in next_room.item_set.all()],
             'containers': [container.name for container in next_room.container_set.all()],
             'players': next_room.player_names(player.id),
             'error_msg': ""},
            safe=True)
    else:
        return JsonResponse(
            {'name': player.user.username,
             'title': room.title,
             'description': room.description,
             'items': [item.name for item in room.item_set.all()],
             'containers': [container.name for container in room.container_set.all()],
             'players': room.player_names(player.id),
             'error_msg': "You cannot move that way."},
            safe=True)


# @csrf_exempt
@api_view(["POST"])
def say(request):
    # IMPLEMENT
    return JsonResponse({'error': "Not yet implemented"}, safe=True, status=500)
