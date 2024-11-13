from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import EmailVerificationEvent
from .forms import EmailForm
from .services import start_verification_event
from django.contrib import messages
from . import services

def email_token_login(request):
    if not request.htmx:
        return redirect("/")
    templates = "email/hx/form.html"
    form = EmailForm(request.POST or None)
    context={
        'form':form,
        'message':""
    }
    if form.is_valid():
        email_val = form.cleaned_data.get('email')
        # obj = form.save()
        obj = start_verification_event(email_val)
        context['form']=EmailForm()
        context['message']="success"
    print(request.session.get('email_id'))
    return render(request, templates, context)

def verify_email(request, token, *args, **kwargs):
    did_verify, msg, email_obj = services.verify_token(token)
    if not did_verify:
        messages.error(request, msg)
        return redirect("/login")
    messages.success(request, msg)
    request.session['email_id']=f"{email_obj.id}"
    next_url = request.session.get("next_url") or "/"
    if not next_url.startswith("/"):
        next_url="/"
    return redirect(next_url)