from django.conf.urls import url

from . import views
app_name = 'invoices'

urlpatterns = [
    url(r'^$', views.show_invoices, name='list'),
]