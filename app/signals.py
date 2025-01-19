from app.models import CustomUser
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings

@receiver(pre_save, sender=CustomUser)
def presavefunc(sender, instance, **kwargs):
    print(f'user {instance} has been initialized')


@receiver(post_save, sender=CustomUser)
def postsavefunc(sender, created, instance, **kwargs):
    if created:
        subject = f'Welcome {instance.username} to Portfolio Generator'
        message = 'Good To See You Here'
        # send_mail(subject,message, settings.EMAIL_HOST_USER, [instance.email], fail_silently=False)
        send_mail(
                    subject,  # Email subject
                    message,  
                    settings.EMAIL_HOST_USER,  # Sender email
                    [instance.email],  # List of recipient emails
                    fail_silently=False,  # Raise exceptions if sending fails
                 )
    else:
        print(f'user {instance} is modified')
