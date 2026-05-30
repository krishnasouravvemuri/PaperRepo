from django.urls import path

from .views import (
    MyQuestionPapersView,
    QuestionPaperDetailView,
    QuestionPaperFileView,
    QuestionPaperListCreateView,
)

urlpatterns = [
    path("", QuestionPaperListCreateView.as_view(), name="question_papers"),
    path("my_uploads/", MyQuestionPapersView.as_view(), name="my_question_papers"),
    path("<uuid:paper_id>/", QuestionPaperDetailView.as_view(), name="question_paper_detail"),
    path("<uuid:paper_id>/file/", QuestionPaperFileView.as_view(), name="question_paper_file"),
]
