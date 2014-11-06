from django.conf.urls import patterns, include, url
from django.contrib import admin
from route_recommendation import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'TravelRouteRecommendation.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    # url(r'^$', include('route_recommendation.urls')),
    url(r'^$', views.index, name='index'),
    url(r'^landmarks$', views.extract_landmarks),
    url(r'^landmarks/(?P<location>[0-9]+)$', views.extract_landmarks)
)
