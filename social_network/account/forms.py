from django import forms

class ConfirmTempPasswordForm(forms.Form):
    temp_password = forms.CharField(widget=forms.PasswordInput, label="Temporary Password")
    new_password = forms.CharField(widget=forms.PasswordInput, label="New Password")
    confirm_password = forms.CharField(widget=forms.PasswordInput, label="Confirm New Password")

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get("new_password")
        confirm_password = cleaned_data.get("confirm_password")
        if new_password != confirm_password:
            raise forms.ValidationError("New password and confirm password do not match.")
        return cleaned_data



class LoginForm(forms.Form):
    identifier = forms.CharField(max_length=150, label="Email or Mobile")
    password = forms.CharField(widget=forms.PasswordInput, label="Password")
    


class EmailLoginForm(forms.Form):
    email = forms.EmailField(label="Email")
    password = forms.CharField(widget=forms.PasswordInput, label="Password")




