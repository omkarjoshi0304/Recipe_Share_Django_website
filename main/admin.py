from django.contrib import admin
from .models import Recipe
from .models import ContactMessage
from .models import ItemCategory, MarketplaceItem, ItemReview, ItemOffer

admin.site.register(ItemCategory)
admin.site.register(MarketplaceItem)
admin.site.register(ItemReview)
admin.site.register(ItemOffer)
admin.site.register(Recipe)
admin.site.register(ContactMessage)



# Register your models here.
