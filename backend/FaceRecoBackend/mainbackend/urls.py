from django.conf.urls import url
from .views import FileView

urlpatterns = [
  url(r'^add/$', FileView.as_view(), name='user-add'),
]