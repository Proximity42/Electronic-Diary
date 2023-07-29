from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from users.views import UserProfileView

urlpatterns = [
    path('login/', LoginView.as_view(template_name="login.html"), name='login'),
    path('logout/', LogoutView.as_view(next_page='login', template_name='logged_out.html'), name='logout'),
    path('profile/<pk>', UserProfileView.as_view(), name='profile')
]