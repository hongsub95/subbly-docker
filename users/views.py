import os
import requests
from django.shortcuts import redirect, reverse,render
from django.urls import reverse_lazy
from django.views.generic import FormView
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from . import forms, models
from orders.models import Order



class LoginView(FormView):

    template_name = "users/login.html"
    form_class = forms.LoginForm
    success_url = reverse_lazy("clothes:all_clothes")

    def form_valid(self, form):
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(self.request, username=email, password=password)
        if user is not None:
            login(self.request, user)
        next_val = self.request.POST.get('next')
        if next_val:
            return redirect(next_val)
        return super().form_valid(form)


def log_out(request):
    logout(request)
    return redirect(reverse("clothes:all_clothes"))


class SignUpView(FormView):
    template_name = "users/signup.html"
    form_class = forms.SignUpForm
    success_url = reverse_lazy("clothes:all_clothes")

    def form_valid(self, form):
        form.save()
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password1")
        user = authenticate(self.request, username=email, password=password)
        if user is not None:
            login(self.request, user)
        return super().form_valid(form)


def kakao_login(request):
    REST_API_KEY = os.environ.get("K_KEY")
    REDIRECT_URI = "http://127.0.0.1:8000/users/login/kakao/callback"
    return redirect(
        f"https://kauth.kakao.com/oauth/authorize?response_type=code&client_id={REST_API_KEY}&redirect_uri={REDIRECT_URI}"
    )


class KakaoException(Exception):
    pass


def kakao_callback(request):
    try:
        AUTHORIZE_CODE = request.GET.get("code")
        REST_API_KEY = os.environ.get("K_KEY")
        REDIRECT_URI = "http://127.0.0.1:8000/users/login/kakao/callback"
        token_request = requests.get(
            f"https://kauth.kakao.com/oauth/token?grant_type=authorization_code&client_id={REST_API_KEY}&redirect_uri={REDIRECT_URI}&code={AUTHORIZE_CODE}"
        )
        token_json = token_request.json()
        error = token_json.get("error")
        if error is not None:
            raise KakaoException()
        ACCESS_TOKEN = token_json.get("access_token")
        profile_request = requests.get(
            "https://kapi.kakao.com/v2/user/me",
            headers={"Authorization": f"Bearer {ACCESS_TOKEN}"},
        )
        profile_json = profile_request.json()
        k_account = profile_json.get("kakao_account")
        email = k_account.get("email", None)
        if email is None:
            raise KakaoException()
        nickname = k_account.get("profile").get("nickname")
        profile_image = k_account.get("profile").get("profile_image_url")
        try:
            user = models.User.objects.get(email=email)
            if user.login_method == models.User.LOGIN_KAKAO:
                raise KakaoException()
        except models.User.DoesNotExist:
            user = models.User.objects.create(
                email=email, first_name=nickname, login_method=models.User.LOGIN_KAKAO
            )
            user.set_unusable_password()
            user.save()
        login(request, user)
        return redirect(reverse("clothes:all_clothes"))
    except KakaoException:
        return redirect(reverse("users:login"))

@login_required
def PurchaseList(request,user_pk):
    try:
        orders = Order.objects.filter(buyer=user_pk).all()
        return render(request,'users/mypage.html',{'orders':orders})
    except Order.DoesNotExist:
        return render(request,'users/mypage.html')
    
    
