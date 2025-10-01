from django import forms
from .models import QuestionPapers , ImportantTopics , Materials

class QuestionPapersForm(forms.ModelForm):
    class Meta:
        model = QuestionPapers
        fields = ['question_paper_title' , 'subject_name' , 'subject_code' , 'exam_slot' , 'exam_type' , 'semester' , 'year' , 'file_choosen']

class ImportantTopicsForm(forms.ModelForm):
    class Meta:
        model = ImportantTopics
        fields = ['important_topic_title' , 'subject_name' , 'subject_code' , 'exam_type' , 'faculty_name' , 'file_choosen']

class MaterialsForm(forms.ModelForm):
    class Meta:
        model = Materials
        fields = ['study_material_title' , 'subject_name' , 'subject_code' , 'exam_type' , 'faculty_name' , 'file_choosen']
