from .base import DealBase, DealSetBase


class DealSetVirtual(DealSetBase):
    users = []
    is_virtual = True


class DealVirtual(DealBase):
    users = []
    is_virtual = True
