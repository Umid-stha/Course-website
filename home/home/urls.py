from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from . import views 
from django.conf.urls.static import static
from emails.views import verify_email, email_token_login

urlpatterns = [
    path('admin/', admin.site.urls),
    path('courses/', include('courses.urls')),
    path('', views.home), 
    path("verify/<uuid:token>/", verify_email),
    path('hx/login/', email_token_login)
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
