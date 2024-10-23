from django.urls import path
from . import views

urlpatterns = [
    path('services/list/', views.ServiceListView.as_view(), name='service_list'),
    path('services/create/', views.ServiceCreateView.as_view(), name='service_create'),
    path('services/<int:pk>/detail/', views.ServiceDetailView.as_view(), name='service_detail'),
    path('services/<int:pk>/update/', views.ServiceUpdateView.as_view(), name='service_update'),
    path("services/<int:pk>/delete/", views.ServiceDeleteView.as_view(), name="service_delete")
]
