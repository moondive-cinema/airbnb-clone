from django import forms
from . import models


class LoginForm(forms.Form):

    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")
        try:
            user = models.User.objects.get(email=email)
            if user.check_password(password):
                return self.cleaned_data
            else:
                self.add_error("password", forms.ValidationError("Password is wrong."))
        except models.User.DoesNotExist:
            self.add_error("email", forms.ValidationError("User does not exist."))


class SignUpForm(forms.ModelForm):
    # 장고 오센티케이션 시스템 빌트인폼 UserCreationForm 활용하면 더 간단하게 구현 가능 (하단 주석 참고))
    class Meta:
        model = models.User
        fields = ("first_name", "last_name", "email")

    password = forms.CharField(widget=forms.PasswordInput)
    password_again = forms.CharField(
        widget=forms.PasswordInput, label="Confirm Password"
    )

    def clean_password_again(self):
        password = self.cleaned_data.get("password")
        password_again = self.cleaned_data.get("password_again")
        if password != password_again:
            raise forms.ValidationError("Password does not match.")
        else:
            return password
        # django.contrib,auth에서 password_validation.validate_password() 함수를 이용하여 비밀번호 검사 가능함

    def save(self, *args, **kwargs):
        user = super().save(commit=False)
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")
        user.username = email
        user.set_password(password)
        user.save()


"""
<UserCreationForm 을 통한 구현>

from django.contrib.auth.forms import UserCreationForm

class SignUpForm(UserCreationForm):
    username = forms.EmailField(label="email)




<ModelForm 말고, 일반 Form으로 작성한 SignUpForm 클래스>

class SignUpForm(forms.Form):

    first_name = forms.CharField(max_length=80)
    last_name = forms.CharField(max_length=80)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    password_again = forms.CharField(
        widget=forms.PasswordInput, label="Confirm Password"
    )

    def clean_email(self):
        email = self.cleaned_data.get("email")
        try:
            models.User.objects.get(email=email)
            raise forms.ValidationError("User already exists with that email")
        except models.User.DoesNotExist:
            return email

    def clean_password_again(self):
        password = self.cleaned_data.get("password")
        password_again = self.cleaned_data.get("password_again")
        if password != password_again:
            raise forms.ValidationError("Password does not match.")
        else:
            return password

    def save(self):
        first_name = self.cleaned_data.get("first_name")
        last_name = self.cleaned_data.get("last_name")
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")

        user = models.User.objects.create_user(email, email, password)
        user.first_name = first_name
        user.last_name = last_name
        user.save()
"""
