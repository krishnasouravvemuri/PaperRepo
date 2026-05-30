from django.urls import path

from .views import (
    ImportantTopicDetailView,
    ImportantTopicFileView,
    ImportantTopicListCreateView,
    MyImportantTopicsView,
)

urlpatterns = [
    path("", ImportantTopicListCreateView.as_view(), name="important_topics"),
    path("my_uploads/", MyImportantTopicsView.as_view(), name="my_important_topics"),
    path("<uuid:topic_id>/", ImportantTopicDetailView.as_view(), name="important_topic_detail"),
    path("<uuid:topic_id>/file/", ImportantTopicFileView.as_view(), name="important_topic_file"),
]
