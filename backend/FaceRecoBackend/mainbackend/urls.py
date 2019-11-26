from django.conf.urls import url
from .views import Signup, Login

urlpatterns = [
  url(r'^add/$', Signup.as_view(), name='user-add'),
  url(r'^login/$', Login.as_view(), name='user-login')
]