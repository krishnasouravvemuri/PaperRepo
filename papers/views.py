from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import FileResponse
import urllib
from .forms import QuestionPapersForm, ImportantTopicsForm, MaterialsForm
from .models import QuestionPapers, ImportantTopics, Materials

def PapersHome(request):
    return render(request, 'PapersHome.html')

@login_required
def UploadHome(request, username):
    return render(request, 'UploadHome.html', {"username": username})

def ShowQuestionPapers(request):
    papers = QuestionPapers.objects.filter(is_deleted=False).order_by('-question_paper_id')

    course_code = request.GET.get("course_code", "")
    exam_type = request.GET.get("exam_type", "")

    if course_code:
        papers = papers.filter(subject_code__icontains=course_code)
    if exam_type:
        papers = papers.filter(exam_type=exam_type)

    return render(request, "QuestionPapers.html", {
        "papers": papers,
        "course_code": course_code,
        "exam_type": exam_type
    })

def ShowImportantTopics(request):
    topics = ImportantTopics.objects.filter(is_deleted=False).order_by('-important_topic_id')

    course_code = request.GET.get("course_code", "")
    exam_type = request.GET.get("exam_type", "")

    if course_code:
        topics = topics.filter(subject_code__icontains=course_code)
    if exam_type:
        topics = topics.filter(exam_type=exam_type)

    return render(request, "ImportantTopics.html", {
        "topics": topics,
        "course_code": course_code,
        "exam_type": exam_type
    })

def Shownotes(request):
    materials = Materials.objects.filter(is_deleted=False).order_by('-material_id')

    course_code = request.GET.get("course_code", "")
    topic_type = request.GET.get("topic_type", "")

    if course_code:
        materials = materials.filter(subject_code__icontains=course_code)
    if topic_type:
        materials = materials.filter(topic_type=topic_type)

    return render(request, "notes.html", {
        "materials": materials,
        "course_code": course_code,
        "topic_type": topic_type
    })

@login_required
def ImportantTopicsUpload(request):
    if request.method == "POST":
        form = ImportantTopicsForm(request.POST, request.FILES)
        files = request.FILES.getlist('file_choosen')

        if form.is_valid():
            for f in files:
                ImportantTopics.objects.create(
                    user=request.user,
                    important_topic_title=form.cleaned_data['important_topic_title'],
                    subject_name=form.cleaned_data['subject_name'],
                    subject_code=form.cleaned_data['subject_code'],
                    exam_type=form.cleaned_data['exam_type'],
                    faculty_name=form.cleaned_data.get('faculty_name'),
                    file_choosen=f
                )
            messages.success(request, f"{len(files)} file(s) uploaded successfully!")
            return redirect("ImportantTopicsUpload")
        else:
            messages.error(request, form.errors)
    else:
        form = ImportantTopicsForm()

    return render(request, "ImportantTopicsUpload.html", {"form": form, "username": request.user.username})

@login_required
def QuestionPapersUpload(request):
    if request.method == "POST":
        form = QuestionPapersForm(request.POST, request.FILES)
        files = request.FILES.getlist('file_choosen')

        if form.is_valid():
            for f in files:
                QuestionPapers.objects.create(
                    user=request.user,
                    question_paper_title=form.cleaned_data['question_paper_title'],
                    subject_name=form.cleaned_data['subject_name'],
                    subject_code=form.cleaned_data['subject_code'],
                    exam_slot=form.cleaned_data['exam_slot'],
                    exam_type=form.cleaned_data['exam_type'],
                    semester=form.cleaned_data['semester'],
                    year=form.cleaned_data['year'],
                    file_choosen=f
                )
            messages.success(request, f"{len(files)} file(s) uploaded successfully!")
            return redirect("QuestionPapersUpload")
        else:
            messages.error(request, form.errors)
    else:
        form = QuestionPapersForm()

    return render(request, "QuestionPapersUpload.html", {"form": form, "username": request.user.username})

@login_required
def notesUpload(request):
    if request.method == "POST":
        form = MaterialsForm(request.POST, request.FILES)
        files = request.FILES.getlist('file_choosen')

        if form.is_valid():
            for f in files:
                Materials.objects.create(
                    user=request.user,
                    study_material_title=form.cleaned_data['study_material_title'],
                    subject_name=form.cleaned_data['subject_name'],
                    subject_code=form.cleaned_data['subject_code'],
                    topic_type=form.cleaned_data['topic_type'],
                    faculty_name=form.cleaned_data.get('faculty_name'),
                    file_choosen=f
                )
            messages.success(request, f"{len(files)} file(s) uploaded successfully!")
            return redirect("notesUpload")
        else:
            messages.error(request, form.errors)
    else:
        form = MaterialsForm()

    return render(request, "notesUpload.html", {"form": form, "username": request.user.username})

