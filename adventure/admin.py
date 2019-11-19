from django.contrib import admin
from .models import Item, Container, Room, Player

# Register your models here.
admin.site.register((Item, Container, Room, Player))