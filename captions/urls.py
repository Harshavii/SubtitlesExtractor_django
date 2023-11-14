from django.urls import path
from .views import extract_subtitles

urlpatterns = [
    path('', extract_subtitles, name='extract_subtitles'),
]