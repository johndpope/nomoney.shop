from tests_abc import TestCase
from deal.models import Deal, DealStatus
from user.models import User


class DealTestCase(TestCase):
    def test_deal_views(self):
        self.anon.get302('deal_list')
        self.user.get200('deal_list')

        self.anon.get302('deal_detail', url_args=self.deal.pk)
        self.user.get200('deal_detail', url_args=self.deal.pk)

        self.user.post302('deal_accepted', url_args=self.deal.pk, data={})
        self.deal.refresh_from_db()
        self.assertEqual(self.deal.status, DealStatus.ACCEPTED)

        data = {'user2': self.demo1.pk, 'location': self.location.pk}
        self.user.post302('deal_create', data=data)

        data = {'location': self.location.pk}
        self.user.get200('deal_user_create', url_args=self.demo1.pk)
        self.user.post302('deal_user_create', url_args=self.demo1.pk, data=data)

    def test_deal_model(self):
        # TODO Change procedure to a fresh started deal
        self.assertEqual(self.deal.status, DealStatus.PLACED)
        self.deal.set_placed()
        self.assertEqual(self.deal.status, DealStatus.PLACED)
        self.assertIsInstance(self.deal.partner_pulls, list)
        self.assertIsInstance(self.deal.get_users()[0], User)
        self.assertIsInstance(self.deal.get_users()[1], User)

        deal = Deal.by_users(self.deal.user2, self.deal.user1)[0]
        self.assertEqual(deal, self.deal)

        deal = Deal.by_users(
            self.random_object(User), self.random_object(User), create=True
            )[0]
        self.assertIsInstance(deal, Deal)

        deal = Deal.get_or_create((self.deal.user2, self.deal.user1))[0]
        self.assertEqual(deal, self.deal)

        self.deal.set_accepted()
        self.assertEqual(self.deal.status, DealStatus.ACCEPTED)

        self.assertEqual(self.deal.level, self.deal.level)
        self.assertEqual(self.deal.quality, self.deal.quality)

        self.assertIsInstance(self.deal.can_accept(self.deal.user1), bool)
        self.assertIsInstance(self.deal.can_accept(self.deal.user2), bool)
        self.assertNotEqual(
            self.deal.can_bid(self.deal.user1),
            self.deal.can_bid(self.deal.user2)
            )

