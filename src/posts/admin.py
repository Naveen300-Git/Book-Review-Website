from django.contrib import admin
from .models import Post,Post_Like,Review,Review_Like
# Register your models here.
admin.site.register(Post)
admin.site.register(Post_Like)
admin.site.register(Review)
admin.site.register(Review_Like)
