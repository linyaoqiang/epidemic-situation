from django.core.paginator import Paginator, EmptyPage
class SelfPaginator(Paginator):
    def __init__(self, object_list, page_size, page_number, display_size=10):
        super().__init__(object_list, page_size)
        self.pages = []
        self.has_more = False
        self.init_pages(page_number, display_size)

    def init_pages(self, page_number, display_size):

        if page_number - (display_size // 2) > 0:
            left = page_number - (display_size // 2)
        else:
            left = 1
        right = left + display_size - 1
        if right > self.num_pages:
            right = self.num_pages
            left = right - display_size + 1
            if left < 0:
                left = 1
        pages = [index for index in range(left, right + 1)]
        if right < self.num_pages:
            self.has_more = True

        self.pages = pages