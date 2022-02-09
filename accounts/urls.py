from django.urls import path, reverse_lazy
from django.contrib.auth.views import (
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
    PasswordChangeView,
    PasswordChangeDoneView,
)

from accounts.views import (
    logout_view,
    register_view,
    login_view,
    check_username,
    check_email,
    password_reset_request,
    profile_view,
    profile_edit,
)

app_name = "accounts"
urlpatterns = [
    path('profile/', profile_view, name='profile'),
    path('login/', login_view, name="login"),
    path('logout/', logout_view, name="logout"),
    path('register/', register_view, name='register'),
    path('password-change/', PasswordChangeView.as_view(template_name="accounts/password_change.html"), name='password_change'),
    path('password-change-done/', PasswordChangeDoneView.as_view(template_name="accounts/password_change_done.html"), name='password_change_done'),
    path('password-reset/', password_reset_request, name='password_reset'),
    path('password-reset-done/', PasswordResetDoneView.as_view(template_name="accounts/password_reset_done.html"),name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(template_name="accounts/password_reset_confirm.html",success_url=reverse_lazy('accounts:password_reset_complete')), name='password_reset_confirm'),
    path('password-reset-complete/', PasswordResetCompleteView.as_view(template_name="accounts/password_reset_complete.html"),name='password_reset_complete'),
]

htmx_urlpatterns = [
    path('check-username/', check_username, name="check_username"),
    path('check-email/', check_email, name='check_email'),
    path('edit-profile', profile_edit, name='edit_profile'),
]

urlpatterns += htmx_urlpatterns