from django.shortcuts import render
from django.http import Http404
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

# Rest Framework Imports
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status

# Permissions
from oauth2_provider.contrib.rest_framework import TokenHasScope, OAuth2Authentication
from health.authentication import ResourceServerAuthentication

# Application imports
from .models import Report
from .serializers import ReportSerializer

# Create your views here.
class EnvironmentView(APIView):
    """
    List all environmental reports
    """
    authentication_classes = [ResourceServerAuthentication ]
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Get queryset with optional filtering"""
        queryset = Report.objects.all()
        
        # Filtering by title
        if 'title' in self.request.query_params:
            queryset = queryset.filter(title__icontains=self.request.query_params['title'])
            
        return queryset
    
    def get(self, request, report_id=None):
        """
        Handle GET:
        """
        if report_id:
            # Single report retrieval
            report = get_object_or_404(Report, report_id=report_id)
            serializer = ReportSerializer(report)
            return Response(serializer.data)
        else:
            # List all reports
            reports = self.get_queryset()
            serializer = ReportSerializer(reports, many=True)
            return Response({
                'count': reports.count(),
                'results': serializer.data
            })
            
    def post(self, request):
        """
        POST requests
        """
        serializer = ReportSerializer(data=request.data, context={'request': request})
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, report_id):
        """
        PUT requests
        """
        report = get_object_or_404(Report, report_id=report_id)
        serializer = ReportSerializer(report, data=request.data, context={'request': request})
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request, report_id):
        """
        PATCH requests
        """
        report = get_object_or_404(Report, report_id=report_id)
        serializer = ReportSerializer(report, data=request.data, partial=True, context={'request': request})
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, report_id):
        """
        DELETE requests
        """
        report = get_object_or_404(Report, report_id=report_id)
        report.delete()
        return Response(
            {'message': 'Report deleted successfully'},
            status=status.HTTP_204_NO_CONTENT
        )
    
    
