

from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('marks_system/',include('marks_system.urls')),
    path('admin/', admin.site.urls),
]
