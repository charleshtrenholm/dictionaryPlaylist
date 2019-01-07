from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^create$', views.create),
    url(r'^result$', views.result),
    url(r'^signup$', views.signup),
    url(r'^success$', views.success),
    url(r'^logout$', views.logout)
]