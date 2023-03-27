from rest_framework.pagination import PageNumberPagination


class MainPagination(PageNumberPagination):
    page_size = 6
    page_size_query_param = 'limit'


class RecipePagination(MainPagination):
    pass

class SubscriptionPagination(MainPagination):
    pass
    