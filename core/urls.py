from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from . import views

urlpatterns = [
    path("register/", views.register_view),
    path("login/", TokenObtainPairView.as_view()),
    path("token/refresh/", TokenRefreshView.as_view()),

    path("rewrite/", views.rewrite_view),

    path("history/", views.list_history_view),
    path("history/save/", views.save_history_view),
    path("history/<int:pk>/", views.delete_history_view),

    path("export/pdf/<int:pk>/", views.export_pdf_view),

    path("voice/", views.voice_view),
    path("speech-to-text/", views.speech_to_text_view),
]

