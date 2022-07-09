import os
import requests
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, reverse  # , render
from django.urls import reverse_lazy
from django.core.files.base import ContentFile
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin

# from django.views import View
from django.contrib.auth.views import PasswordChangeView
from django.views.generic import FormView, DetailView, UpdateView
from . import forms, models, mixins


class LoginView(mixins.LoggedOutOnlyView, FormView):

    template_name = "users/login.html"
    form_class = forms.LoginForm

    def form_valid(self, form):
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(self.request, username=email, password=password)
        if user is not None:
            login(self.request, user)
        return super().form_valid(form)

    def get_success_url(self):
        next_arg = self.request.GET.get("next")
        if next_arg is not None:
            return next_arg
        else:
            return reverse("core:home")


def log_out(request):
    messages.info(request, "See you later")
    logout(request)
    return redirect(reverse("core:home"))


class SignUpView(mixins.LoggedOutOnlyView, FormView):

    template_name = "users/signup.html"
    form_class = forms.SignUpForm
    success_url = reverse_lazy("core:home")

    def form_valid(self, form):
        form.save()
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(self.request, username=email, password=password)
        if user is not None:
            login(self.request, user)
        return super().form_valid(form)


def complete_verification(request, key):
    try:
        user = models.User.objects.get(email_key=key)
        user.email_verified = True
        user.email_secret = ""
        user.save()
        # to do : add success message
    except models.User.DoesNotExist:
        # to do: add error message
        pass
    return redirect(reverse("core:home"))


def github_login(request):
    client_id = os.environ.get("GITHUB_ID")
    redirect_uri = "http://127.0.0.1:8000/users/login/github/callback"
    return redirect(
        f"https://github.com/login/oauth/authorize?client_id={client_id}&redirect_uri={redirect_uri}&scope=read:user, user:email"
    )
    # scope에 user:email 추가


class GithubException(Exception):
    pass


def github_callback(request):
    try:
        client_id = os.environ.get("GITHUB_ID")
        client_secret = os.environ.get("GITHUB_SECRET")
        code = request.GET.get("code", None)
        if code is not None:
            token_request = requests.post(
                f"https://github.com/login/oauth/access_token?client_id={client_id}&client_secret={client_secret}&code={code}",
                headers={"Accept": "application/json"},
            )
            token_json = token_request.json()
            error = token_json.get("error", None)
            if error is not None:
                raise GithubException("Failed to get access token")
            else:
                access_token = token_json.get("access_token")
                profile_request = requests.get(
                    "https://api.github.com/user",
                    headers={
                        "Authorization": f"token {access_token}",
                        "Accept": "application/json",
                    },
                )
                profile_json = profile_request.json()
                username = profile_json.get("login", None)
                # Github의 개인계정 설정에서 email의 속성이 private으로 설정되어 있으면
                # https://api.github.com/user 에서는 반환되는 json의 email 키의 값에 None으로 반환되므로
                # 아래와 같이 추가로 https://api.github.com/user/emails 을 통해 이메일 값을 추출해 낸다.
                email_request = requests.get(
                    "https://api.github.com/user/emails",
                    headers={
                        "Authorization": f"token {access_token}",
                        "Accept": "application/json",
                    },
                )
                email_json = email_request.json()
                email = email_json[0].get("email", None)
                if username is not None:
                    name_get = profile_json.get("name")
                    bio_get = profile_json.get("bio")
                    name = (
                        "" if name_get is None else name_get
                    )  # User object 생성시 name에 None이 들어가는 것을 방지
                    bio = (
                        "" if bio_get is None else bio_get
                    )  # User object 생성시 bio에 None이 들어가는 것을 방지
                    try:
                        user = models.User.objects.get(email=email)
                        if user.login_method != models.User.LOGIN_GITHUB:
                            raise GithubException(
                                f"Please log in with: {user.login_method}"
                            )
                    except models.User.DoesNotExist:
                        user = models.User.objects.create(
                            username=email,
                            email=email,
                            first_name=name,
                            bio=bio,
                            login_method=models.User.LOGIN_GITHUB,
                            email_verified=True,
                        )
                        user.set_unusable_password()
                        user.save()
                    login(request, user)
                    messages.success(request, f"Welcome back {user.first_name}")
                    return redirect(reverse("core:home"))
                else:
                    raise GithubException("Failed to get your profile")
        else:
            raise GithubException("Failed to get code")
    except GithubException as e:
        messages.error(request, e)
        return redirect(reverse("users:login"))


def kakao_login(request):
    client_id = os.environ.get("KAKAO_KEY")
    redirect_uri = "http://127.0.0.1:8000/users/login/kakao/callback"
    return redirect(
        f"https://kauth.kakao.com/oauth/authorize?client_id={client_id}&redirect_uri={redirect_uri}&response_type=code"
    )
    # scope에 user:email 추가


