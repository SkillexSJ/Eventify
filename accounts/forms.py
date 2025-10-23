from django.contrib.auth.forms import UserCreationForm , AuthenticationForm
from django import forms
from django.contrib.auth.models import User
class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=100, required=True)
    last_name = forms.CharField(max_length=100, required=True)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email',)


class CustomAuthenticationForm(AuthenticationForm):
    
    def clean(self):
        cleaned_data = super().clean()
        user = self.user_cache
        if user is not None and not user.is_active:
            raise forms.ValidationError("This account is inactiv")
        return cleaned_data