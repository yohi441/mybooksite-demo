from accounts.models import Profile
from django.contrib.auth.models import User
import pytest






@pytest.mark.django_db
def test_create_user():
    User.objects.create(username="testusername", password="testpassword")
    count = User.objects.all().count()
    user = User.objects.get(pk=1)
    assert count == 1
    assert user.username == "testusername"
    assert user.password == "testpassword"



@pytest.mark.django_db
def test_update_user():
    User.objects.create(username="testusername", password="testpassword")
    user = User.objects.get(pk=1)

    user.username = 'test1username'
    user.password = 'test2password'

    assert user.username == "test1username"
    assert user.password == "test2password"

@pytest.mark.django_db
def test_delete_user():
    User.objects.create(username="testusername", password="testpassword")
    user = User.objects.get(pk=1)
    count = User.objects.all().count()
    assert count == 1
    user.delete()
    assert User.objects.all().count() == 0


@pytest.mark.django_db
def test_create_profile():
    user = User.objects.create(username="testusername", password="testpassword")
    
    profile = Profile.objects.get(user=user)

    assert profile.user.username == 'testusername'
    assert profile.user.password == 'testpassword'
    assert profile.address == None
    assert profile.cellphone_number == None
    assert profile.gender == None


@pytest.mark.django_db
def test_update_profile():
    user = User.objects.create(username="testusername", password="testpassword")
    
    profile = Profile.objects.get(user=user)
    profile.address="testaddress" 
    profile.cellphone_number=1209233412
    profile.gender="Male"

    assert profile.user.username == 'testusername'
    assert profile.user.password == 'testpassword'
    assert profile.address == 'testaddress'
    assert profile.cellphone_number == 1209233412
    assert profile.gender == "Male"

@pytest.mark.django_db
def test_delete_profile():
    user = User.objects.create(username="testusername", password="testpassword")
    
    assert Profile.objects.all().count() == 1
    user.delete()
    assert Profile.objects.all().count() == 0

    