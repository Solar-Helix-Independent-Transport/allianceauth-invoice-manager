from django.urls import re_path

from . import views
from .api import api

app_name = 'invoices'

urlpatterns = [
    re_path(r'^$', views.show_invoices, name='list'),
    re_path(r'^r/$', views.react_main, name='r_list'),
    re_path(r'^admin/$', views.show_admin, name='admin'),
    re_path(r'^admin_create_tasks/$', views.admin_create_tasks,
            name='admin_create_tasks'),
    re_path(r'^api/', api.urls),

]
