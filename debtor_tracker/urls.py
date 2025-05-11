# debtor_tracker/urls.py

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from debts import views as debt_views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),

    # Authentication
    path('accounts/login/',
         auth_views.LoginView.as_view(
             template_name='registration/login.html',
             redirect_authenticated_user=True
         ),
         name='login'),
    path('login/',
         auth_views.LoginView.as_view(
             template_name='registration/login.html',
             redirect_authenticated_user=True
         ),
         name='login'),
    path('accounts/register/',
         debt_views.register,
         name='register'),
    path('accounts/profile/',
         debt_views.profile,
         name='profile'),
    path('logout/',
         auth_views.LogoutView.as_view(next_page='login'),
         name='logout'),

    # Debts app (root)
    path('', include('debts.urls')),
]

# Serve uploaded media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
