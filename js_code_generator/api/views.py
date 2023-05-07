from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from .services import ScriptService
from .models import Script
from .serializers import ScriptListSerializer

class ListFunctionsAPIView(APIView):
    """
    A class that describes the list_functions/ endpoint
    """
    serializer_class = ScriptListSerializer

    def get(self, request):
        scripts = Script.objects.all()
        serializer = self.serializer_class(scripts, many=True)
        return Response(serializer.data)

class GenerateScriptAPIView(APIView):
    """
    A class that describes the generate/ endpoint
    """

    permission_classes = [permissions.AllowAny]
    script_service = ScriptService()

    def post(self, request):
        script_request = request.data
        # Generate the script object by calling the script_service
        script = self.script_service.generate(script_request["description"])
        try:
            # Test if the script runs without errors
            self.script_service.test(script, script_request["test_parameters"])
        except:
            # Error occured - output server error
            return Response(status=500)
        else:
            # No errors occured, save the script and return its id
            script.save()
            return Response({"id" : script.id})
        

class RunScriptAPIView(APIView):
    """
    A class that describes the test/ endpoint
    """

    permission_classes = [permissions.AllowAny]
    script_service = ScriptService()

    def post(self, request):
        run_request = request.data
        # Load the script from the database by its id
        script = Script.objects.get(pk=run_request["id"])
        # Run the script with the user's parameters
        result = self.script_service.test(script, run_request["parameters"])
        return Response({"result" : result})