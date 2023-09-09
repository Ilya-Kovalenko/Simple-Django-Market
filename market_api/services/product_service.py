from market_api.models import Product


class ProductService:
    @staticmethod
    def add_product(name: str, manufacturer: str, price: float) -> None:
        Product.objects.create(name=name, manufacturer=manufacturer, price=price)

    @staticmethod
    def get_products(request):
        name_filter = request.GET.get("name", None)
        manufacturer_filter = request.GET.get("manufacturer", None)
        price_min_filter = request.GET.get("price_min", None)
        price_max_filter = request.GET.get("price_max", None)
        sorting = request.GET.get("sorting", None)

        queryset = Product.objects.all()

        if manufacturer_filter:
            queryset = queryset.filter(name=name_filter)

        if manufacturer_filter:
            queryset = queryset.filter(manufacturer=manufacturer_filter)

        if price_min_filter:
            queryset = queryset.filter(price__gte=price_min_filter)

        if price_max_filter:
            queryset = queryset.filter(price__lte=price_max_filter)

        match sorting:
            case "price_up":
                queryset = queryset.order_by("price")
            case "price_down":
                queryset = queryset.order_by("-price")
            case "name_up":
                queryset = queryset.order_by("name")
            case "name_down":
                queryset = queryset.order_by("-name")
            case _:
                pass

        return queryset
