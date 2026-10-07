from django.contrib import admin
from django.urls import path
from accounts import views as acc_views
from dashboard import views as dash_views
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name="home.html"), name='home'),

    path('login/', acc_views.login_view, name='login'),
    path('register/', acc_views.register_view, name='register'),
    path('logout/', acc_views.logout_view, name='logout'),

    path('dashboard/', dash_views.dashboard_view, name='dashboard'),
    path('predict/', dash_views.predict_view, name='predict'),
    path('history/', dash_views.history_view, name='history'),
    path('profile/', dash_views.profile_page, name='profile'),
    path('my-predictions/', dash_views.my_predictions, name='my_predictions'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
