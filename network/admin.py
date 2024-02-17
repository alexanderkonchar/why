from django.contrib import admin

from network.models import User, Follower, Post

# Register your models here.
admin.site.register(User)
admin.site.register(Follower)
admin.site.register(Post)
