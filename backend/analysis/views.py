from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from .utils import predict, analyze, measure_volume

def index(request):
    return render(request, 'index.html')

class PredictView(APIView):
    parser_classes = [MultiPartParser]

    def get(self, request):
        return render(request, 'templates/index.html')

    def post(self, request):
        if 'file' not in request.FILES:
            return Response({"error": "No file provided"}, status=400)

        file_obj = request.FILES['file']
        file_path = f'temp/{file_obj.name}'

        # Save the file temporarily
        with open(file_path, 'wb') as f:
            for chunk in file_obj.chunks():
                f.write(chunk)

        try:
            # Make analysis
            prediction = predict(file_path)
            volume_dB = measure_volume(file_path)
            analysis = analyze(file_path)
            return Response({"label": prediction, "volume_dB": volume_dB, "analysis": analysis})
        except Exception as e:
            return Response({"error": str(e)}, status=500)
        finally:
            # Clean up temporary file
            import os
            if os.path.exists(file_path):
                os.remove(file_path)

