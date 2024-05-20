from django.contrib import admin

# Register your models here.
from .models import StreamPlatform , Watchlist , Review

admin.site.register(StreamPlatform)
admin.site.register(Watchlist)
admin.site.register(Review)