from django.urls import path

from .views import (
    MaterialDetailView,
    MaterialFileView,
    MaterialListCreateView,
    MyMaterialsView,
)

urlpatterns = [
    path("", MaterialListCreateView.as_view(), name="materials"),
    path("my_uploads/", MyMaterialsView.as_view(), name="my_materials"),
    path("<uuid:material_id>/", MaterialDetailView.as_view(), name="material_detail"),
    path("<uuid:material_id>/file/", MaterialFileView.as_view(), name="material_file"),
]
