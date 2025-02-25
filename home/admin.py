from django.contrib import admin
from .models import * 

class OrderedAdmin(admin.StackedInline):
    model = Ordered
    extra = 0
    readonly_fields = ['product', 'quantity', 'orderedby','size']

class OrderedByAdmin(admin.ModelAdmin):
    list_display = ['customer', 'order_date', 'process_status']
    inlines = [OrderedAdmin]
    readonly_fields = ['user', 'address', 'date']

    def customer(self, obj):
        return obj.user.username  # Assuming you have a user field in OrderedBy model

    def order_date(self, obj):
        return obj.date
    
    def process_status(self, obj):
        return "✅" if obj.process else "❌"

admin.site.register(OrderedBy, OrderedByAdmin)



# Register your models here.
admin.site.register(Contact)
admin.site.register(Product)
admin.site.register(Category)

