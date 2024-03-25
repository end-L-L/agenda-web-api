from django.views.generic.base import RedirectView
from django.contrib import admin
from django.urls import path
from .views import users
from .views import auth
from .views import contact_register

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),
    # Home Redirect
    path('', RedirectView.as_view(url='/admin/', permanent=True)),
    # Create User
    path('register/', users.RegisterView.as_view()),
    # Login
    path('token/', auth.CustomAuthToken.as_view()),
    # Logout
    path('logout/', auth.Logout.as_view()),    
    # Register Personal Contact
    path('register-personal-contact/', contact_register.PersonalContactRV.as_view()),
    # Register Business Contact
    #path('register-bc/', users.BusinessContactView.as_view()),
]