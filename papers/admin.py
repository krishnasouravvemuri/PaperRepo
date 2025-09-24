from django.contrib import admin
from .models import QuestionPapers , ImportantTopics , Materials

admin.site.register([QuestionPapers , ImportantTopics , Materials])
