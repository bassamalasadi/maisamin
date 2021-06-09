from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from main import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path("password_reset", auth_views.PasswordResetView.as_view(template_name="account_reset_password"),
         name="password_reset"),
    path('', include('main.urls', namespace='main')),
    path('ratings/', include('star_ratings.urls', namespace='ratings')),
    url(r'^media/(?P<path>.*)$', serve, {'document_root':
        settings.MEDIA_ROOT}),
    url(r'^static/(?P<path>.*)$', serve, {'document_root':
        settings.STATIC_ROOT}),
]


urlpatterns += static(settings.MEDIA_URL,
                      document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL,
                      document_root=settings.STATIC_ROOT)
