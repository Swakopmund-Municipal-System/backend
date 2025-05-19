# Django imports
from django.shortcuts import get_object_or_404

# Rest Framework imports
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

# Application imports
from .models import Complaint, ComplaintImage
from .serializers import ComplaintSerializer
from health.authentication import ResourceServerAuthentication

class ComplaintView(APIView):
    """
    List all complaints or create/update/delete a specific complaint
    """
    authentication_classes = [ResourceServerAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Get queryset with optional filtering"""
        queryset = Complaint.objects.all()
        
        # Filtering by title
        if 'title' in self.request.query_params:
            queryset = queryset.filter(title__icontains=self.request.query_params['title'])
            
        # Filtering by status
        if 'status' in self.request.query_params:
            queryset = queryset.filter(status=self.request.query_params['status'])
            
        return queryset
    
    def get(self, request, complaint_id=None):
        """
        GET Request
        """
        if complaint_id:
            # Single complaint retrieval
            complaint = get_object_or_404(Complaint, complaint_id=complaint_id)
            serializer = ComplaintSerializer(complaint)
            return Response(serializer.data)
        else:
            # List all complaints
            complaints = self.get_queryset()
            serializer = ComplaintSerializer(complaints, many=True)
            return Response({
                'count': complaints.count(),
                'results': serializer.data
            })
            
    def post(self, request):
        """
        POST request
        """
        
        print(request.user.auth_data)
        # Create mutable copy of request data
        data = request.data.copy()
        
        data['created_by'] = request.user.auth_data.get('user', {}).get('user', {}).get('email')
        data['updated_by'] = request.user.auth_data.get('user', {}).get('user', {}).get('email')
        
        serializer = ComplaintSerializer(data=data, context={'request': request})
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, complaint_id):
        """
        PUT request
        """
        complaint = get_object_or_404(Complaint, complaint_id=complaint_id)
        data = request.data.copy()
        data['updated_by'] = request.user.auth_data.get('user', {}).get('user', {}).get('email')
        
        serializer = ComplaintSerializer(
            complaint, 
            data=data, 
            context={'request': request}
        )
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request, complaint_id):
        """
        PATCH request
        """
        complaint = get_object_or_404(Complaint, complaint_id=complaint_id)
        data = request.data.copy()
        data['updated_by'] = request.user.auth_data.get('user', {}).get('user', {}).get('email')
        
        serializer = ComplaintSerializer(
            complaint, 
            data=data, 
            partial=True, 
            context={'request': request}
        )
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, complaint_id):
        """
        DELETE request
        """
        complaint = get_object_or_404(Complaint, complaint_id=complaint_id)
        complaint.delete()
        return Response(
            {'message': 'Complaint deleted successfully'},
            status=status.HTTP_204_NO_CONTENT
        )
        
class ComplaintImageView(APIView):
    """
    Images API for specific complaint
    """
    authentication_classes = [ResourceServerAuthentication]
    permission_classes = [IsAuthenticated]
    
    def post(self, request, complaint_id):
        """
        POST request to add images to a complaint
        """
        complaint = get_object_or_404(Complaint, complaint_id=complaint_id)
        images = request.FILES.getlist('images')
        
        if not images:
            return Response(
                {'error': 'No images provided'},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        created_images = []
        for image in images:
            complaint_image = ComplaintImage.objects.create(
                complaint=complaint,
                image=image
            )
            created_images.append({
                'id': complaint_image.id,
                'image': complaint_image.image.url,
                'uploaded_at': complaint_image.uploaded_at
            })
            
        return Response({
            'complaint_id': complaint_id,
            'added_images': created_images
        }, status=status.HTTP_201_CREATED)
    
    def delete(self, request, complaint_id, image_id=None):
        """
        DELETE images request for a complaint
        """
        complaint = get_object_or_404(Complaint, complaint_id=complaint_id)
        
        if image_id:
            # Delete specific image
            image = get_object_or_404(ComplaintImage, id=image_id, complaint=complaint)
            image.delete()
            return Response(
                {'message': f'Image {image_id} deleted successfully'},
                status=status.HTTP_204_NO_CONTENT
            )
        else:
            # Delete all images for this complaint
            count, _ = complaint.images.all().delete()
            return Response(
                {'message': f'{count} images deleted successfully'},
                status=status.HTTP_204_NO_CONTENT
            )