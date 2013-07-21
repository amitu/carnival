import facebook, tempfile
from django.core.paginator import Paginator, InvalidPage
from django.template import loader, RequestContext
from django.http import Http404
from importd import d

def download_all_in(urls, folder): 
	pass

def create_collage(photo_urls):
	# download all photos to a folder
	tmp = tempfile.gettempdir()
	download_all_in(photo_urls, tmp)

	# https://scottlinux.com/2011/08/13/create-photo-collage-in-linux/
	# 
	# montage *.jpg -border 2x2 -background black +polaroid -resize 75% -geometry -60-60 -tile x6 final.jpg
	
	# other alternative: http://cs.colby.edu/courses/S09/cs151-labs/labs/lab06/

def post_photo_on_facebook(photo_url, message, tags, token):
	graph = facebook.GraphAPI(token)
	graph.put_photo(open(photo_file), message, tags=tags)


# object_list # {{{ 
# https://github.com/amitu/dutils/blob/master/dutils/utils.py#L1204
def object_list(request, queryset, paginate_by=None, page=None,
    allow_empty=True, template_name=None, template_loader=loader,
    extra_context=None, context_processors=None, template_object_name='object',
    mimetype=None, renderer=None, allow_json=True, jsoner=lambda x: x
):
    if extra_context is None: extra_context = {}
    queryset = queryset._clone()
    if paginate_by:
        paginator = Paginator(queryset, paginate_by, allow_empty_first_page=allow_empty)
        if not page:
            page = request.GET.get('page', 1)
        try:
            page_number = int(page)
        except ValueError:
            if page == 'last':
                page_number = paginator.num_pages
            else:
                # Page is not 'last', nor can it be converted to an int.
                raise Http404
        try:
            page_obj = paginator.page(page_number)
        except InvalidPage:
            raise Http404
        pagination_info = {
            'is_paginated': page_obj.has_other_pages(),
            'results_per_page': paginator.per_page,
            'has_next': page_obj.has_next(),
            'has_previous': page_obj.has_previous(),
            'page': page_obj.number,
            'next': page_obj.next_page_number(),
            'previous': page_obj.previous_page_number(),
            'first_on_page': page_obj.start_index(),
            'last_on_page': page_obj.end_index(),
            'pages': paginator.num_pages,
            'hits': paginator.count        
        }
        c = RequestContext(request, {
            '%s_list' % template_object_name: page_obj.object_list,
            'paginator': paginator,
            'page_obj': page_obj,
            'is_paginated': page_obj.has_other_pages(),
            'results_per_page': paginator.per_page,
            'has_next': page_obj.has_next(),
            'has_previous': page_obj.has_previous(),
            'page': page_obj.number,
            'next': page_obj.next_page_number(),
            'previous': page_obj.previous_page_number(),
            'first_on_page': page_obj.start_index(),
            'last_on_page': page_obj.end_index(),
            'pages': paginator.num_pages,
            'hits': paginator.count,
            'page_range': paginator.page_range,
            'pagination_info': pagination_info
        }, context_processors)
    else:
        c = RequestContext(request, {
            '%s_list' % template_object_name: queryset,
            'paginator': None,
            'page_obj': None,
            'is_paginated': False,
        }, context_processors)
        if not allow_empty and len(queryset) == 0:
            raise Http404
    for key, value in extra_context.items():
        if callable(value):
            c[key] = value()
        else:
            c[key] = value
    if not template_name:
        model = queryset.model
        template_name = "%s/%s_list.html" % (
            model._meta.app_label, model._meta.object_name.lower()
        )
    if allow_json and request.REQUEST.get("json"):
    	return d.JSONResponse(jsoner(c))
    if renderer:
        return d.HttpResponse(renderer(template_name, c))
    t = template_loader.get_template(template_name)
    return d.HttpResponse(t.render(c), mimetype=mimetype)
# }}} 