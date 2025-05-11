from django import forms
from .models import Debtor, Transaction
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile

class DebtorForm(forms.ModelForm):
    class Meta:
        model = Debtor
        fields = ['name','phone']

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['kind','amount','note']




class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model  = User
        fields = ['username','email','password1','password2']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model  = Profile
        fields = ['phone','avatar']
