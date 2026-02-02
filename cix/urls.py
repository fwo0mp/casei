from django.conf import settings
from django.urls import re_path, include
from django.contrib import admin
from django.contrib.auth import views as auth_views

from cix import views

urlpatterns = [
    re_path(r'^$', views.home, name='home'),
    re_path(r'^login/$', views.login_page),
    re_path(r'^do_login/$', views.do_login),
    re_path(r'^signup/$', views.signup),
    re_path(r'^do_signup/$', views.do_signup),
    re_path(r'^signup_thanks/$', views.signup_thanks),
    re_path(r'^do_logout/$', views.do_logout),
    re_path(r'^verify/([a-zA-Z0-9]+)/$', views.verify),
    re_path(r'^ncaa/', include('ncaacards.urls')),
    re_path(r'^password_reset/$', auth_views.PasswordResetView.as_view(
        success_url='/password_reset_sent/',
    ), name='password_reset'),
    re_path(r'^password_reset_sent/$', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    re_path(r'^password_reset_complete/$', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    re_path(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,40})/$',
        auth_views.PasswordResetConfirmView.as_view(success_url='/password_reset_complete/'), name='password_reset_confirm'),

    re_path(r'^yodawg/', admin.site.urls),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        re_path(r'^__debug__/', include(debug_toolbar.urls)),
    ]
