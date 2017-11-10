from django.conf import settings
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render

from wagtail.wagtailcore.models import Page
from wagtail.wagtailsearch.models import Query

from blog.models import BlogPage


def search(request):
    search_query = request.GET.get('q', None)
    if search_query:
        if 'elasticsearch' in settings.WAGTAILSEARCH_BACKENDS['default']['BACKEND']:
            search_results = Page.objects.live().search(search_query)
        else:
            blog_results = BlogPage.objects.live().search(search_query)
            blog_page_ids = [p.page_ptr.id for p in blog_results]

        query = Query.get(search_query)

        # Record hit
        query.add_hit()

    else:
        search_results = Page.objects.none()

    # Pagination
    page = request.GET.get('page', 1)
    paginator = Paginator(search_results, 10)
    try:
        search_results = paginator.page(page)
    except PageNotAnInteger:
        search_results = paginator.page(1)
    except EmptyPage:
        search_results = paginator.page(paginator.num_pages)

    return render(request, 'search/search_results.html', {
        'search_query': search_query,
        'search_results': search_results,
    })
