from django.urls import path

from . import views

app_name = 'views'
urlpatterns = [
    path(r'', views.IndexView.as_view(), name='index'),
    path('submit/', views.submit, name='submit'),
    path('update/<int:pk>/', views.update, name='update'),
    path('show/<int:pk>/', views.ShowView.as_view(), name='show'),
    path('search/', views.search, name='search'),
    path('skim/', views.keywords, name='skim'),
]