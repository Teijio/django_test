from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver

from orders.models import Order
from .models import Robot


@receiver(post_save, sender=Robot)
def send_order_notification(sender, instance, **kwargs):
    if kwargs.get("created", False):
        waiting_orders = Order.objects.filter(
            robot_serial=instance.serial, waiting_for_robot=True
        )

        if waiting_orders.exists():
            for order in waiting_orders:
                send_mail(
                    subject="Робот в наличии!",
                    message=f"""
                    Добрый день!,
                    Недавно вы интересовались нашим
                    роботом модели {instance.model}, версии {instance.version}.
                    Этот робот теперь в наличии."
                    Если вам подходит этот вариант - пожалуйста,
                    свяжитесь с нами.
                    """,
                    from_email="your_email@test.com",
                    recipient_list=[order.customer.email],
                )
                order.waiting_for_robot = False
                order.save()
