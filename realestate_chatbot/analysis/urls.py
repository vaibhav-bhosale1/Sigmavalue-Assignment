from django.urls import path
from .views import ChatAnalysisView

urlpatterns = [
    path('chat/', ChatAnalysisView.as_view(), name='chat-analysis'),
]