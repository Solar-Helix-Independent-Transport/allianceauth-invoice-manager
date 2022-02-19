from django.conf.urls import url

from . import views
from .api import api

app_name = 'invoices'

urlpatterns = [
    url(r'^$', views.show_invoices, name='list'),
    url(r'^r/$', views.react_main, name='r_list'),
    url(r'^admin/$', views.show_admin, name='admin'),
    url(r'^admin_create_tasks/$', views.admin_create_tasks,
        name='admin_create_tasks'),
    url(r'^api/', api.urls),

]
