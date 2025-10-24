from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User, Group


@receiver(post_save, sender=User)
def send_activation_email(sender, instance, created, **kwargs):
    if created and not instance.is_staff:
        try:
            participant_group = Group.objects.get(name='Participant')
            # add korlam participant group e
            instance.groups.add(participant_group)
        except Group.DoesNotExist:
            print("error adding group")
        
        token = default_token_generator.make_token(instance)
        domain = settings.SITE_DOMAIN
       
        protocol = 'https' if 'render.com' in domain else 'http'
        activation_link = f"{protocol}://{domain}/accounts/activate/{instance.id}/{token}/"
        
        # Email content
        subject = "Activate your Eventify account"
        message = f"""Hi {instance.username},

Welcome to Eventify! 🎉

Please click the link below to activate your account:
{activation_link}

If you didn't create this account, please ignore this email.

Thank you!
The Eventify Team"""

        try:
            send_mail(
                subject,
                message,
                settings.EMAIL_HOST_USER,
                [instance.email],
                fail_silently=True,
            )
            print(f"Activation email sent to {instance.email}")
        except Exception as e:
            print(f"Error sending email to {instance.email}: {e}")

