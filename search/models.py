""" business models of the search module """
from abc import ABC
from django.db.models import Q
from django.urls.base import reverse
from user.models import User
from listing.models import Push, Pull
from category.models import Category


class Result:  # pylint: disable=too-few-public-methods
    """ this represents a result submitted as context """
    quality = 0
    title = 'title'
    text = 'text'
    url = 'url'
    breadcrumb = []
    type = 'Typ'

    def __init__(self, obj):
        self.object = obj

    def __lt__(self, other):
        return self.quality < other.quality


class SearchBase(ABC):
    """ Base class for a search module """
    model = None
    fields = []
    type = None
    url_name = None

    def __init__(self, search_string):
        self.search_string = search_string
        self.query_set = self.get_query_set()
        self.objects = self.get_result_objects()

    def get_query_set(self):
        """
        :returns: QuerySet(all objects of self.model)
        """
        return self.model.objects.filter(
                *self._create_basic_query(self.fields, self.search_string)
                )

    def get_url(self, obj):
        if isinstance(self.url_name, tuple):
            return reverse(self.url_name[0], args=(*self.url_name[1:], obj.pk))
        return reverse(self.url_name, args=(obj.pk,))

    def get_result_objects(self):
        """
        :returns: list of Result objects
        """
        results = []
        for obj in self.get_query_set():
            result = Result(obj)
            result.type = self.type
            if hasattr(obj, 'username'):
                result.title = obj.username
            else:
                result.title = obj.title
            result.url = self.get_url(obj)
            results.append(result)
        return results

    def get_results(self):
        """
        :returns: list of Result objects from self.get_result_objects()
        """
        return self.get_result_objects()

    @staticmethod
    def _create_basic_query(fields, search_string):
        for field in fields:
            field = field.replace('.', '__')
            yield Q(**{field + '__icontains': search_string})


class UserSearch(SearchBase):
    """ module to search for users """
    model = User
    fields = ['first_name', 'last_name', 'email', 'username']
    type = 'user'
    url_name = 'user_detail'


class CategorySearch(SearchBase):
    """ module to search for categories """
    model = Category
    fields = ['title', 'description']
    type = 'category'
    url_name = 'category_detail'


class PushSearch(SearchBase):
    """ module to search for pushs """
    model = Push
    fields = ['title', 'description', 'category.title']
    type = 'push'
    url_name = 'listing_detail', 'push'


class PullSearch(PushSearch):
    """ module to search for pulls """
    model = Pull
    type = 'pull'
    url_name = 'listing_detail', 'pull'


class SearchEngine:
    """ this is the interface that initiates the search modules """
    modules = [UserSearch, CategorySearch, PushSearch, PullSearch]

    def __init__(self, search_string):
        self.search_string = search_string

    def search_modules(self):
        """ fetches the Result objects of the search modules
        :returns: dict{module_type: [Results]}
        """
        results = {}
        for module in self.modules:
            results[module.type] = module(self.search_string).get_results()
        return results

    def sort_results(self):
        """ sorts the results
        :returns: dict{module_type: [Results]} -> sorted
        """
        return self.search_modules()

    def get_results(self):
        """ get the results - this ist the method to use from outside
        :returns: dict{module_type: [Results]}
        """
        return self.sort_results()
