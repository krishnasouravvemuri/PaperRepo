from django.urls import path

from .views import ListSubjectsView

urlpatterns = [
    path("", ListSubjectsView.as_view(), name="list_subjects"),
]
