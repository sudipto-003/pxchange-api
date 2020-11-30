from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

class CustomPaginator(PageNumberPagination):
    page_size = 5

    def get_paginated_response(self, data):
        return Response({
            'next_page': self.get_next_link(),
            'previous_page': self.get_previous_link(),
            'count': self.page.paginator.count,
            'total_pages': self.page.paginator.num_pages,
            'cur_page': self.page.number,
            'results': data
        })