class KakaoException(Exception):
    pass


def kakao_callback(request):
    try:
        code = request.GET.get("code")
        client_id = os.environ.get("KAKAO_KEY")
        redirect_uri = "http://127.0.0.1:8000/users/login/kakao/callback"
        token_request = requests.get(
            f"https://kauth.kakao.com/oauth/token?grant_type=authorization_code&client_id={client_id}&redirect_uri={redirect_uri}&code={code}",
            headers={"Content-type": "application/x-www-form-urlencoded;charset=utf-8"},
        )
        token_json = token_request.json()
        error = token_json.get("error", None)
        if error is not None:
            raise KakaoException("Failed to get access token")
        access_token = token_json.get("access_token")
        profile_request = requests.get(
            "https://kapi.kakao.com/v2/user/me",
            headers={
                "Authorization": f"Bearer {access_token}",
                "Content-type": "application/x-www-form-urlencoded;charset=utf-8",
            },
        )
        profile_json = profile_request.json()
        """
        카카오 프로필 json response
        {
            'id': 2324271388,
            'connected_at': '2022-07-02T15:45:24Z',
            'properties': {
​							'nickname': '문형욱',
​							'profile_image': 'http://k.kakaocdn.net/dn/ixHxX/btqQSBQ71h3/EHwMvU2A9MlJvgO4CWlku0/img_640x640.jpg', 
​							'thumbnail_image': 'http://k.kakaocdn.net/dn/ixHxX/btqQSBQ71h3/EHwMvU2A9MlJvgO4CWlku0/img_110x110.jpg'},
​						   },
            'kakao_account': {
                               'profile_nickname_needs_agreement': False,
                               'profile_image_needs_agreement': True,
                               'profile': {
                                           'nickname': '문형욱'
                                           'thumbnail_image_url': 'http://k.kakaocdn.net/dn/ixHxX/btqQSBQ71h3/EHwMvU2A9MlJvgO4CWlku0/img_110x110.jpg',
    ​                                       'profile_image_url': 'http://k.kakaocdn.net/dn/ixHxX/btqQSBQ71h3/EHwMvU2A9MlJvgO4CWlku0/img_640x640.jpg',
                                           'is_default_image': False
                                           },
                               'has_email': True,
                               'email_needs_agreement': False,
                               'is_email_valid': True,
                               'is_email_verified': True,
                               'email': 'moondive79@gmail.com',
    ​							}

        }
        """
        email = profile_json.get("kakao_account").get("email", None)
        if email is None:
            raise KakaoException("Please provide your email info")
        properties = profile_json.get("properties")
        nickname = properties.get("nickname", None)
        profile_image = properties.get("profile_image", None)
        try:
            user = models.User.objects.get(email=email)
            if user.login_method != models.User.LOGIN_KAKAO:
                raise KakaoException(f"Please log in with: {user.login_method}")
        except models.User.DoesNotExist:
            user = models.User.objects.create(
                username=email,
                email=email,
                first_name=nickname,
                login_method=models.User.LOGIN_KAKAO,
                email_verified=True,
            )
            user.set_unusable_password()
            user.save()
            if profile_image is not None:
                photo_request = requests.get(profile_image)
                user.avatar.save(
                    f"{nickname}-avatar", ContentFile(photo_request.content)
                )
        messages.success(request, f"Welcome back {user.first_name}")
        login(request, user)
        return redirect(reverse("core:home"))
    except KakaoException as e:
        messages.error(request, e)
        return redirect(reverse("users:login"))


class UserProfileView(DetailView):

    model = models.User
    context_object_name = "user_obj"

    # context 추가 예시용 코드 => 추가 context를 템플릿에 보낼수 있다.
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["hello"] = "Hello!"
        return context


class UpdateProfileView(mixins.LoginRequiredMixin, SuccessMessageMixin, UpdateView):

    model = models.User
    template_name = "users/update-profile.html"
    fields = (
        "first_name",
        "last_name",
        "avatar",
        "gender",
        "bio",
        "birthdate",
        "language",
        "currency",
    )
    success_message = "Profile Updated"

    def get_object(self, queryset=None):
        return self.request.user


class UpdatePasswordView(
    mixins.EmailLoginOnlyView,
    mixins.LoginRequiredMixin,
    SuccessMessageMixin,
    PasswordChangeView,
):

    template_name = "users/update-password.html"
    success_message = "Password Updated"

    def get_form(self, form_class=None):
        form = super().get_form(form_class=form_class)
        form.fields["old_password"].widget.attrs = {"placeholder": "Current password"}
        form.fields["new_password1"].widget.attrs = {"placeholder": "New password"}
        form.fields["new_password2"].widget.attrs = {
            "placeholder": "Confirm new password"
        }
        return form

    def get_success_url(self):
        return self.request.user.get_absolute_url()
