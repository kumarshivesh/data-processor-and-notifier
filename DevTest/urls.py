from django.contrib import admin
from django.urls import include, path
from fileupload import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('fileupload.urls')),
]
