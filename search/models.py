from user.models import User


class Search:
    results = []
    modules = []


class SearchResult:
    value = None


class SearchModuleBase:
    model = User
