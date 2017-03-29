from django.conf.urls import url
from stackoverflow import views


urlpatterns=[
    url(r'^$',views.IndexView,name='index'),
    url(r'^(?P<pk>[0-9]+)/$',views.DetailView,name='detail'),
    url(r'^(?P<pk>[0-9]+)/result/$',views.ResultsView,name='results'),
    url(r'^(?P<question_id>[0-9]+)/vote/$',views.vote,name='vote'),


]
