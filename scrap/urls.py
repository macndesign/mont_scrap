from django.conf.urls import url
from .views import extract

urlpatterns = [
    url(r'^$', extract, name='extract'),
]
