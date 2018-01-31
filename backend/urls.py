from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^add_message/$', views.add_message),
    url(r'^show_messages/$', views.show_messages)
]
