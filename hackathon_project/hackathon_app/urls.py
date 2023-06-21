from django.urls import path
from .views import UserRegistrationView, LoginView, UserHackathonCreateView


urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login', LoginView.as_view(), name='login'),
    path('id/<int:user_id>/create-hackathon/', UserHackathonCreateView.as_view(), name='create-hackathon'),

]