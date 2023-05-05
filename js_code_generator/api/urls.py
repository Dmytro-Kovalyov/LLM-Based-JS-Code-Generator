from django.urls import path
from . import views

urlpatterns = [
    path('generate-script/', views.GenerateScriptAPIView.as_view()),
    path('run-script/', views.RunScriptAPIView.as_view()),
]