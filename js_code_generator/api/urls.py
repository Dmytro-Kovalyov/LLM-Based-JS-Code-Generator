from django.urls import path
from . import views

urlpatterns = [
    path('generate/', views.GenerateScriptAPIView.as_view()),
    path('test/', views.RunScriptAPIView.as_view()),
    path('list_functions/', views.ListFunctionsAPIView.as_view())
]