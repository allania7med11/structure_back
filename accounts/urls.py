from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from accounts import views as accounts_views
from django.urls import path, include
from django.views.generic import TemplateView

urlpatterns = [
    path('social-auth/', include('social_django.urls', namespace="social")),
    # path('', TemplateView.as_view(template_name='home.html'), name='home'),
    url(r'^signup/$', accounts_views.signup, name='signup'),
    url(r'^login/$', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    # path(r'^login/$', accounts_views.login, name="login"),
    path("", accounts_views.home, name="home"),
    url(r'^logout/$', auth_views.LogoutView.as_view(), name='logout'),

    url(r'^reset/$',
        auth_views.PasswordResetView.as_view(
            template_name='password_reset.html',
            email_template_name='password_reset_email.html',
            subject_template_name='password_reset_subject.txt'
        ),
        name='password_reset'),
    url(r'^reset/done/$',
        auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'),
        name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'),
        name='password_reset_confirm'),
    url(r'^reset/complete/$',
        auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'),
        name='password_reset_complete'),

    url(r'^password/change$', auth_views.PasswordChangeView.as_view(template_name='password_change.html'),
        name='password_change'),
    url(r'^password/change/done$', auth_views.PasswordChangeDoneView.as_view(template_name='password_change_done.html'),
        name='password_change_done'),
]
