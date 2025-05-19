from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import InterestingPlace, InterestingPlaceImage
from .serializer import InterestingPlaceSerializer, InterestingPlaceImageSerializer

# Places Of Interest
# Public
@api_view(["GET"])
def place_list(request):
    if request.method == "GET":
        places = InterestingPlace.objects.all()
        serializer = InterestingPlaceSerializer(places, many=True)
        return Response(data=serializer.data)


@api_view(["GET"])
def place_details(request, id):
    try:
        place = InterestingPlace.objects.get(id = id)
    except InterestingPlace.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = InterestingPlaceSerializer(place)
        return Response(data=serializer.data)
    
# Internal 
@api_view(["GET","POST"])
def admin_create_poi(request):
    # TODO: add auth check for admins

    if request.method == "GET":
        serializer = InterestingPlaceSerializer(place)
        return Response(data=serializer.data)
    
    if request.method == "POST":
        serializer = InterestingPlaceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["GET", "PUT", "DELETE"])
def admin_poi_detail(request, id):
    # TODO: add auth check for admins
    try:
        place = InterestingPlace.objects.get(id = id)
    except InterestingPlace.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = InterestingPlaceSerializer(place)
        return Response(data=serializer.data)

    if request.method == "PUT":
        serializer = InterestingPlaceSerializer(place, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "DELETE":
        place.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# Places Of Interest Images

# Public

def poi_images(request, place_id):

    if request.method == "GET":
        place_images = InterestingPlaceImage.objects.get(place_id=place_details)
        serializer = InterestingPlaceImageSerializer(place_images, many=True)
        return Response(data=serializer.data)
    


    
