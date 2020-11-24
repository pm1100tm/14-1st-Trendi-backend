import json

from django.views     import View
from django.http      import JsonResponse

from user.models    import User 
from product.models import Product


class SearchView(View):
    @query_debugger
    def get(self, request):
        product = request.GET['result']
        products = Product.objects.select_related('seller','delivery','sale').filter(title__contains=product)
        
        if not products.exists():
            return JsonResponse({'MESSAGE':'NO_RESULT!'}, status = 400)

        product_lists = [{
            'title'            : product.title,
            'thumb_image'      : product.thumb_image_url,
            'discounted_price' : int(round(float(product.price) * float(1-product.sale.sale_ratio),-2)),
            'price'            : product.price,
            'seller'           : product.seller.name,
            'delivery'         : product.delivery.delivery_type,
            'sale'             : str(int(product.sale.sale_ratio * 100)) + '%'
            } for product in products]

        number_of_results = Product.objects.filter(title__contains=product).count()

        return JsonResponse({'number of results': number_of_results, 'results': product_lists}, status = 200)
