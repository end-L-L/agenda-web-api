from django.contrib import admin
from django.urls import path
from .views import users

urlpatterns = [
   path('admin/', admin.site.urls),
   path('register/', users.RegisterView.as_view()),
]
