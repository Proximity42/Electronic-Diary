from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView
from django.urls import path
from users.views import UserProfileView


urlpatterns = [
    path('login/', LoginView.as_view(template_name="login.html"), name='login'),
    path('logout/', LogoutView.as_view(next_page='login', template_name='logged_out.html'), name='logout'),
    path('password-change/', PasswordChangeView.as_view(template_name='password_change.html', success_url='/login/'), name='password_change'),
    path('password-change/done/', PasswordChangeDoneView.as_view(template_name='password_change_done.html'), name='password_change_done'),
    path('profile/<pk>', UserProfileView.as_view(), name='profile')
]

