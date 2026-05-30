from django.urls import include, path

urlpatterns = [
    path("api/v2/user_management/", include("user_management.urls")),
    path("api/v2/subject_management/", include("subject_management.urls")),
    path("api/v2/question_paper_management/", include("question_paper_management.urls")),
    path("api/v2/important_topic_management/", include("important_topic_management.urls")),
    path("api/v2/material_management/", include("material_management.urls")),
]
