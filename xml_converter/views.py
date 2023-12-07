import json
import logging

from django.http import JsonResponse
from django.shortcuts import render
from django.utils.datastructures import MultiValueDictKeyError

from xml_converter.exceptions import XMLConverterError
from xml_converter.services import parse_xml_string

logger = logging.getLogger(__name__)


def upload_page(request):
    def _return_response(data):
        if request.POST.get("output_format") == "formatted":
            data_json = json.dumps(data, indent=4)
            return render(request, "result_page.html", {"data_json": data_json})
        else:
            return JsonResponse(data)

    if request.method == 'POST':
        try:
            f = request.FILES['file']
            result = parse_xml_string(f.read().decode('utf-8'))
            return _return_response(result)
        except XMLConverterError:
            return render(request, "error_page.html")
        except MultiValueDictKeyError:
            logger.exception("No file uploaded", exc_info=True)
            return render(request, "error_page.html")

    return render(request, "upload_page.html")
