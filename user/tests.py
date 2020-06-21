from tests_abc import TestCase
from testdb import TestDB
from .models import User
from django.urls.base import reverse


class UserTestCase(TestCase):
    def test_user_db(self):
        self.assertIs(len(User.objects.all()), TestDB.USER_COUNT + 1)

    def test_urls(self):
        # user_list
        self.assertIs(self.anon.get_name('user_list').status_code, 200)

        #user_create
        new_user_name = 'demo2'
        new_user_pw = 'BuBuBu1234'
        self.assertIs(self.anon.get_name('user_create').status_code, 200)
        self.assertIs(self.user.get_name('user_create').status_code, 200)
        self.anon.post(
            reverse('user_create'),
            {'username': new_user_name,
             'password1': new_user_pw,
             'password2': new_user_pw}
            )
        new_user = User.objects.get(username='demo2')
        self.assertIsInstance(User.objects.get(username='demo2'), User)

        # user_pw
        kwargs = {'pk': new_user.pk}
        data = {
            'old_password': new_user_pw,
            'new_password1': new_user_pw + 'a',
            'new_password2': new_user_pw + 'a'
            }
        self.user.post(reverse('user_pw', kwargs=kwargs), data=data)

        # user_logout
        self.assertIs(self.anon.get(reverse('user_update', kwargs={'pk':1})).status_code, 200) 
        self.assertEquals(self.anon.post(reverse('user_logout')).status_code, 302)
        self.assertEquals(self.anon.get(reverse('user_update', kwargs={'pk':1})).status_code, 302) 

        # user_login
        data = {'username': new_user_name, 'password': new_user_pw}
        self.assertEquals(self.anon.post(reverse('user_login'), data=data).status_code, 302)
        self.assertIs(self.anon.get(reverse('user_update', kwargs={'pk':1})).status_code, 200) 

        # user_update
        user = User.objects.get(username=TestDB.USER_NAME)
        kwargs = {'pk': user.pk}
        data = {'username': user.username, 'first_name':'fritz'}
        self.user.post(reverse('user_update', kwargs=kwargs), data=data)
        user.refresh_from_db()
        self.assertEqual(user.first_name, 'fritz')

        # user_detail
        kwargs = {'pk': user.pk}
        self.assertIs(self.user.get(reverse('user_detail', kwargs=kwargs)).status_code, 200)
