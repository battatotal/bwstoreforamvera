from django.shortcuts import render, redirect
from .models import OrderItem
from .forms import OrderCreateForm
from cart.cart import Cart
#from .tasks import order_created
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import get_object_or_404
from .models import Order
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import render_to_string
#import weasyprint
from shop.views import m, Menu
from django.views import View
#from .tasks import order_created
from django.urls import reverse

from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
@csrf_exempt  # Отключаем проверку CSRF, чтобы запрос прошел к следующему декоратору
@require_http_methods(["GET"])
def order_create(request):
    cart = Cart(request)
    menu = (Menu(x[0], x[1]) for x in m)
    # if request.method == 'POST':
    #     form = OrderCreateForm(request.POST)
    #     if form.is_valid():
    #         order = form.save(commit=False)
    #         order.save()
    #         for item in cart:
    #             OrderItem.objects.create(order=order,
    #                                     product=item['product'],
    #                                     price=item['price'],
    #                                     quantity=item['quantity'])
    #         # очистка корзины
    #         cart.clear()
    #         # Запуск асинхронной таски
    #         order_created.delay(order.id)
    #         # Сохранение заказа в сессии.
    #         request.session['order_id'] = order.id
    #         # Перенаправление на страницу оплаты.
    #
    #         return redirect(reverse('payment:process'))
    #
    # else:
    #     form = OrderCreateForm()

    form = OrderCreateForm() # в полной версии удалить(прописано выше)
    return render(request,
                  'orders/order/createNEW.html',
                  {'cart': cart, 'form': form, 'menu': menu})



@staff_member_required
def admin_order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request,'admin/orders/order/detail.html',{'order': order})




@staff_member_required
def admin_order_pdf(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    html = render_to_string('orders/order/pdf.html',{'order': order})
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="order_{}.pdf"'.format(order.id)
    #weasyprint.HTML(string=html).write_pdf(response,stylesheets=[weasyprint.CSS(settings.STATIC_ROOT + 'css/pdf.css')])
    return response