from django.contrib import admin
from .models import CustomUser,Collection,ArtSupply,Reviews,CollectionRequest,ArtSupplyRequest
# Register your models here.

admin.site.register(CustomUser)
admin.site.register(Collection)
admin.site.register(ArtSupply)
admin.site.register(CollectionRequest)
admin.site.register(Reviews)
admin.site.register(ArtSupplyRequest)