from user.models import User
from category.models import Category
from abc import ABC
from django.db.models import Q
from django.urls.base import reverse
from listing.models import Push, Pull


class Result:
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
    model = None

    def __init__(self, search_string):
        self.search_string = search_string
        self.query_set = self.get_query_set()
        self.objects = self.get_result_objects()

    def get_query_set(self):
        """ returns QuerySet """
        return self.model.objects.all()

    def get_result_objects(self):
        """ returns List of Objects """
        return self.get_query_set()  # [Result(obj) for obj in self.query_set]

    def get_results(self):
        return self.get_result_objects()


class UserSearch(SearchBase):
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
    model = Pull
    type = 'pull'


class SearchEngine:
    modules = [UserSearch, CategorySearch, PushSearch, PullSearch]

    def __init__(self, search_string):
        self.search_string = search_string

    def search_modules(self):
        results = {}
        for module in self.modules:
            results[module.type] = module(self.search_string).get_results()
        return results

    def sort_results(self):
        return self.search_modules()

    def get_results(self):
        return self.sort_results()
