from django.urls import path 
from. import views as v

urlpatterns = [
    path('notes/' , v.Shownotes , name = "notes"),
    path('ImportantTopics/' , v.ShowImportantTopics , name = "ImportantTopics"),
    path('QuestionPapers/' , v.ShowQuestionPapers , name = "QuestionPapers"),

    path('PapersHome/' , v.PapersHome , name = "PapersHome"),
    path('UploadHome/<str:username>/' , v.UploadHome , name = "UploadHome"),
    
    path('QuestionPapersUpload/' , v.QuestionPapersUpload , name = "QuestionPapersUpload"),
    path('ImportantTopicsUpload/' , v.ImportantTopicsUpload , name = "ImportantTopicsUpload"),
    path('notesUpload/' , v.notesUpload , name = "notesUpload"),

    path('MyUploads/<str:username>/' , v.MyUploads , name = "MyUploads"),
    path("EditQuestionPapers/<int:pk>/", v.EditQuestionPapers , name = "EditQuestionPapers"),
    path("EditImportantTopics/<int:pk>/", v.EditImportantTopics , name = "EditImportantTopics"),
    path("EditStudyMaterials/<int:pk>/", v.EditStudyMaterials , name = "EditStudyMaterials"),

    path('MyUploads/<str:username>/DeleteQuestionPapers/<int:pk>/', v.DeleteQuestionPapers, name='DeleteQuestionPapers'),
    path('MyUploads/<str:username>/DeleteImportantTopics/<int:pk>/', v.DeleteImportantTopics, name='DeleteImportantTopics'),
    path('MyUploads/<str:username>/DeleteStudyMaterials/<int:pk>/', v.DeleteStudyMaterials, name='DeleteStudyMaterials'),


    path('MyUploads/<str:username>/QuestionPaper/<int:paper_id>/', v.serve_question_paper, name='serve_question_paper'),
    path('MyUploads/<str:username>/ImportantTopic/<int:topic_id>/', v.serve_important_topic, name='serve_important_topic'),
    path('MyUploads/<str:username>/StudyMaterial/<int:material_id>/', v.serve_material, name='serve_material'),

    path('QuestionPaperSearch/', v.QuestionPaperSearch, name='QuestionPaperSearch'),
    path('ImportantTopicsSearch/', v.ImportantTopicsSearch, name='ImportantTopicsSearch'),
    path('MaterialsSearch/', v.MaterialsSearch, name='MaterialsSearch'),

    path('SearchQuestionPapers/<int:question_paper_id>/' , v.SearchQuestionPapers , name = "SearchQuestionPapers"),
    path('SearchImportantTopics/<int:important_topic_id>/' , v.SearchImportantTopics , name = "SearchImportantTopics"),
    path('SearchStudyMaterials/<int:material_id>/' , v.SearchStudyMaterials , name = "SearchStudyMaterials"),
]