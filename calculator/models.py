""" models for the calculator module """
from itertools import combinations
from deal.models import Deal
from config.settings import LOGGER


class VirtualDeal(Deal):
    """ proxy model for deal to calculate deals that not (need to) exist """
    status = 0

    @classmethod
    def combinated(cls, *users, me_=None):
        """ get possible deal combinations of users
        :param *users: users, deals should be created for
        :param me_: User as point of view
        :returns: list of deals
        """
        deals = []
        combis = [combi for combi in combinations(users, 2)
                  if combi[0] and combi[1]]
        for user1, user2 in combis:
            if me_ and user2 == me_:
                user1, user2 = user2, user1
            deals.append(cls.by_user(user1, user2, level=0))
        return deals

    @staticmethod
    def _calculate_max_quality(deals):
        """
        :returns: int max quality from a set of deals
        """
        return max((deal.quality for deal in deals)) if deals else 0

    @staticmethod
    def _calculate_quality_pct(deals, max_quality):
        """ adds deal.quality to each deal """
        # Calculate Quality Percentage of each deal (for view/css)
        for deal in deals:
            deal.max_quality = max_quality
            if max_quality == 0:
                deal.quality_pct = 100
            else:
                deal.quality_pct = int(deal.quality / max_quality * 100 + 0.5)

    @classmethod
    def by_users(cls, me_, other_users, level=2):  # pylint: disable=arguments-differ
        """ get deal between me_ and other_users
        :param me_: User as point of view
        :param other_users: users, deals should be created for
        :param level: int of deal level you want to get (default: 2)
        :returns: list of deals, sorted by quality
        """
        deals = []
        # Calculate possible Deals
        for user in other_users:
            deal = cls(user1=me_, user2=user)
            if deal.level >= level:
                deals.append(deal)

        cls._calculate_quality_pct(deals, cls._calculate_max_quality(deals))
        if deals:
            log_str = 'Calculator: Found {} possible deals.'.format(str(len(deals)))
            LOGGER.info(log_str)
        return sorted(deals, key=lambda x: x.quality, reverse=True)

    @classmethod
    def by_user(cls, me_, partner, level=2):
        """ get deal between me_ and partner
        :param me_: User as point of view
        :param partner: deal partner
        :param level: int of deal level you want to get (default: 2)
        :returns: list of deals, sorted by quality
        """
        deals = cls.by_users(me_, [partner], level=level)
        return deals[0] if deals else None

    def save(self):  # pylint: disable=arguments-differ
        pass

    class Meta:
        proxy = True
