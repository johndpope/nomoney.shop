from user.models import User


class Test_db:
    USER_COUNT = 10

    @classmethod
    def setup(cls):
        cls.setup_user_db()

    @classmethod
    def setup_user_db(cls):
        for i in range(cls.USER_COUNT):
            i = str(i + 1)
            User.objects.create(
                username='test' + i,
                first_name='first' + i,
                last_name='last' + i,
                email='test{}@local.local'.format(i),
                )
