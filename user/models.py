from django.contrib.auth.models import AbstractUser
from django.db import models
from deal.models import DealSet, DealSetVirtual

#===============================================================================
# 
# class DealSet:
#     """
#     Levels:
#         0 - No Deal match
#         1 - One side Match
#         2 - Two side Match
#         3 - Deal between three users
#         4 - Deal between four users
# 
#     users represent all users taking part at this deal
#     """
#     def __init__(self, user, partners):
#         self.user = user
#         self.partners = [partners] if isinstance(partners, User) else partners
#         self.deals = self.get_deals()
#         self.level = self.get_level()
#         self.quality = self.get_quality()
# 
#     @property
#     def deal(self):
#         """ returns deal if single, else raises exeption """
#         deals = self.get_deals()
#         if len(deals) != 1:
#             raise AttributeError("Multiple Deals in Dealset")
#         return deals[0]
# 
#     def get_level(self):
#         return max([deal.level for deal in self.deals])
# 
#     def get_quality(self):
#         return max([deal.quality for deal in self.deals])
# 
#     def get_deals(self):
#         """ Calculate all deal constellations """
#         return [Deal(self.user, partner) for partner in self.partners]
# 
# 
# class Deal:
#     """ These deals are for only two persons, ever!
#     So level3 and up needs multiple Deals
#     """
#     def __init__(self, user, partner):
#         self.user = user
#         self.partner = partner
#         self.pushs, self.pulls = self.get_intersecting()
#         self.level = self.get_level()
#         self.quality = self.get_quality()
# 
#     def get_level(self):
#         level = 0
#         if self.pushs:
#             level += 1
#         if self.pulls:
#             level += 1
#         return level
# 
#     def get_quality(self):
#         return len(self.pushs + self.pulls)
# 
#     def get_intersecting(self):
#         """ returns intersecting pushs, pulls """
#         return list(self.intersection(self.user.pushs, self.partner.pulls)), \
#             list(self.intersection(self.user.pulls, self.partner.pushs))
# 
#     @staticmethod
#     def intersection(lst1, lst2):
#         """ returns intersecting elements """
#         for element in lst1:
#             if element in lst2:
#                 yield element
# 
#     def __repr__(self):
#         return 'Deal: ' + str(self)
# 
#     def __str__(self):
#         return '{} vs. {}'.format(self.user, self.partner)
#===============================================================================


class User(AbstractUser):

    @property
    def other_users(self):
        return self.__class__.objects.exclude(pk=self.pk)

    @property
    def pushs(self):
        return self.push_set.all()

    @property
    def pulls(self):
        return self.pull_set.all()

    @property
    def listings(self):
        """ returns list of listings (pushs and pulls) """
        return list(self.pushs) + list(self.pulls)

    @property
    def bids(self):
        return sorted(
            {*self.bids_sent.all(), *self.bids_received.all()},
            key=lambda x: x.datetime
            )

    @property
    def dealsets(self):
        dealsets = self.dealset_set.all()
        for dealset in dealsets:
            dealset.set_pov(self)
        return dealsets

    def possible_dealsets(self):
        """ returns a list of possible dealsets """
        dealsets_virtual = []
        for partner in self.other_users:
            dealset_virtual = DealSetVirtual()
            dealset_virtual.users = (self, partner)
            dealsets_virtual.append(dealset_virtual)
        return dealsets_virtual


#===============================================================================
#     def get_dealsets(self):
#         import pdb; pdb.set_trace()  # <---------
# #===============================================================================
# #         import pdb; pdb.set_trace()  # <---------
# #         level = {1: [], 2: [], 3: []}
# # 
# #         for partner in self.get_partners():
# #             dealset = DealSet(self, partner)
# #             level.get(dealset.level).append(dealset)
# # 
# #         return [], \
# #             sorted(level[1], key=lambda x: x.quality, reverse=True), \
# #             sorted(level[2], key=lambda x: x.quality, reverse=True), \
# #             sorted(level[3], key=lambda x: x.quality, reverse=True)
# #===============================================================================
# 
#     def get_matches(self):
#         matches = []
#         for listing in self.listings:
#             matches += listing.get_matches()
#         return matches
# 
#     def get_matches_by_partner(self, partner):
#         import pdb; pdb.set_trace()  # <---------
# 
#     def get_dealset_from_partner(self, partner):  # WEG?
#         """ returns a Dealset for a Deal between self and partner """
#         return DealSet(self, partner)
# 
#     def level1(self):
#         """ ich habe was du brauchst und du hast was ich brauche """
#         return self.get_dealsets()[1]
# 
#     def level2(self):
#         """ ich habe was du brauchst ODER du hast was ich brauche """
#         return self.get_dealsets()[2]
# 
#     def level3(self):
#         return
#===============================================================================
