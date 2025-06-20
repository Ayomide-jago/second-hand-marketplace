from django.contrib import admin
from .models import ItemImage, Item, Category,UserProfile,Message,UserRating,Favorite



# Register your models here.
admin.site.register(ItemImage)
admin.site.register(Item)
admin.site.register(Category)
admin.site.register(UserProfile)
admin.site.register(Message)
admin.site.register(UserRating)
admin.site.register(Favorite)
