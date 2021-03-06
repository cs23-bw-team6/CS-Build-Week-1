from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
import uuid


class Item(models.Model):
    # !!-- Be sure to add attributes to dictionary if adding here --!!
    name = models.CharField(max_length=50, default="Item Name")
    description = models.CharField(max_length=50, default='Item Description')
    container = models.ForeignKey('Container',
                                  on_delete=models.CASCADE,
                                  blank=True,
                                  null=True)
    room = models.ForeignKey('Room',
                             on_delete=models.CASCADE,
                             blank=True,
                             null=True)
    player = models.ForeignKey('Player',
                               on_delete=models.CASCADE,
                               blank=True,
                               null=True)

    def __str__(self):
        return f"{self.name}\n{self.description}"

    def dictionary(self):
        return {'name': self.name,
                'description': self.description,
                'container': self.container_id,
                'room': self.room_id,
                'player': self.player_id}


class Container(models.Model):
    # !!-- Be sure to add attributes to dictionary if adding here --!!
    name = models.CharField(max_length=50, default="Container Name")
    description = models.CharField(max_length=50, default='Container Description')
    room = models.ForeignKey('Room',
                             on_delete=models.CASCADE,
                             blank=True,
                             null=True)
    key = models.OneToOneField('Item',
                               on_delete=models.CASCADE,
                               blank=True,
                               null=True,
                               related_name='key_to')

    def dictionary(self):
        return {'name': self.name,
                'description': self.description,
                'room': self.room_id,
                'key': self.key_id,
                'item': [item.id for item in Item.objects.filter(container=self.id)]}


class Room(models.Model):
    # !!-- Be sure to add attributes to dictionary if adding here --!!
    title = models.CharField(max_length=50, default="DEFAULT TITLE")
    description = models.CharField(max_length=500, default="DEFAULT DESCRIPTION")
    n_to = models.IntegerField(default=0)
    s_to = models.IntegerField(default=0)
    e_to = models.IntegerField(default=0)
    w_to = models.IntegerField(default=0)
    x = models.IntegerField(default=0)
    y = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.title}\n{self.description}"

    def dictionary(self):
        return {'title': self.title,
                'description': self.description,
                'items': {item.id: item.dictionary() for item in Item.objects.filter(room=self.id)},
                'containers': {container.id: container.dictionary()
                               for container in Container.objects.filter(room=self.id)},
                'players': {player.id: player.dictionary() for player in Player.objects.filter(current_room=self.id)},
                'n_to': self.n_to,
                's_to': self.s_to,
                'e_to': self.e_to,
                'w_to': self.w_to,
                'x': self.x,
                'y': self.y}

    def connect_rooms(self, connecting_room, direction):
        """Connect two rooms in the given direction."""
        reverse_dirs = {"n": "s", "s": "n", "e": "w", "w": "e"}
        reverse_dir = reverse_dirs[direction]
        setattr(self, f"{direction}_to", connecting_room.id)
        setattr(connecting_room, f"{reverse_dir}_to", self.id)
        self.save()
        connecting_room.save()

    def player_names(self, current_player_id):
        """List the names of other players in the current room."""
        return [p.user.username for p in Player.objects.filter(current_room=self.id) if p.id != int(current_player_id)]

    def player_UUIDs(self, current_player_id):
        """List the uuid of other players in the room."""
        return [p.uuid for p in Player.objects.filter(current_room=self.id) if p.id != int(current_player_id)]


class Player(models.Model):
    # !!-- Be sure to add attributes to dictionary if adding here --!!
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    current_room = models.IntegerField(default=0)
    uuid = models.UUIDField(default=uuid.uuid4, unique=True)
    score = models.IntegerField(default=0)
    high_score = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_login}"

    def dictionary(self):
        return {'user': self.user.username,
                'current_room': self.current_room,
                'items': [item.id for item in Item.objects.filter(player=self)],
                'score': self.score,
                'high_score': self.high_score,
                'uuid': self.uuid}

    def initialize(self):
        """Set the current room to the first room's id."""
        if self.current_room == 0:
            self.current_room = Room.objects.first().id
            self.save()

    def room(self):
        """Return the player's current Room object."""
        try:
            return Room.objects.get(id=self.current_room)
        except Room.DoesNotExist:
            self.initialize()
            return self.room()


@receiver(post_save, sender=User)
def create_user_player(sender, instance, created, **kwargs):
    if created:
        Player.objects.create(user=instance)
        Token.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_player(sender, instance, **kwargs):
    instance.player.save()





