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
    is_light = models.BooleanField(default=False)
    weight = models.IntegerField(default=1)
    seen = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name}\n{self.description}"

    def dictionary(self):
        return {'name': self.name,
                'description': self.description,
                'is_light': self.is_light,
                'weight': self.weight,
                'seen': self.seen}


class Container(models.Model):
    # !!-- Be sure to add attributes to dictionary if adding here --!!
    name = models.CharField(max_length=50, default="Container Name")
    description = models.CharField(max_length=50, default='Container Description')
    weight = models.IntegerField(default=50)
    seen = models.BooleanField(default=False)

    key = models.BooleanField(default=None)
    locked = models.BooleanField(default=True)
    items = models.ManyToManyField('Item')

    def dictionary(self):
        return {'name': self.name,
                'description': self.description,
                'weight': self.weight,
                'seen': self.seen,
                'key': self.key,
                'locked': self.locked,
                'items': {item.id: item.dictionary() for item in self.items.all()}
        }


class Room(models.Model):
    # !!-- Be sure to add attributes to dictionary if adding here --!!
    title = models.CharField(max_length=50, default="DEFAULT TITLE")
    description = models.CharField(max_length=500, default="DEFAULT DESCRIPTION")
    items = models.ManyToManyField('Item')
    n_to = models.IntegerField(default=0)
    s_to = models.IntegerField(default=0)
    e_to = models.IntegerField(default=0)
    w_to = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.title}\n{self.description}"

    def dictionary(self):
        return {'title': self.title,
                'description': self.description,
                'items': {item.id: item.dictionary() for item in self.items.all()},
                'n_to': self.n_to,
                's_to': self.s_to,
                'e_to': self.e_to,
                'w_to': self.w_to}

    def connect_rooms(self, destination_room, direction):
        destination_room_id = destination_room.id
        try:
            destination_room = Room.objects.get(id=destination_room_id)
        except Room.DoesNotExist:
            print("That room does not exist")
        else:
            if direction == "n":
                self.n_to = destination_room_id
            elif direction == "s":
                self.s_to = destination_room_id
            elif direction == "e":
                self.e_to = destination_room_id
            elif direction == "w":
                self.w_to = destination_room_id
            else:
                print("Invalid direction")
                return
            self.save()

    def add_item(self, item):
        self.items.add(item)

    def player_names(self, current_player_id):
        return [p.user.username for p in Player.objects.filter(currentRoom=self.id) if p.id != int(current_player_id)]

    def player_UUIDs(self, current_player_id):
        return [p.uuid for p in Player.objects.filter(currentRoom=self.id) if p.id != int(current_player_id)]


class Player(models.Model):
    # !!-- Be sure to add attributes to dictionary if adding here --!!
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    current_room = models.IntegerField(default=0)
    items = models.ManyToManyField('Item')
    uuid = models.UUIDField(default=uuid.uuid4, unique=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_login}"

    def dictionary(self):
        return {'user': self.user,
                'current_room': self.current_room,
                'item': {item.id: item.dictionary() for item in self.items.all()},
                'uuid': self.uuid}

    def initialize(self):
        if self.current_room == 0:
            self.current_room = Room.objects.first().id
            self.save()

    def room(self):
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





