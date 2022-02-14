from accounts.forms import ProfileForm, RegisterForm
import pytest




def test_profile_form_valid_data():
    form = ProfileForm(data={

    'first_name': 'testfirstname',
    'last_name': 'testlastname',
    'email':'test@email.com',
    'address':'testaddress',
    'gender':'Male',
    'cellphone_number':1234567890,
    'avatar': '',
    })

    assert form.is_valid() == True

def test_profile_form_invalid_email():
    form = ProfileForm(data={

    'first_name': 'testfirstname',
    'last_name': 'testlastname',
    'email':'testemail.com',
    'address':'testaddress',
    'gender':'Male',
    'cellphone_number':1234567890,
    'avatar': '',
    })

    assert form.is_valid() == False


def test_profile_form_invalid_data():
    form = ProfileForm(data={})

    assert form.is_valid() == False
    assert len(form.errors) == 6


@pytest.mark.django_db
def test_register_form_valid_data():

    form = RegisterForm(data={
        'email': 'test@email.com',
        'username': 'username',
        'password1': 'testpassword',
        'password2': 'testpassword',
    })

    assert form.is_valid() == True

def test_register_form_invalid_data():

    form = RegisterForm(data={})

    assert form.is_valid() == False
    assert len(form.errors) == 4


@pytest.mark.django_db
def test_register_form_invalid_email():

    form = RegisterForm(data={
        'email': 'testemail.com',
        'username': 'username',
        'password1': 'testpassword',
        'password2': 'testpassword',
    })

    assert form.is_valid() == False
    assert len(form.errors) == 1

@pytest.mark.django_db
def test_register_form_mismatch_password():

    form = RegisterForm(data={
        'email': 'testemail.com',
        'username': 'username',
        'password1': 'test1password',
        'password2': 'testpassword',
    })

    assert form.is_valid() == False
    assert len(form.errors) == 2