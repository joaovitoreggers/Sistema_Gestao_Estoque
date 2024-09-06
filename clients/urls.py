from django.urls import path
from . import views

urlpatterns = [
    path('clients/list/', views.ClientListView.as_view(), name='client_list'),
    path('clients/create/', views.ClientCreateView.as_view(), name='client_create'),
    path('clients/<int:pk>/detail/', views.ClientDetailView.as_view(), name='client_detail'),
    path('clients/<int:pk>/update/', views.ClientUpdateView.as_view(), name='client_update'),
    path("clients/<int:pk>/delete/", views.ClientDeleteView.as_view(), name="client_delete")
]
