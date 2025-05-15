from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import BusinessRegApplication
from .serializer import BusinessRegApplicationSerializer

# Public 
@api_view(["GET", "POST"])
def businesses_public(request):
    if request.method == "GET":
        businesses = BusinessRegApplication.objects.all().filter(is_approved=True)
        serializer = BusinessRegApplicationSerializer(businesses, many=True)
        return Response(data=serializer.data)
       
    if request.method == "POST":
        serializer = BusinessRegApplicationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data,status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["GET"])
def get_tourist_attractions(request):
    # get data from poi service
    return Response(data="get data from poi service")

@api_view(["GET"])
def get_upcoming_events(request):
    # get data from event sercive
    return Response(data="get data from event service")


# Internal
@api_view(["GET"])
def get_business_reg_requests(request):
    if request.method == "GET":
        businesses = BusinessRegApplication.objects.all().filter(is_approved=False)
        serializer = BusinessRegApplicationSerializer(businesses, many=True)
        return Response(data=serializer.data)
    

@api_view(["GET","PUT"])
def reg_request_detail(request, id):
    try:
        business = BusinessRegApplication.objects.get(id = id)
    except BusinessRegApplication.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == "GET":
        serializer = BusinessRegApplicationSerializer(business)
        return Response(data=serializer.data)

    if request.method == "PUT":    
        serializer = BusinessRegApplicationSerializer(business, data=request.data)
        if serializer.is_valid():
            serializer.save()
            #TODO: make request to add business to specified table if is_approved == true
            return Response(data=serializer.data)
        return Response(data=serializer.error_messages, status=status.HTTP_400_BAD_REQUEST)


