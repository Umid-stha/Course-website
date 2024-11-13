from django import forms
from .models import Email
from .services import verify_email

class EmailForm(forms.Form):
    email=forms.EmailField(  
        widget=forms.EmailInput(
            attrs={
                "id": "email-login-input",
                "class":"bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
            }
        )
    )
    # class Meta:
    #     model=Email
    #     fields=["email"]

    def clean_email(self):
        email = self.cleaned_data.get('email')
        verified = verify_email(email)
        print(email)
        if not verified:
            raise forms.ValidationError("Invalid email.")
        return email