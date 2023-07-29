from django.views import generic

from .models import Product


class ProductListView(generic.ListView):
    model = Product
    template_name = 'products/products_list.html'
    context_object_name = 'products'
    queryset = Product.objects.filter(active=True)
