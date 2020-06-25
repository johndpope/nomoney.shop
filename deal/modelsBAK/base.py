from itertools import combinations


class DealSetBase:
    users = []
    deal_class = None

    def __init__(self):
        self.deal_class = DealBase
        self._deals = None
        self._quality = None
        self._level = None

    def get_users(self):
        return list(self.users)

    def set_users(self, *users):
        self.users = list(users)
        return self

    @property
    def deals(self):
        if self._deals is not None:
            return self._deals
        self._deals = []
        for user_combi in combinations(self.get_users(), 2):
            deal = self.deal_class()
            deal.dealset = self
            deal.set_users(user_combi)
            self._deals.append(deal)
        return self._deals

    @property
    def deal(self):
        return self.deals[0] if self.deals else []

    @property
    def level(self):
        """ Levels:
            0 - No Deal match
            1 - One side Match
            2 - Two side Match
            3 - Deal between three users
            4 - Deal between four users
        users represent all users taking part at this deal
        """
        if self._level is None:
            levels = [deal.level for deal in self.deals]
            self._level = max(levels) if levels else 0
        return self._level

    @property
    def quality(self):
        if self._quality is None:
            qualities = [deal.quality for deal in self.deals]
            self._quality = max(qualities) if qualities else 0
        return self._quality

    @property
    def pushs(self):
        push_qs = [user.pushs for user in self.get_users()]
        return push_qs[0].union(*push_qs)

    @property
    def pulls(self):
        pull_qs = [user.pulls for user in self.get_users()]
        return pull_qs[0].union(*pull_qs)

    @property
    def bids(self):
        bids = []
        for deal in self.deals:
            for bid in deal.bids:
                bids.append(bid)
        return bids

    @property
    def latest_bid(self):
        bids = self.bids
        return bids[-1] if bids else None

    def can_add_bid(self, me_):
        if not self.bids:
            return True
        elif self.latest_bid.creator != me_:
            return True
        return False

    def set_pov(self, user):
        for deal in self.deals:
            deal.set_pov(user)

    def __lt__(self, other):
        return self.quality > other.quality


class DealBase:
    users = []
    _user = None  # POV User of this instance
    dealset = None
    accepted = False

    def __init__(self):
        self.deal_class = None

    @property
    def user(self):
        return self._user or self.users[0]

    @user.setter
    def user(self, value):
        self._user = value

    @property
    def partner(self):
        if self.user:
            for user in self.get_users():
                if user != self.user:
                    return user
        else:
            return self.users[1]

    def get_users(self):
        return self.users

    def set_users(self, users):
        if not len(users) == 2:
            raise AttributeError("Need exactly 2 users for a single Deal")
        self.users = users

    @property
    def level(self):
        """ Levels:
            0 - No Deal match
            1 - One side Match
            2 - Two side Match
            3 - Deal between three users
            4 - Deal between four users
        users represent all users taking part at this deal
        """
        level = 0
        if self.pushs:
            level += 1
        if self.pulls:
            level += 1
        return level

    @property
    def quality(self):
        return len(self.pushs + self.pulls)

    @property
    def pushs(self):
        return list(self.intersection(self.user.pushs, self.partner.pulls))

    @property
    def pulls(self):
        return list(self.intersection(self.user.pulls, self.partner.pushs))

    def set_pov(self, user):
        if user in self.get_users():
            self.user = user

    @staticmethod
    def intersection(lst1, lst2):
        """ returns intersecting elements """
        for element in lst1:
            if element in lst2:
                yield element

    def __lt__(self, other):
        return self.quality < other.quality
