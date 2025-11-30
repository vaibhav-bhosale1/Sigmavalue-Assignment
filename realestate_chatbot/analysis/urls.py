from django.urls import path
from .views import ChatAnalysisView, DownloadAnalysisView  # <--- Import the new view

urlpatterns = [
    path('chat/', ChatAnalysisView.as_view(), name='chat-analysis'),
    path('download/', DownloadAnalysisView.as_view(), name='download-analysis'), # <--- Add this line
]