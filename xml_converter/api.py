from django.http import JsonResponse
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser
from rest_framework.viewsets import ViewSet

from xml_converter.exceptions import XMLConverterError
from xml_converter.services import parse_xml_string


class ConverterViewSet(ViewSet):
    # Note this is not a restful API
    # We still use DRF to assess how well you know the framework
    parser_classes = [MultiPartParser]

    @action(methods=["POST"], detail=False, url_path="convert")
    def convert(self, request, **kwargs):
        xml_file = request.data.get("file")
        if not xml_file:
            return JsonResponse({"error": "No file uploaded"}, status=400)

        try:
            response = parse_xml_string(xml_file.read().decode("utf-8"))
        except XMLConverterError:
            return JsonResponse({"error": "Invalid XML"}, status=400)

        return JsonResponse(response)
