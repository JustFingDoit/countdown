from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
     url(r'^$', 'triggers.views.home', name='home'),
     url(r'^create_user', 'triggers.views.create_user', name='create_user'),
     url(r'^login', 'triggers.views.login', name='login'),
    # url(r'^countdown/', include('countdown.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
