from rest_framework.views import APIView

from src.utils.response import ApiResponse

from .models import SubjectManagement


class ListSubjectsView(APIView):
    def get(self, request):
        search = request.query_params.get("search")
        code, message, data = SubjectManagement.list_subjects(search=search)
        return ApiResponse(data, code, message).build()
