from rest_framework.pagination import PageNumberPagination


class CategoryPagination(PageNumberPagination):
    page_size = 5


class GenrePagination(PageNumberPagination):
    page_size = 5


class TitlesPagination(PageNumberPagination):
    page_size = 5
