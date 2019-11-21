from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
# from pusher import Pusher
from django.http import JsonResponse
from decouple import config
from django.contrib.auth.models import User
from .models import *
from rest_framework.decorators import api_view
import json
from util.world import World

# instantiate pusher
# pusher = Pusher(app_id=config('PUSHER_APP_ID'),
#                 key=config('PUSHER_KEY'),
#                 secret=config('PUSHER_SECRET'),
#                 cluster=config('PUSHER_CLUSTER'))

@csrf_exempt
@api_view(["GET"])
def rooms(request):
    rooms_ = {room.id: room.dictionary() for room in Room.objects.all()}
    return JsonResponse({'rooms': rooms_})


@csrf_exempt
@api_view(["GET"])
def initialize(request):
    user = request.user
    player = user.player
    player_id = player.id
    uuid = player.uuid
    room = player.room()
    players = room.player_names(player_id)
    return JsonResponse(
        {'uuid': uuid,
         'name': player.user.username,
         'title': room.title,
         'description': room.description,
         'items': [item.name for item in room.item_set.all()],
         'containers': [container.name for container in room.container_set.all()],
         'players': players}, safe=True)


@csrf_exempt
@api_view(["POST"])
def use_item(request):
    player = request.user.player
    data = json.loads(request.body)
    item = Item.objects.get(name=data['item'])
    if item.player == player:
        chest_name = "Chest of the" + item.name[10:]
        chest = Container.objects.get(name=chest_name)

        chest_item = chest.item_set.all()[0]
        chest_item.locked = False
        chest_item.player = player
        chest_item.container = None
        chest_item.save()
        return JsonResponse({"name": player.user.username,
                             'item': chest_item.name,
                             'description': chest_item.description,
                             'error_msg': ""})
    return JsonResponse({"error_msg": "You don't have that item."})


@csrf_exempt
@api_view(["POST"])
def get_item(request):
    player = request.user.player
    data = json.loads(request.body)
    item = Item.objects.get(name=data['item'])
    if item.room:
        if item.is_key:
            item.room = None
            item.player = player
            player.save()
            item.save()
            return JsonResponse({'name': player.user.username,
                                 'item': item.name,
                                 'description': item.description,
                                 'error_msg': "Error in get_item"},
                                safe=True)
        return JsonResponse({'error_msg': 'Chests are too heavy.'},
                            safe=True)
    return JsonResponse({'error_msg': "I don't see that here"})


@csrf_exempt
@api_view(["POST"])
def move(request):
    dirs = {"n": "north", "s": "south", "e": "east", "w": "west"}
    reverse_dirs = {"n": "south", "s": "north", "e": "west", "w": "east"}
    player = request.user.player
    player_id = player.id
    player_uuid = player.uuid
    data = json.loads(request.body)
    direction = data['direction']
    room = player.room()
    next_room_id = None
    if direction == "n":
        next_room_id = room.n_to
    elif direction == "s":
        next_room_id = room.s_to
    elif direction == "e":
        next_room_id = room.e_to
    elif direction == "w":
        next_room_id = room.w_to
    if next_room_id and next_room_id > 0:
        next_room = Room.objects.get(id=next_room_id)
        player.current_room = next_room_id
        player.save()

        # Below is all for the pusher stuff.

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
             'items': [item.name for item in room.item_set.all()],
             'containers': [container.name for container in room.container_set.all()],
             'players': {player.id: player.dictionary() for player in Player.objects.filter(current_room=next_room_id)},
             'error_msg': ""},
            safe=True)
    else:
        return JsonResponse(
            {'name': player.user.username,
             'title': room.title,
             'description': room.description,
             'items': [item.name for item in room.item_set.all()],
             'containers': [container.name for container in room.container_set.all()],
             'players': {player.id: player.dictionary() for player in Player.objects.filter(current_room=room.id)},
             'error_msg': "You cannot move that way."},
            safe=True)


@csrf_exempt
@api_view(["POST"])
def say(request):
    # IMPLEMENT
    return JsonResponse({'error': "Not yet implemented"}, safe=True, status=500)
