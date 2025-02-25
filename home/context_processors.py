from .models import Cart, OrderedBy, Category
from django.db.models import Sum, Count
from django.core.exceptions import ObjectDoesNotExist

def base_context(request):
    if request.user.is_authenticated:
        cart_count = Cart.objects.filter(user=request.user).count()
        order_count = OrderedBy.objects.filter(user=request.user, process=False).count()
        categories = Category.objects.all()
    else:
        cart_count = 0
        order_count = 0
        categories = []

    return {
        'cart_count': cart_count,
        'order_count': order_count,
        'categories': categories,
    }
