from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions

from .serializers import GenerateRequestSerializer, TestRequestSerializer
from .services import ScriptService
from .models import Script

class GenerateScriptAPIView(APIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = GenerateRequestSerializer

    def post(self, request):
        script_request = self.serializer_class(data=request.data)
        if script_request.is_valid():
            script = ScriptService.generate(script_request.description)
            if ScriptService.test(script, script_request.test_parameters):
                script.save()
        
        return Response({"id" : script.id})

class RunScriptAPIView(APIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = TestRequestSerializer

    def post(self, request):
        run_request = self.serializer_class(data=request.data)
        if run_request.is_valid():
            script = Script.objects.get(pk=run_request.id)
            result = ScriptService.test(script, run_request.parameters)
        return Response({"result" : result})