from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.views import APIView

from src.utils.response import ApiResponse

from .models import QuestionPaperManagement
from .serializers import CreateQuestionPaperSerializer, UpdateQuestionPaperSerializer


def _require_auth(request):
    return request.META.get("user_id")


class QuestionPaperListCreateView(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def get(self, request):
        filters = {
            "course_code": request.query_params.get("course_code"),
            "exam_type": request.query_params.get("exam_type"),
        }
        code, message, data = QuestionPaperManagement.list_papers(filters=filters)
        return ApiResponse(data, code, message).build()

    def post(self, request):
        user_id = _require_auth(request)
        if not user_id:
            return ApiResponse(None, 401, "Please login!").build()
        serializer = CreateQuestionPaperSerializer(data=request.data)
        if not serializer.is_valid():
            return ApiResponse(serializer.errors, 400, "Validation error.").build()
        files = serializer.validated_data.pop("files")
        code, message, data = QuestionPaperManagement.create(user_id, serializer.validated_data, files)
        return ApiResponse(data, code, message).build()


class MyQuestionPapersView(APIView):
    def get(self, request):
        user_id = _require_auth(request)
        if not user_id:
            return ApiResponse(None, 401, "Please login!").build()
        code, message, data = QuestionPaperManagement.list_mine(user_id=user_id)
        return ApiResponse(data, code, message).build()


class QuestionPaperDetailView(APIView):
    def patch(self, request, paper_id):
        user_id = _require_auth(request)
        if not user_id:
            return ApiResponse(None, 401, "Please login!").build()
        serializer = UpdateQuestionPaperSerializer(data=request.data)
        if not serializer.is_valid():
            return ApiResponse(serializer.errors, 400, "Validation error.").build()
        code, message, data = QuestionPaperManagement.update(
            user_id, str(paper_id), serializer.validated_data
        )
        return ApiResponse(data, code, message).build()

    def delete(self, request, paper_id):
        user_id = _require_auth(request)
        if not user_id:
            return ApiResponse(None, 401, "Please login!").build()
        code, message, data = QuestionPaperManagement.delete(user_id, str(paper_id))
        return ApiResponse(data, code, message).build()


class QuestionPaperFileView(APIView):
    def get(self, request, paper_id):
        code, message, data = QuestionPaperManagement.get_file_url(str(paper_id))
        return ApiResponse(data, code, message).build()
