from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()


class RegistrationForm(forms.ModelForm):
    email = forms.EmailField(label="Email")
    password1 = forms.CharField(label="Senha", widget=forms.PasswordInput)
    password2 = forms.CharField(
        label="Confirma Senha", widget=forms.PasswordInput)

    def clean_password2(self):
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']
        if password1 != password2:
            raise forms.ValidationError('A confirmação não está correta')
        return password2

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.set_password = self.cleaned_data['password1']
        if commit:
            user.save()
        return user

    class Meta:
        model = User
        fields = ['username', 'email', 'name', ]


class EditAccountForm(forms.ModelForm):

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'name',
        ]
