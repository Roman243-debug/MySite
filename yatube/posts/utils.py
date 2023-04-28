from django.core.paginator import Paginator

NUM_OF_POSTS = 10


def get_page_context(queryset, request):
    paginator = Paginator(queryset, NUM_OF_POSTS)
    page_number = request.GET.get('page')
    return paginator.get_page(page_number)
