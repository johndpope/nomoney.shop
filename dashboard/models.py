from django.db import models
from deal.models import Deal


class VirtualDeal(Deal):

    @classmethod
    def by_users(cls, me_, other_users, level=2):
        deals = []
        # Calculate possible Deals
        for user in other_users:
            deal = cls(user1=me_, user2=user)
            if deal.level == level:
                deals.append(deal)

        # Calculate max Quality
        max_quality = max(
                (deal.quality for deal in deals)
            ) if deals else 0

        # Calculate Quality Percentage of each deal (for view/css)
        for deal in deals:
            deal.max_quality = max_quality
            deal.quality_pct = int(deal.quality / max_quality * 100 + 0.5)

        return sorted(deals, key=lambda x: x.quality, reverse=True)

    class Meta:
        proxy = True
