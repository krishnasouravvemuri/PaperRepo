from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.views import APIView

from src.utils.response import ApiResponse

from .models import MaterialManagement
from .serializers import CreateMaterialSerializer, UpdateMaterialSerializer


def _require_auth(request):
    return request.META.get("user_id")


class MaterialListCreateView(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def get(self, request):
        filters = {
            "course_code": request.query_params.get("course_code"),
            "topic_type": request.query_params.get("topic_type"),
        }
        code, message, data = MaterialManagement.list_materials(filters=filters)
        return ApiResponse(data, code, message).build()

    def post(self, request):
        user_id = _require_auth(request)
        if not user_id:
            return ApiResponse(None, 401, "Please login!").build()
        serializer = CreateMaterialSerializer(data=request.data)
        if not serializer.is_valid():
            return ApiResponse(serializer.errors, 400, "Validation error.").build()
        files = serializer.validated_data.pop("files")
        code, message, data = MaterialManagement.create(user_id, serializer.validated_data, files)
        return ApiResponse(data, code, message).build()


class MyMaterialsView(APIView):
    def get(self, request):
        user_id = _require_auth(request)
        if not user_id:
            return ApiResponse(None, 401, "Please login!").build()
        code, message, data = MaterialManagement.list_mine(user_id=user_id)
        return ApiResponse(data, code, message).build()


class MaterialDetailView(APIView):
    def patch(self, request, material_id):
        user_id = _require_auth(request)
        if not user_id:
            return ApiResponse(None, 401, "Please login!").build()
        serializer = UpdateMaterialSerializer(data=request.data)
        if not serializer.is_valid():
            return ApiResponse(serializer.errors, 400, "Validation error.").build()
        code, message, data = MaterialManagement.update(
            user_id, str(material_id), serializer.validated_data
        )
        return ApiResponse(data, code, message).build()

    def delete(self, request, material_id):
        user_id = _require_auth(request)
        if not user_id:
            return ApiResponse(None, 401, "Please login!").build()
        code, message, data = MaterialManagement.delete(user_id, str(material_id))
        return ApiResponse(data, code, message).build()


class MaterialFileView(APIView):
    def get(self, request, material_id):
        code, message, data = MaterialManagement.get_file_url(str(material_id))
        return ApiResponse(data, code, message).build()
