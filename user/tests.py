from tests_abc import TestCase
from testdb import TestDB
from .models import User
from django.urls.base import reverse


class UserTestCase(TestCase):
    def test_user_db(self):
        self.assertIs(len(User.objects.all()), TestDB.USER_COUNT + 2)

    def test_urls(self):
        # user_list
        self.anon.get302('user_list')

        # user_create
        new_user_name = 'demo2'
        new_user_pw = 'BuBuBu1234'
        self.user.get200('user_create')
        self.anon.get200('user_create')
        self.anon.post(
            reverse('user_create'),
            {'username': new_user_name,
             'password1': new_user_pw,
             'password2': new_user_pw}
            )
        new_user = User.objects.get(username='demo2')
        self.assertIsInstance(User.objects.get(username='demo2'), User)

        # user_pw
        data = {
            'old_password': new_user_pw,
            'new_password1': new_user_pw + 'a',
            'new_password2': new_user_pw + 'a'
            }
        self.user.post(reverse('user_pw'), data=data)

        # user_logout
        self.assertEqual(self.anon.get(reverse('user_update')).status_code, 200) 
        self.assertEqual(self.anon.post(reverse('user_logout')).status_code, 302)
        self.assertEqual(self.anon.get(reverse('user_update')).status_code, 302) 

        # user_login
        data = {'username': new_user_name, 'password': new_user_pw}
        self.assertEqual(self.anon.post(reverse('user_login'), data=data).status_code, 302)
        self.assertEqual(self.anon.get(reverse('user_update')).status_code, 200) 
        self.assertEqual(self.anon.post(reverse('user_logout')).status_code, 302)
        self.assertEqual(self.anon.get(reverse('user_update')).status_code, 302) 

        # user_update
        user = User.objects.get(username=TestDB.USER_NAME)
        kwargs = {'pk': user.pk}
        data = {'username': user.username, 'first_name':'fritz'}
        self.user.post(reverse('user_update'), data=data)
        user.refresh_from_db()
        self.assertEqual(user.first_name, 'fritz')

        # user_detail
        kwargs = {'pk': user.pk}
        self.assertIs(self.user.get(reverse('user_detail', kwargs=kwargs)).status_code, 200)
