from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from .models import CustomUser
from .forms import CustomUserCreationForm
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from .models import SignupToken
from django.http import HttpResponse
from django.urls import reverse
import uuid
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .forms import CustomUserChangeForm
from django.shortcuts import render, get_object_or_404

def signup_view(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('login')  # ログイン画面にリダイレクト
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/signup.html', {'form': form})

@login_required
def profile_view(request, pk):
    user = get_object_or_404(CustomUser, pk=pk)
    return render(request, 'users/profile.html', {'user': user})

def profile_edit_view(request):
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('home', pk=request.user.pk)  # 編集後にプロフィールページにリダイレクト
    else:
        form = CustomUserChangeForm(instance=request.user)

    return render(request, 'users/profile_edit.html', {'form': form})

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('polls:poll_list')  # Redirect to a specific view
    else:
        form = UserCreationForm()
    return render(request, 'users/register.html', {'form': form})

from django.contrib.auth.views import LogoutView

class CustomLogoutView(LogoutView):
    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)



User = get_user_model()

def signup_request(request):
    if request.method == "POST":
        email = request.POST.get("email")
        
        # メールアドレスが既に登録されているか確認
        if User.objects.filter(email=email).exists():
            return HttpResponse("このメールアドレスはすでに登録されています。")

        # 既存トークンの確認
        existing_token = SignupToken.objects.filter(email=email).first()
        
        if existing_token:
            token = existing_token.token  # 既存トークンを使う
        else:
            token = uuid.uuid4()  # 新しいUUIDトークンを生成
            # 新しいトークンをデータベースに保存
            SignupToken.objects.create(email=email, token=token)
        
        # サインアップ確認用のURLを生成
        signup_url = request.build_absolute_uri(reverse('users:signup_confirm', args=[token]))
        
        # 認証メールを送信
        send_mail(
            "アカウント作成認証",
            f"以下のリンクをクリックしてアカウント作成を完了してください:\n{signup_url}",
            'auth.uniqa@gmail.com',
            [email],
        )
        
        return HttpResponse("認証メールを送信しました。")
    
    return render(request, "users/signup_request.html")
def signup_confirm(request, token):
    try:
        signup_token = SignupToken.objects.get(token=token)
    except SignupToken.DoesNotExist:
        return HttpResponse("無効なトークンです。")

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = User.objects.create(
            username=username,
            email=signup_token.email,
            password=make_password(password),
        )
        signup_token.delete()
        return redirect("users:login")
    return render(request, "users/signup_confirm.html", {"token": token})

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('profile')  # ユーザープロフィール画面にリダイレクト
        else:
            return HttpResponse("ログイン失敗")
    return render(request, 'users/login.html')


@login_required
def profile_view(request):
    return render(request, 'users/profile_view.html', {'user': request.user})