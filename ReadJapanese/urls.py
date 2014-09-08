from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth import views as auth_views

urlpatterns = [
    # Examples:
    url(r'^$', 'ReadJapanese.views.index', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^adduser/', 'ReadJapanese.views.adduser', name='adduser'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^login/$', auth_views.login, {'template_name': 'login.html'
                                        ''}, name='login'),
    url(r'^logout/$', 'ReadJapanese.views.logout_user', name='logout'),
    url(r'^kana/', include('kana.urls', namespace="kana")),
]
