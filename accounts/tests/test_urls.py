from django.urls import reverse, resolve


def test_accounts_url():
    path = reverse('accounts:profile')
    assert resolve(path).view_name == 'accounts:profile'

def test_login_url():
    path = reverse('accounts:login')
    assert resolve(path).view_name == 'accounts:login'

def test_logout_url():
    path = reverse('accounts:logout')
    assert resolve(path).view_name == 'accounts:logout'

def test_register_success_url():
    path = reverse('accounts:register_success')
    assert resolve(path).view_name == 'accounts:register_success'

def test_register_url():
    path = reverse('accounts:register')
    assert resolve(path).view_name == 'accounts:register'

def test_password_change_url():
    path = reverse('accounts:password_change')
    assert resolve(path).view_name == 'accounts:password_change'

def test_password_change_done_url():
    path = reverse('accounts:password_change_done')
    assert resolve(path).view_name == 'accounts:password_change_done'

def test_password_reset_url():
    path = reverse('accounts:password_reset')
    assert resolve(path).view_name == 'accounts:password_reset'

def test_password_reset_done_url():
    path = reverse('accounts:password_reset_done')
    assert resolve(path).view_name == 'accounts:password_reset_done'

# def test_password_reset_confirm_url():
#     path = reverse('accounts:password_reset_confirm')
#     assert resolve(path).view_name == 'accounts:password_reset_confirm'

def test_password_reset_complete_url():
    path = reverse('accounts:password_reset_complete')
    assert resolve(path).view_name == 'accounts:password_reset_complete'

def test_check_username_url():
    path = reverse('accounts:check_username')
    assert resolve(path).view_name == 'accounts:check_username'

def test_check_email_url():
    path = reverse('accounts:check_email')
    assert resolve(path).view_name == 'accounts:check_email'

def test_edit_profile_url():
    path = reverse('accounts:edit_profile')
    assert resolve(path).view_name == 'accounts:edit_profile'


