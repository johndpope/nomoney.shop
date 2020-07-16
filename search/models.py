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

    def __init__(self, search_string):
        self.search_string = search_string
        self.query_set = self.get_query_set()
        self.objects = self.get_result_objects()

    def get_query_set(self):
        """
        :returns: QuerySet(all objects of self.model)
        """
        return self.model.objects.all()

    def get_result_objects(self):
        """
        :returns: list of Result objects
        """
        return self.get_query_set()  # [Result(obj) for obj in self.query_set]

    def get_results(self):
        """
        :returns: list of Result objects from self.get_result_objects()
        """
        return self.get_result_objects()


class UserSearch(SearchBase):
    """ module to search for users """
    model = User
    type = 'user'

    def get_query_set(self):
        result = self.model.objects.filter(
            Q(first_name__icontains=self.search_string) |
            Q(last_name__icontains=self.search_string) |
            Q(email__icontains=self.search_string) |
            Q(username__icontains=self.search_string)
            )
        return result

    def get_result_objects(self):
        results = []
        for obj in self.get_query_set():
            result = Result(obj)
            result.type = self.type
            result.title = obj.username
            result.url = reverse('user_detail', args=(obj.pk,))
            results.append(result)
        return results


class CategorySearch(SearchBase):
    """ module to search for categories """
    model = Category
    type = 'category'

    def get_query_set(self):
        result = self.model.objects.filter(
            Q(title__icontains=self.search_string) |
            Q(description__icontains=self.search_string)
            )
        return result

    def get_result_objects(self):
        results = []
        for obj in self.get_query_set():
            result = Result(obj)
            result.type = self.type
            result.title = obj.title
            result.url = reverse('category_detail', args=(obj.pk,))
            results.append(result)
        return results


class PushSearch(SearchBase):
    """ module to search for pushs """
    model = Push
    type = 'push'

    def get_query_set(self):
        result = self.model.objects.filter(
            Q(title__icontains=self.search_string) |
            Q(description__icontains=self.search_string) |
            Q(category__title__icontains=self.search_string)
            )
        return result

    def get_result_objects(self):
        results = []
        for obj in self.get_query_set():
            result = Result(obj)
            result.type = self.type
            result.title = obj.title
            result.url = reverse('category_detail', args=(obj.pk,))
            results.append(result)
        return results


class PullSearch(PushSearch):
    """ module to search for pulls """
    model = Pull
    type = 'pull'


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