@login_required
def MyUploads(request, username):
    user_id = request.user.id

    # Question Papers (exclude deleted)
    question_papers = QuestionPapers.objects.raw(
        "SELECT question_paper_title, question_paper_id, subject_name, subject_code, exam_slot, exam_type, semester "
        "FROM papers_questionpapers WHERE user_id = %s AND is_deleted = FALSE ORDER BY question_paper_id DESC",
        [user_id]
    )

    # Important Topics (exclude deleted)
    important_topics = ImportantTopics.objects.raw(
        "SELECT important_topic_title , important_topic_id, subject_name, subject_code, exam_type, faculty_name "
        "FROM papers_importanttopics WHERE user_id = %s AND is_deleted = FALSE ORDER BY important_topic_id DESC",
        [user_id]
    )

    # Materials (exclude deleted)
    materials = Materials.objects.raw(
        "SELECT study_material_title , material_id, subject_name, subject_code, topic_type, faculty_name "
        "FROM papers_materials WHERE user_id = %s AND is_deleted = FALSE ORDER BY material_id DESC",
        [user_id]
    )

    return render(request, 'MyUploads.html', {
        "username": username,
        "question_papers": question_papers,
        "important_topics": important_topics,
        "materials": materials
    })

@login_required
def serve_question_paper(request, username, paper_id):
    paper = get_object_or_404(QuestionPapers, pk=paper_id, user=request.user, is_deleted=False)
    s3_file = urllib.request.urlopen(paper.file_choosen.url)
    download = request.GET.get("download", "false") == "true"
    return FileResponse(s3_file, as_attachment=download, filename=paper.file_choosen.name)

@login_required
def serve_important_topic(request, username, topic_id):
    topic = get_object_or_404(ImportantTopics, pk=topic_id, user=request.user, is_deleted=False)
    s3_file = urllib.request.urlopen(topic.file_choosen.url)
    download = request.GET.get("download", "false") == "true"
    return FileResponse(s3_file, as_attachment=download, filename=topic.file_choosen.name)

@login_required
def serve_material(request, username, material_id):
    material = get_object_or_404(Materials, pk=material_id, user=request.user, is_deleted=False)
    s3_file = urllib.request.urlopen(material.file_choosen.url)
    download = request.GET.get("download", "false") == "true"
    return FileResponse(s3_file, as_attachment=download, filename=material.file_choosen.name)

@login_required
def EditQuestionPapers(request, pk):
    paper = get_object_or_404(QuestionPapers, pk=pk, is_deleted=False)

    if request.method == "POST":
        form = QuestionPapersForm(request.POST, request.FILES, instance=paper)
        if form.is_valid():
            if form.changed_data:
                for field in form.changed_data:
                    setattr(paper, field, form.cleaned_data[field])
                paper.save()
                messages.success(request, "Updates made successfully!")
            else:
                messages.info(request, "No changes were made.")
            return redirect("MyUploads", request.user.username)
        else:
            messages.error(request, form.errors)
    else:
        form = QuestionPapersForm(instance=paper)

    return render(request, "QuestionPaperEdit.html", {"form": form, "username": request.user.username, "object": paper})

@login_required
def EditImportantTopics(request, pk):
    topic = get_object_or_404(ImportantTopics, pk=pk, is_deleted=False)

    if request.method == "POST":
        form = ImportantTopicsForm(request.POST, request.FILES, instance=topic)
        if form.is_valid():
            if form.changed_data:
                for field in form.changed_data:
                    setattr(topic, field, form.cleaned_data[field])
                topic.save()
                messages.success(request, "Updates made successfully!")
            else:
                messages.info(request, "No changes were made.")
            return redirect("MyUploads", request.user.username)
        else:
            messages.error(request, form.errors)
    else:
        form = ImportantTopicsForm(instance=topic)

    return render(request, "ImportantTopicEdit.html", {"form": form, "username": request.user.username, "object": topic})

