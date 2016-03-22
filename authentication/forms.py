from django import forms
from .models import Account, SignupKey


class RegistrationForm(forms.ModelForm):
    """
    Form for registering a new account.
    """
    email = forms.EmailField(widget=forms.widgets.TextInput, label="Email")
    first_name = forms.CharField(widget=forms.widgets.TextInput, label="First Name")
    last_name = forms.CharField(widget=forms.widgets.TextInput, label="Last Name")
    password = forms.CharField(widget=forms.widgets.PasswordInput, label="Password")
    password_confirm = forms.CharField(widget=forms.widgets.PasswordInput, label="Password (again)")
    signup_key = forms.CharField(widget=forms.widgets.TextInput, max_length=10, label="Signup Key")

    class Meta:
        model = Account
        fields = ['email', 'first_name', 'last_name', 'password', 'password_confirm']

    def clean(self):
        """
        Verifies that the values entered into the password fields match

        NOTE: Errors here will appear in ``non_field_errors()`` because it applies to more than one field.
        """
        cleaned_data = super(RegistrationForm, self).clean()
        if 'password' in self.cleaned_data and 'password_confirm' in self.cleaned_data:
            if self.cleaned_data['password'] != self.cleaned_data['password_confirm']:
                raise forms.ValidationError("Passwords don't match. Please enter both fields again.")

        # try:
        #     key = SignupKey.objects.get(key=cleaned_data['signup_key'])
        #     if forms.account:
        #         raise forms.ValidationError("Signup key already in use")
        # except:
        #     raise forms.ValidationError("Signup key ballballsbals.")

        return self.cleaned_data

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user

class LoginForm(forms.Form):
    """
    Form for authenticating
    """
    email = forms.EmailField(widget=forms.widgets.TextInput)
    password = forms.CharField(widget=forms.widgets.PasswordInput)

    class Meta:
        fields = ['email', 'password']