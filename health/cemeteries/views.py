# Django imports
from django.shortcuts import get_object_or_404

# Rest Framework imports
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

# Application imports
from .models import CemeteryPlot
from .serializers import CemeteryPlotSerializer
from health.authentication import ResourceServerAuthentication

class CemeteryPlotView(APIView):
    """
    List all cemetery plots or create/update/delete a specific plot
    """
    authentication_classes = [ResourceServerAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Get queryset with optional filtering"""
        queryset = CemeteryPlot.objects.all()
        
        # Filtering by name
        if 'name' in self.request.query_params:
            queryset = queryset.filter(name__icontains=self.request.query_params['name'])
            
        # Filtering by availability
        if 'available' in self.request.query_params:
            queryset = queryset.filter(available=self.request.query_params['available'])
            
        return queryset
    
    def get(self, request, plot_id=None):
        """
        Handle GET:
        - If plot_id provided: return single plot
        - Else: return list of all plots with count
        """
        if plot_id:
            # Single plot retrieval
            plot = get_object_or_404(CemeteryPlot, plot_id=plot_id)
            serializer = CemeteryPlotSerializer(plot)
            return Response(serializer.data)
        else:
            # List all plots
            plots = self.get_queryset()
            serializer = CemeteryPlotSerializer(plots, many=True)
            return Response({
                'count': plots.count(),
                'results': serializer.data
            })
            
    def post(self, request):
        """
        Handle POST - Create new cemetery plot
        """
        serializer = CemeteryPlotSerializer(data=request.data, context={'request': request})
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, plot_id):
        """
        Handle PUT - Full update of plot
        """
        plot = get_object_or_404(CemeteryPlot, plot_id=plot_id)
        serializer = CemeteryPlotSerializer(
            plot, 
            data=request.data, 
            context={'request': request}
        )
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request, plot_id):
        """
        Handle PATCH - Partial update of plot
        """
        plot = get_object_or_404(CemeteryPlot, plot_id=plot_id)
        serializer = CemeteryPlotSerializer(
            plot, 
            data=request.data, 
            partial=True, 
            context={'request': request}
        )
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, plot_id):
        """
        Handle DELETE - Remove plot
        """
        plot = get_object_or_404(CemeteryPlot, plot_id=plot_id)
        plot.delete()
        return Response(
            {'message': 'Cemetery plot deleted successfully'},
            status=status.HTTP_204_NO_CONTENT
        )