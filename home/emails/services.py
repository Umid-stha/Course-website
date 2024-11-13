from .models import Email, EmailVerificationEvent
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone

EMAIL_HOST_USER = settings.EMAIL_HOST_USER

def verify_email(email):
    qs = Email.objects.filter(email=email, active=False)
    return qs.exists()

def getVerificationEmailMessage(verification_instance, as_html = False):
    if not isinstance(verification_instance, EmailVerificationEvent):
        return None
    verify_link = verification_instance.get_link()
    if as_html:
        return f"<h1>Verify your email with:</h1><p><a href='{verify_link}'>{verify_link}</a></p>"
    return f"Verify your email with:{verify_link}"

def start_verification_event(email):
    email_obj, created = Email.objects.get_or_create(email=email)
    obj=EmailVerificationEvent.objects.create(
        parent=email_obj,
        email=email
    )
    send_verification_token(obj)
    return obj

def send_verification_token(obj):
    subject =  "Verify your email"
    text_msg= getVerificationEmailMessage(obj, as_html=False)
    text_html  = getVerificationEmailMessage(obj, as_html=True)

    sent = send_mail(
        subject=subject,
        message= text_msg,
        from_email= EMAIL_HOST_USER,
        recipient_list= [obj.email],
        fail_silently= False,
        html_message= text_html
    )

def verify_token(token, max_attempts=5):
    qs = EmailVerificationEvent.objects.filter(token=token)
    if not qs.exists() and not qs.count==1:
        return False, "invalid token", None
    email_expired = qs.filter(expired = True)
    if email_expired.exists():
        return False, "Token expired", None
    max_attempts_reached = qs.filter(attempts__gte = max_attempts)
    if max_attempts_reached.exists():
        return False, "Too many attempts used", None
    obj = qs.first()
    obj.attempts += 1
    obj.last_attempted_at = timezone.now()
    if obj.attempts > max_attempts:
        obj.expired = True
        obj.expired_at = timezone.now()
    obj.save()
    email_obj = obj.parent
    return True, "Welcome", email_obj
        

