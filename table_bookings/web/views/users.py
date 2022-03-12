from datetime import timedelta

from django.contrib import auth, messages
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.shortcuts import redirect
from django.template.loader import render_to_string
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.views import View
from django.views.generic import FormView

from ..forms import RegisterForm, LoginForm
from ..models import UserProfile, UserVerification
from ..utils import create_email_key


def send_verification_email(request, user, receiver):
    key = create_email_key(user.id)
    link = f"http://{request.get_host()}{reverse('verification')}?key={key}"
    expired_at = timezone.now() + timedelta(days=3)  # 3일 안에 인증을 해야함
    UserVerification.objects.create(user=user, key=key, expired_at=expired_at)

    email_context = {'link': link}
    msg_plain = render_to_string('email/verification.txt', email_context)
    msg_html = render_to_string('email/verification.html', email_context)
    send_mail(
        '이메일 인증을 완료해주세요.', msg_plain,
        'wnsdud3119@gmail.com',
        [receiver],
        html_message=msg_html,
        fail_silently=True
    )


class RegisterView(FormView):
    template_name = 'users/register.html'
    form_class = RegisterForm
    success_url = reverse_lazy('index')

    # form 의 clean 함수가 실행 뒤
    def form_valid(self, form):
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']
        nickname = form.cleaned_data['nickname']
        profile_image = form.cleaned_data['profile_image']
        user = User.objects.create_user(email, email, password)
        UserProfile.objects.create(user=user, nickname=nickname, profile_image=profile_image)

        send_verification_email(self.request, user, email)

        return super(RegisterView, self).form_valid(form)


class LoginView(FormView):
    template_name = 'users/login.html'
    success_url = reverse_lazy('index')
    form_class = LoginForm

    def form_valid(self, form):
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']
        user = auth.authenticate(username=email, password=password)
        if user is not None:
            auth.login(self.request, user)  # django session에 기록
            return super(LoginView, self).form_valid(form)
        else:
            messages.warning(self.request, '계정 혹은 비밀번호를 확인해주세요.')
            return redirect(reverse_lazy('login'))


class LogoutView(View):
    def get(self, request):
        auth.logout(request)
        return redirect(reverse('index'))


class VerificationView(View):
    def get(self, request):
        key = request.GET.get('key', '')
        verification = UserVerification.objects.get(key=key)
        current = timezone.now()

        if verification.expired_at > current:
            verification.verified = True
            verification.verified_at = current
            verification.save()

            user = verification.user
            user.verification = True
            user.save()

            messages.success(self.request, '인증이 완료되었습니다.')
        else:
            messages.warning(self.request, '인증을 다시 시도해주세요.')

        return redirect(reverse('index'))
