from django.urls import path
from .views import extract_subtitles, processing_status

urlpatterns = [
    path('', extract_subtitles, name='extract_subtitles'),
    path('processing/<str:task_id>/', processing_status, name='processing_status'),
]