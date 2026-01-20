from django.contrib import admin
from .models import Cart, CartItem

class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    # 'id' എന്ന് ഇവിടെ നൽകുന്നതോടെ UUID അഡ്മിൻ പാനലിൽ നേരിട്ട് കാണാം
    list_display = ['id', 'user', 'created_at'] 
    inlines = [CartItemInline]