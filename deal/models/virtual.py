from .base import DealBase, DealSetBase


class DealVirtual(DealBase):
    users = []
    is_virtual = True


class DealSetVirtual(DealSetBase):
    users = []
    is_virtual = True
    deal_class = DealVirtual
