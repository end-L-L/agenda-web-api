from django.views.generic.base import RedirectView
from django.contrib import admin
from django.urls import path
from .views import users
from .views import auth
from .views import personal_contact_directory as personal_contact
from .views import business_contact_directory as business_contact

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),
    # Home Redirect
    path('', RedirectView.as_view(url='/admin/', permanent=True)),
    # Create User
    path('register/', users.RegisterView.as_view()),
    # Get User by ID
    path('profile/', users.RegisterView.as_view()),
    # Login
    path('token/', auth.CustomAuthToken.as_view()),
    # Logout
    path('logout/', auth.Logout.as_view()),    
    
    # Personal Contact Directory
    
    # Register Personal Contact
    path('register-personal-contact/', personal_contact.PersonalContactRV.as_view()),
    # Edit Personal Contact
    path('edit-personal-contact/', personal_contact.PersonalContactEV.as_view()),
    # Delete Personal Contact
    path('delete-personal-contact/', personal_contact.PersonalContactEV.as_view()),
    # All Personal Contacts by User
    path('list-personal-contacts/', personal_contact.PersonalContactByUser.as_view()),

    # Business Contact Directory

    # Register Business Contact
    path('register-business-contact/', business_contact.BusinessContactRV.as_view()),
    # Edit Business Contact
    path('edit-business-contact/', business_contact.BusinessContactEV.as_view()),
    # Delete Business Contact
    path('delete-business-contact/', business_contact.BusinessContactEV.as_view()),
    # All Business Contacts by User
    path('list-business-contacts/', business_contact.BusinessContactByUser.as_view()),
]

