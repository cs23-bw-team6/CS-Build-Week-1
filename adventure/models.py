from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
import uuid


class Room(models.Model):
    title = models.CharField(max_length=50, default="DEFAULT TITLE")
    description = models.CharField(max_length=500, default="DEFAULT DESCRIPTION")
    n_to = models.IntegerField(default=0)
    s_to = models.IntegerField(default=0)
    e_to = models.IntegerField(default=0)
    w_to = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.title}\n{self.description}"

    def __dict__(self):
        return {'title': self.title,
                'description': self.description,
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

    def player_names(self, current_player_ID):
        return [p.user.username for p in Player.objects.filter(currentRoom=self.id) if p.id != int(current_player_ID)]

    def player_UUIDs(self, current_player_ID):
        return [p.uuid for p in Player.objects.filter(currentRoom=self.id) if p.id != int(current_player_ID)]


class Player(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    currentRoom = models.IntegerField(default=0)
    uuid = models.UUIDField(default=uuid.uuid4, unique=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_login}"

    def initialize(self):
        if self.currentRoom == 0:
            self.currentRoom = Room.objects.first().id
            self.save()

    def room(self):
        try:
            return Room.objects.get(id=self.currentRoom)
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





