from django.urls import path
from . import views

urlpatterns = [
    path('brands/list/', views.BrandListView.as_view(), name='brand_list'),
    path('brands/create/', views.BrandCreateView.as_view(), name='brand_create'),
    path('brands/<int:pk>/detail/', views.BrandDetailView.as_view(), name='brand_detail'),
    path('brands/<int:pk>/update/', views.BrandUpdateView.as_view(), name='brand_update'),
    path("brands/<int:pk>/delete/", views.BrandDeleteView.as_view(), name="brand_delete"),

    path("brands/history/", views.BrandFilterView.as_view(), name="brand_filter"),

    path('api/v1/brands/', views.BrandCreateListApiView.as_view(), name='brand_list_api'),
    path('api/v1/brands/<int:pk>', views.BrandRetriveUpdateDestroyApiView.as_view(), name='brand_update_api'),

]
