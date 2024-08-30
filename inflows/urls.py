from django.urls import path
from . import views

urlpatterns = [
    path("inflows/list/", views.InflowListView.as_view(), name="inflow_list"),
    path("inflows/create/", views.InflowCreateView.as_view(), name="inflow_create"),
    path("inflows/<int:pk>/detail/", views.InflowDetail.as_view(), name="inflow_detail"),
]
