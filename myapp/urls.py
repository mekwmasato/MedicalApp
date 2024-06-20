
from django.urls import path
from myapp import views

urlpatterns = [
    path('',views.IndexView.as_view(), name='index'),
]
