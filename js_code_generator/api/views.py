from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from .services import ScriptService
from .models import Script

class GenerateScriptAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        script_request = request.data
        script = ScriptService.generate(script_request["description"])
        try:
            ScriptService.test(script, script_request["test_parameters"])
        except:
            return Response(status=500)
        else:
            script.save()
            return Response({"id" : script.id})
        

class RunScriptAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        run_request = request.data
        script = Script.objects.get(pk=run_request["id"])
        result = ScriptService.test(script, run_request["parameters"])
        return Response({"result" : result})