from django.shortcuts import render
from emails.forms import EmailForm
from emails.models import Email, EmailVerificationEvent
from emails.services import start_verification_event

def home(request):
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
    return render(request, 'home.html', context)