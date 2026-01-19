from django.shortcuts import render, get_object_or_404
from .models import Category, Product
from cart.forms import CartAddProductForm
from django.views.generic import TemplateView, ListView, DetailView

m = (("Главная",''), ("Галерея","gallery/"), ("Заказать",""), ("Новости",""), ("О нас",""))


class Menu:
    def __init__(self, title, url=''):
        self.title = title
        self.url = url



# def main(request):
#
#     title = "Главная страница"
#     menu = (Menu(x[0],x[1]) for x in m)
#     current = "Главная"
#     # return render(request, 'product/main.html', {"menu": menu})
#     return render(request, 'product/main.html', {"menu": menu, "title": title, "current": current})

# def product_list(request, category_slug=None):
#
#     title = "Галлерея цветов"
#     menu = (Menu(x[0], x[1]) for x in m)
#
#     category = None
#     categories = Category.objects.all()
#     products = Product.objects.all()
#     current = "Галлерея"
#
#     if category_slug:
#         category = get_object_or_404(Category, slug=category_slug)
#         products = products.all()
#     return render(request, 'product/list.html',{'category': category,'categories': categories,'products': products, 'menu': menu,
#                                                  "title": title, "current": current})


def product_detail(request, id, slug):
    title = "Цветок"
    menu = [Menu(x[0], x[1]) for x in m]
    current = "Галерея"

    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    cart_product_form = CartAddProductForm()
    return render(request, 'product/gracedetail.html', {'product': product, 'menu': menu, "title": title, "current": current,
                                                   'cart_product_form': cart_product_form})


# def product_list_active(request, category_slug=None):
#
#     title = "Галлерея цветов рабочая"
#     menu = (Menu(x[0], x[1]) for x in m)
#
#     category = None
#     categories = Category.objects.all()
#     products = Product.objects.filter(available=True)
#     current = "Галлерея"
#
#     if category_slug:
#         category = get_object_or_404(Category, slug=category_slug)
#         products = products.filter(category=category)
#     return render(request, 'product/list_active.html',{'category': category,'categories': categories,'products': products, 'menu': menu,
#                                                  "title": title, "current": current})
#


class Main(TemplateView):
    template_name = 'product/mainNEW.html'


    def get_context_data(self, **kwargs):
        menu = [Menu(x[0], x[1]) for x in m]
        context = super().get_context_data(**kwargs)
        context['title'] = "Главная страница"
        context['current'] = "Главная"
        context['menu'] = menu

        return context


class ProdList(ListView):

    model = Product
    template_name = 'product/listNEW.html'
    context_object_name = "products"

    def get_context_data(self, **kwargs):
        menu = [Menu(x[0], x[1]) for x in m]
        context = super().get_context_data(**kwargs)
        context['title'] = "Галерея"
        context['current'] = "Галерея"
        context['menu'] = menu

        return context


class ProdListActive(ListView):

    model = Product
    template_name = 'product/list_activeNEW.html'
    context_object_name = "products"


    def get_queryset(self):
        return Product.objects.filter(available=True)

    def get_context_data(self, **kwargs):
        menu = [Menu(x[0], x[1]) for x in m]
        context = super().get_context_data(**kwargs)
        context['title'] = "Галерея товаров в наличии"
        context['current'] = "Галерея"
        context['menu'] = menu

        return context



class Tech_description(TemplateView):
    template_name = 'product/tech_description.html'


    def get_context_data(self, **kwargs):
        menu = [Menu(x[0], x[1]) for x in m]
        context = super().get_context_data(**kwargs)
        context['title'] = "Техническое описание"
        context['current'] = "Описание"
        context['menu'] = menu

        return context

# class ProdDetail(DetailView):
#     template_name = 'product/detail.html'
#     model = Product
#     context_object_name = "products"
#     slug_url_kwarg = 'slug'
#     id_url_kwarg = 'product_id'
#
#
#     def get_context_data(self, **kwargs):
#         cart_product_form = CartAddProductForm()
#         product_id = self.get_context_data(**kwargs['product_id'])
#         menu = (Menu(x[0], x[1]) for x in m)
#         context = super().get_context_data(**kwargs)
#         context['title'] = "Страница товара"
#         context['current'] = "Галлерея"
#         context['menu'] = menu
#         context['cart_product_form']= cart_product_form
#         return context