@login_required
def EditStudyMaterials(request, pk):
    material = get_object_or_404(Materials, pk=pk, is_deleted=False)

    if request.method == "POST":
        form = MaterialsForm(request.POST, request.FILES, instance=material)
        if form.is_valid():
            if form.changed_data:
                for field in form.changed_data:
                    setattr(material, field, form.cleaned_data[field])
                material.save()
                messages.success(request, "Updates made successfully!")
            else:
                messages.info(request, "No changes were made.")
            return redirect("MyUploads", request.user.username)
        else:
            messages.error(request, form.errors)
    else:
        form = MaterialsForm(instance=material)

    return render(request, "StudyMaterialEdit.html", {"form": form, "username": request.user.username, "object": material})

@login_required
def DeleteQuestionPapers(request, username, pk):
    paper = get_object_or_404(QuestionPapers, pk=pk)
    if request.method == "POST":
        paper.is_deleted = True  # soft delete
        paper.save()
        messages.success(request, "Question paper deleted successfully!")
        return redirect("MyUploads", username=username)
    return render(request, "ConfirmDelete.html", {"object": paper, "type": "Question Paper"})

@login_required
def DeleteImportantTopics(request, username, pk):
    topic = get_object_or_404(ImportantTopics, pk=pk)
    if request.method == "POST":
        topic.is_deleted = True  # soft delete
        topic.save()
        messages.success(request, "Important topic deleted successfully!")
        return redirect("MyUploads", username=username)
    return render(request, "ConfirmDelete.html", {"object": topic, "type": "Important Topic"})

@login_required
def DeleteStudyMaterials(request, username, pk):
    material = get_object_or_404(Materials, pk=pk)
    if request.method == "POST":
        material.is_deleted = True  # soft delete
        material.save()
        messages.success(request, "Study material deleted successfully!")
        return redirect("MyUploads", username=username)
    return render(request, "ConfirmDelete.html", {"object": material, "type": "Study Material"})

def QuestionPaperSearch(request):
    course_code = request.GET.get("course_code")
    exam_type = request.GET.get("exam_type")

    query = "SELECT * FROM papers_questionpapers WHERE is_deleted = FALSE"
    params = []

    if course_code:
        query += " AND subject_code LIKE %s"
        params.append(f"%{course_code}%")
    if exam_type:
        query += " AND exam_type = %s"
        params.append(exam_type)

    papers = QuestionPapers.objects.raw(query, params)

    return render(request, "QuestionPapers.html", {
        "papers": papers,
        "course_code": course_code or "",
        "exam_type": exam_type or ""
    })

def ImportantTopicsSearch(request):
    course_code = request.GET.get("course_code")
    exam_type = request.GET.get("exam_type")

    query = "SELECT * FROM papers_importanttopics WHERE is_deleted = FALSE"
    params = []

    if course_code:
        query += " AND subject_code LIKE %s"
        params.append(f"%{course_code}%")
    if exam_type:
        query += " AND exam_type = %s"
        params.append(exam_type)

    topics = ImportantTopics.objects.raw(query, params)

    return render(request, "ImportantTopics.html", {
        "topics": topics,
        "course_code": course_code or "",
        "exam_type": exam_type or ""
    })

def MaterialsSearch(request):
    course_code = request.GET.get("course_code")
    topic_type = request.GET.get("topic_type")

    query = "SELECT * FROM papers_materials WHERE is_deleted = FALSE"
    params = []

    if course_code:
        query += " AND subject_code LIKE %s"
        params.append(f"%{course_code}%")
    if topic_type:
        query += " AND topic_type = %s"
        params.append(topic_type)

    materials = Materials.objects.raw(query, params)

    return render(request, "notes.html", {
        "materials": materials,
        "course_code": course_code or "",
        "topic_type": topic_type or ""
    })

def SearchQuestionPapers(request, question_paper_id):
    paper = get_object_or_404(QuestionPapers, pk=question_paper_id, is_deleted=False)
    download = request.GET.get("download", "false") == "true"
    return FileResponse(paper.file_choosen.open(), as_attachment=download, filename=paper.file_choosen.name)

def SearchImportantTopics(request, important_topic_id):
    topic = get_object_or_404(ImportantTopics, pk=important_topic_id, is_deleted=False)
    download = request.GET.get("download", "false") == "true"
    return FileResponse(topic.file_choosen.open(), as_attachment=download, filename=topic.file_choosen.name)

def SearchStudyMaterials(request, material_id):
    material = get_object_or_404(Materials, pk=material_id, is_deleted=False)
    download = request.GET.get("download", "false") == "true"
    return FileResponse(material.file_choosen.open(), as_attachment=download, filename=material.file_choosen.name)
