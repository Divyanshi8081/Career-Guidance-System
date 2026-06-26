from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'placeholder': 'your@email.com'}))
    first_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'placeholder': 'First Name'}))
    last_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'placeholder': 'Last Name'}))

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'bio', 'profile_pic',
                  'current_skills', 'desired_career', 'linkedin_url', 'github_url', 'experience_years']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 3}),
            'current_skills': forms.TextInput(attrs={'placeholder': 'Python, Django, SQL, Machine Learning...'}),
            'desired_career': forms.TextInput(attrs={'placeholder': 'e.g. Software Engineer, Data Scientist...'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            if not isinstance(field.widget, forms.FileInput):
                field.widget.attrs['class'] = 'form-control'
