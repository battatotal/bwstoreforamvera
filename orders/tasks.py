from celery import shared_task
from django.core.mail import send_mail
from .models import Order


@shared_task()
def order_created(order_id):
    """Задача отправки email-уведомлений при успешном оформлении заказа."""
    order = Order.objects.get(id=order_id)
    subject = f'Заказ номер {order.id}'
    message = 'Уважаемый {},\n\nВы успешно разместили заказ.Номер вашего заказа {}.'.format(order.first_name,order.id)
    mail_sent = send_mail(subject,message,'somml@sommlforeg.al',[order.email])

    return mail_sent

    # return 5