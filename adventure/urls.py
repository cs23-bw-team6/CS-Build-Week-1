from django.conf.urls import url
from . import api

urlpatterns = [
    url('spawn', api.spawn),
    url('use_item', api.use_item),
    url('get_item', api.get_item),
    url('rooms', api.rooms),
    url('init', api.initialize),
    url('move', api.move),
    url('say', api.say),
]