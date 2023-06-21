from django.urls import path
from .views import UserRegistrationView, LoginView, UserHackathonCreateView, UserHackathonUpdateView, \
    UserHackathonDeleteView, HackathonListView, EnrollHackathonView, SubmitHackathonView, EnrolledHackathonListView, UserSubmissionsView


urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login', LoginView.as_view(), name='login'),
    path('id/<int:user_id>/create-hackathon/', UserHackathonCreateView.as_view(), name='create-hackathon'),
    path('id/<int:user_id>/update/hackathon-id/<int:hackathon_id>/', UserHackathonUpdateView.as_view(),
         name='hackathon-update-delete'),
    path('id/<int:user_id>/delete/hackathon-id/<int:hackathon_id>/', UserHackathonDeleteView.as_view(),
         name='hackathon-update-delete'),
    path('list-hackathon/', HackathonListView.as_view(), name='hackathon-list'),
    path('enroll-hackathon/user-id/<int:user_id>/hackathon-id/<int:hackathon_id>/', EnrollHackathonView.as_view(), name='enroll_hackathon'),
    path('submit-hackathon/user_id/<int:user_id>/hackathon_id/<int:hackathon_id>/', SubmitHackathonView.as_view(), name='submit_hackathon'),
    path('users/<int:user_id>/enrolled-hackathons/', EnrolledHackathonListView.as_view(), name='enrolled-hackathon-list'),
    path('users/<int:user_id>/hackathons/<int:hackathon_id>/submissions/', UserSubmissionsView.as_view(), name='user-submissions'),


]