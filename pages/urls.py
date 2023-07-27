from django.urls import path

from .views import HomePageView, AbountUsPageView

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('aboutus/', AbountUsPageView.as_view(), name='aboutus'),
]