from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile

class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, help_text='First Name')
    last_name = forms.CharField(max_length=30, required=True, help_text='Last Name')
    email = forms.EmailField(max_length=254, help_text='Required. Enter a valid email address.')
    cin = forms.CharField(max_length=20, required=True, help_text='CIN')
    birthdate = forms.DateField(required=True, widget=forms.DateInput(attrs={'type': 'date'}), help_text='Birthdate')
    photo = forms.ImageField(required=False, help_text='Upload your profile picture (optional).')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'cin', 'birthdate', 'photo')
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Username'}),
            'first_name': forms.TextInput(attrs={'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Last Name'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Email'}),
            'password1': forms.PasswordInput(attrs={'placeholder': 'Password'}),
            'password2': forms.PasswordInput(attrs={'placeholder': 'Confirm Password'}),
            'cin': forms.TextInput(attrs={'placeholder': 'CIN'}),
            'birthdate': forms.DateInput(attrs={'type': 'date', 'placeholder': 'Birthdate'}),
            'photo': forms.ClearableFileInput(attrs={'placeholder': 'Profile Picture'}),
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            # Ensure profile is created if it doesn't exist
            profile, created = Profile.objects.update_or_create(
                user=user,
                defaults={
                    'cin': self.cleaned_data['cin'],
                    'birthdate': self.cleaned_data['birthdate'],
                    'photo': self.cleaned_data.get('photo')  # Save the photo
                }
            )
        return user
