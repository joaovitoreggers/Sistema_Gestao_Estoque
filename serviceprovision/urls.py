from django.urls import path
from . import views

urlpatterns = [
    path("service/provision/list/", views.ServiceProvisionListView.as_view(), name="service_provision_list"),
    path("service/provision/create/", views.ServiceProvisionCreateView.as_view(), name="service_provision_create"),
    path("service/provision/<int:pk>/detail/", views.ServiceProvisionDetail.as_view(), name="service_provision_detail"),
]
