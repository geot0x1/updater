from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('logs/', views.logs),
    path('api/downloads_status/', views.downloads_status),
    path('api/downloads_status/clear/', views.clear_downloads),
    path('api/firmwares/', views.firmwares_api),
    path('upload/', views.upload),
    path('download/<str:firmware_id>/', views.download_firmware),
]
