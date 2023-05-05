from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Script

class GenerateScriptAPIView(APIView):

    def post(self, request):
        return Response({"data" : request.data})

class RunScriptAPIView(APIView):

    def post(self, request):
        return Response({"data" : request.data})