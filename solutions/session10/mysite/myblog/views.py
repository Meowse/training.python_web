from django.shortcuts import render
import datetime
from django.utils.timezone import utc
from django.http import HttpResponse, HttpResponseRedirect, Http404

from models import Post

def stub_view(request, *args, **kwargs):
    body = "Stub View\n\n"
    if args:
        body += "Args:\n"
        body += "\n".join(["\t%s" % a for a in args])
    if kwargs:
        body += "\n\nKwargs:\n"
        body += "\n".join(["\t%s: %s" % i for i in kwargs.items()])
    if request.GET:
        body += "\n\nGET query parameters:\n"
        body += "\n".join(["\t%s: %s" % i for i in request.GET.items()])
    if request.POST:
        body += "\n\nPOST query parameters:\n"
        body += "\n".join(["\t%s: %s" % i for i in request.POST.items()])
        
    return HttpResponse(body, content_type="text/plain")

#from django.template import loader, RequestContext

#    template = loader.get_template('list.html')
#    context = RequestContext(request, {
#        'posts': posts,
#    })
#    body = template.render(context)
#    return HttpResponse(body, content_type="text/html")

def list_view(request):
    now = datetime.datetime.utcnow().replace(tzinfo=utc)
    published = Post.objects.exclude(published_date__exact=None).exclude(published_date__gt=now)
    posts = published.order_by('-published_date')
    return render(request, 'list.html', {'posts': posts})

def post_detail_view(request, post_id):
#    published = Post.objects.exclude(published_date__exact=None)
#    post = published.get(pk=post_id)
#    raise Http404("query was: " + post.query);
    try:
        post = Post.objects.get(pk__exact=post_id)
    except:
        raise Http404("Post does not exist")
    now = datetime.datetime.utcnow().replace(tzinfo=utc)
    if post.published_date == None or post.published_date > now:
        raise Http404("Post does not exist")
    return render(request, 'post.html', {'post': post})


def detail_view(request, post_id):
    published = Post.objects.exclude(published_date__exact=None)
    try:
        post = published.get(pk=post_id)
    except Post.DoesNotExist:
        raise Http404
    context = {'post': post}
    return render(request, 'detail.html', context)