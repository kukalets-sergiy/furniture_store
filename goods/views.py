from django.core.paginator import Paginator
from django.shortcuts import get_list_or_404, get_object_or_404, render

from goods.models import Products
from goods.utils import q_search


# The function accepts an HTTP request and an optional category_slug parameter
def catalog(request, category_slug=None):
    # Get the page number from the GET parameters, defaulting to 1
    page = request.GET.get('page', 1)
    # Get the 'on_sale' parameter from the GET parameters
    on_sale = request.GET.get('on_sale', None)
    # Get the 'order_by' parameter from the GET parameters
    order_by = request.GET.get('order_by', None)
    # Get the 'q' (search query) parameter from the GET parameters
    query = request.GET.get('q', None)

    # If category_slug equals "all", select all products
    if category_slug == "all":
        goods = Products.objects.all()
    elif query:
        # If there's a search query, perform a search for products based on that query
        goods = q_search(query)
    else:
        # Otherwise, select products that belong to the specified category
        goods = get_list_or_404(Products.objects.filter(category__slug=category_slug))

    # Ensure goods is a QuerySet for proper filtering and ordering
    if not isinstance(goods, Products.objects.all().__class__):
        goods = Products.objects.filter(id__in=[product.id for product in goods])

    # If the 'on_sale' parameter is present, filter for products with a discount
    if on_sale:
        goods = goods.filter(discount__gt=0)

    # If the 'order_by' parameter is present and not equal to "default", order the products accordingly
    if order_by and order_by != "default":
        goods = goods.order_by(order_by)

    # Create a paginator object with a step of 3 items per page
    paginator = Paginator(goods, 3)
    # Get the current page based on the page number from the request
    current_page = paginator.page(int(page))

    # Form the context for the template with the page title, list of products, and category slug
    context = {
        "title": "Home - Catalog",
        "goods": current_page,
        "slug_url": category_slug
    }
    # Return the response as a rendered HTML template with the provided context
    return render(request, "goods/catalog.html", context)


def product(request, product_slug):
    product = Products.objects.get(slug=product_slug)

    context = {"product": product}

    return render(request, "goods/product.html", context=context)


# def catalog(request, category_slug=None):
#     # Функція приймає HTTP-запит та необов'язковий параметр category_slug
#
#     page = request.GET.get('page', 1)
#     # Отримання номера сторінки з GET параметрів запиту, за замовчуванням - 1
#
#     on_sale = request.GET.get('on_sale', None)
#     # Отримання параметру 'on_sale' з GET параметрів запиту
#
#     order_by = request.GET.get('order_by', None)
#     # Отримання параметру 'order_by' з GET параметрів запиту
#
#     query = request.GET.get('q', None)
#     # Отримання параметру 'q' (пошукового запиту) з GET параметрів запиту
#
#     if category_slug == "all":
#         goods = Products.objects.all()
#         # Якщо category_slug дорівнює "all", вибираються всі продукти
#     elif query:
#         goods = q_search(query)
#         # Якщо є пошуковий запит, виконується пошук товарів за цим запитом
#     else:
#         goods = get_list_or_404(Products.objects.filter(category__slug=category_slug))
#         # Інакше вибираються продукти, що відповідають заданій категорії
#
#     # Перевірка, чи є goods об'єктом класу QuerySet, інакше перетворення на QuerySet
#     if not isinstance(goods, Products.objects.all().__class__):
#         goods = Products.objects.filter(id__in=[product.id for product in goods])
#
#     if on_sale:
#         goods = goods.filter(discount__gt=0)
#         # Якщо параметр 'on_sale' присутній, фільтруються тільки товари зі знижкою
#
#     if order_by and order_by != "default":
#         goods = goods.order_by(order_by)
#         # Якщо параметр 'order_by' присутній і не дорівнює "default", сортуються товари відповідно до цього параметру
#
#     paginator = Paginator(goods, 3)
#     # Створення об'єкта пагінації з кроком у 3 об'єкти на сторінку
#
#     current_page = paginator.page(int(page))
#     # Отримання поточної сторінки на основі номера сторінки з запиту
#
#     context = {
#         "title": "Home - Catalog",
#         "goods": current_page,
#         "slug_url": category_slug
#     }
#     # Формування контексту для шаблону з назвою сторінки, списком товарів та slug категорії
#
#     return render(request, "goods/catalog.html", context)
#     # Повернення відповіді у вигляді рендереного HTML-шаблону з переданим контекстом
#
#
