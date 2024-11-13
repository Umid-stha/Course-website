from . import views
from django.urls import path


urlpatterns = [
    path('', views.course_list),
    path('<slug:id>', views.course_detail),
    path('<slug:c_id>/lessons/<slug:l_id>', views.lesson_detail),
] 