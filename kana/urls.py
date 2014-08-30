from django.conf.urls import url
from kana import views

urlpatterns = [
    # ex: /kana/
    url(r'^$', views.index, name='index'),
    # ex: /kana/test/
    url(r'^test/', views.test, name='test'),
    # ex: /kana/5/
    url(r'^(?P<kana_id>[0-9]+)/$', views.detail, name='detail'),
    # ex: /kana/5/results/
    url(r'^(?P<kana_id>[0-9]+)/results/$', views.results, name='results'),

    
]


