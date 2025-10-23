from django.dispatch import receiver
from django.db.models.signals import m2m_changed
from .models import Event
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings


@receiver(m2m_changed, sender=Event.rsvped_users.through)
def send_rsvp_confirmation(sender, instance, action, pk_set, **kwargs):
    if action == "post_add":
        for user_id in pk_set:
            try:
                user = User.objects.get(pk=user_id)
                event = instance

                subject = f'✅ RSVP Confirmation for {event.name}'
                
                body = f"""Dear {user.username},

                🎉 You have successfully RSVP'd to the event!

                Event Details:
                ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
                📌 Event: {event.name}
                📅 Date: {event.date}
                ⏰ Time: {event.time}
                📍 Location: {event.location}
                🏷️ Category: {event.category.name}

                We're excited to see you there!

                If you need to cancel your RSVP, please visit the event page on Eventify.

                Best regards,
                The Eventify Team
                """

                send_mail(
                    subject,
                    body,
                    settings.EMAIL_HOST_USER,
                    [user.email],
                    fail_silently=False,
                )

                print(f"RSVP confirmation email sent to user {user_id}")
                
            except User.DoesNotExist:
                print(f"User with ID {user_id} does not exist")
            except Exception as e:
                print(f"Error sending RSVP confirmation email to user {user_id}: {e}")