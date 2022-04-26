from django.urls import path, reverse_lazy
from django.contrib.auth.views import (
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
    PasswordChangeView,
    PasswordChangeDoneView,
)
from accounts.views import (
    MyLoginView,
    MyLogoutView, 
    CheckUsername, 
    CheckEmail, 
    MyRegisterView,
    PasswordResetRequest,
    ProfileView,
    ProfileEdit,
    RegisterSuccess,
)


app_name = "accounts"
urlpatterns = [
    path('profile/', ProfileView.as_view(), name='profile'),
    path('login/', MyLoginView.as_view(), name="login"),
    path('logout/', MyLogoutView.as_view(), name="logout"),
    path('register-success/', RegisterSuccess.as_view(), name="register_success"),
    path('register/', MyRegisterView.as_view(), name='register'),
    path('password-change/', PasswordChangeView.as_view(template_name="accounts/password_change.html"), name='password_change'),
    path('password-change-done/', PasswordChangeDoneView.as_view(template_name="accounts/password_change_done.html"), name='password_change_done'),
    path('password-reset/', PasswordResetRequest.as_view(), name='password_reset'),
    path('password-reset-done/', PasswordResetDoneView.as_view(template_name="accounts/password_reset_done.html"),name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(template_name="accounts/password_reset_confirm.html",success_url=reverse_lazy('accounts:password_reset_complete')), name='password_reset_confirm'),
    path('password-reset-complete/', PasswordResetCompleteView.as_view(template_name="accounts/password_reset_complete.html"),name='password_reset_complete'),
]

htmx_urlpatterns = [
    path('check-username/', CheckUsername.as_view(), name="check_username"),
    path('check-email/', CheckEmail.as_view(), name='check_email'),
    path('edit-profile', ProfileEdit.as_view(), name='edit_profile'),
]

urlpatterns += htmx_urlpatterns