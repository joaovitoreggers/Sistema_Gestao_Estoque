from django.urls import path
from . import views

urlpatterns = [
    path("category/list/", views.CategoryListView.as_view(), name="category_list"),
    path("category/create/", views.CategoryCreateView.as_view(), name="category_create"),
    path("category/<int:pk>/detail/", views.CategoryDetail.as_view(), name="category_detail"),
    path("category/<int:pk>/update/", views.CategorydUpdateView.as_view(), name="category_update"),
    path("category/<int:pk>/delete/", views.CategoryDeleteView.as_view(), name="category_delete")

]
