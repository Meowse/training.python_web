from django.conf.urls import patterns, url

urlpatterns = patterns('myblog.views',
    url(r'^$',
        'list_view',
        name="blog_index"),

        #r'^posts/(\d+)/$',
		#r'^posts/(?P<post_id>\d+)/$',
    url(r'^posts/(\d+)/$',
		'post_detail_view',
        name="blog_detail"),
    url(r'^sample1/(\d+)/(?P<kwarg_1>\d+)/(\d+)/(?P<kwarg_2>\d+)/$',
		'stub_view',
        name="blog_stub"),
    url(r'^sample2/(\d+)/(\d+)/(\d+)/(\d+)/$',
		'stub_view',
        name="blog_stub"),
    url(r'^sample3/(?P<kwarg_0>\d+)/(?P<kwarg_1>\d+)/(?P<kwarg_2>\d+)/(?P<kwarg_3>\d+)/$',
		'stub_view',
        name="blog_stub"),
)