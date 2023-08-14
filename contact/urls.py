from django.urls import path
from contact.views import IdentityAPIView

urlpatterns = [
    path('/identity', IdentityAPIView.as_view())
]