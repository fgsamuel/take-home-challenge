from django.http import JsonResponse
from django.shortcuts import render

from xml_converter.services import parse_xml_string


def upload_page(request):
    if request.method == 'POST':
        f = request.FILES['file']
        result = parse_xml_string(f.read().decode('utf-8'))
        return JsonResponse(result)

    return render(request, "upload_page.html")
