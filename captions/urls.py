from django.urls import path
from .views import extract_subtitles, processing_status

urlpatterns = [
    path('', extract_subtitles, name='extract_subtitles'),
]