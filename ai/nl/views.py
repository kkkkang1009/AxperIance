from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets
from rest_framework.parsers import JSONParser
from .serializers import FilmrateSerializer
from .models import Filmrate
from .filmrate import filmrating


class FilmrateViewSet(viewsets.ModelViewSet):
    queryset = Filmrate.objects.all()
    serializer_class = FilmrateSerializer

@csrf_exempt
def filmrate_learning(request) :
    if request.method == 'POST' :
        jsonBody = JSONParser().parse(request)
        result = filmrating.make_filmrate_model(jsonBody["url"], jsonBody["keyword"], jsonBody["user_id"], jsonBody["user_pw"])
        return HttpResponse(result, status=200)
    else :
        return HttpResponse(status=404)

@csrf_exempt
def filmrate_predict(request) :
    if request.method == 'POST' :
        jsonBody = JSONParser().parse(request)
        result = filmrating.get_filmrate_prediction(jsonBody["content"])
        #data = "{'data': 'test'}"
        #return JsonResponse("hello", status=200)
        return HttpResponse(result, status=200)
    else:
        return HttpResponse(status=404)
