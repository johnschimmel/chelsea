from django.conf.urls import patterns, include, url

# feeds
from blog.feeds import LatestEntriesFeed

# Uncomment the next two lines to enable the admin:
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'blog.views.index', name='index'),
    
    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<slug>[-\w]+)/$', 
    	'blog.views.view_post', 
    	name='view_blog_post'),
	
    url(r'^category/(?P<categorySlug>[^\.]+)', 
		'blog.views.view_category', 
		name='view_blog_category'
	),
	url(r'^feeds/latest/$', LatestEntriesFeed()),
    # url(r'^$', 'chelsea.views.home', name='home'),
    # url(r'^chelsea/', include('chelsea.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^ckeditor/', include('ckeditor.urls')),
)
