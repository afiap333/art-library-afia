from django.contrib import admin
from .models import CustomUser,Collection,ArtSupply,Reviews
# Register your models here.

admin.site.register(CustomUser)
admin.site.register(Collection)
admin.site.register(ArtSupply)
admin.site.register(Reviews)