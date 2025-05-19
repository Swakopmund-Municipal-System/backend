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

# API Documentation
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiResponse, OpenApiExample
from drf_spectacular.types import OpenApiTypes

from drf_spectacular.utils import inline_serializer
from rest_framework import serializers

# Define serializer schemas for documentation
report_list_response = inline_serializer(
    name='ReportListResponse',
    fields={
        'count': serializers.IntegerField(),
        'results': ReportSerializer(many=True)
    }
)
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

    @extend_schema(
        summary="List all environmental reports",
        description="Returns a list of all environmental reports, optionally filtered by title",
        parameters=[
            OpenApiParameter(
                name="title",
                description="Filter reports by title (case-insensitive)",
                required=False,
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY
            ),
        ],
        responses={
            200: report_list_response,
        }
    )
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

    @extend_schema(
        summary="Retrieve a specific environmental report",
        description="Returns details of a specific environmental report by ID",
        parameters=[
            OpenApiParameter(
                name="report_id",
                description="Unique identifier of the report",
                required=True,
                type=OpenApiTypes.UUID,
                location=OpenApiParameter.PATH
            ),
        ],
        responses={
            200: ReportSerializer,
            404: OpenApiResponse(
                description="Report not found",
                examples=[
                    OpenApiExample(
                        "Not Found",
                        value={"detail": "Not found."}
                    )
                ]
            )
        }
    )
    def get_detail(self, request, report_id):
        pass


    @extend_schema(
        summary="Create a new environmental report",
        description="Creates a new environmental report with the provided data",
        request=ReportSerializer,
        responses={
            201: ReportSerializer,
            400: OpenApiResponse(
                description="Invalid input",
                examples=[
                    OpenApiExample(
                        "Validation Error",
                        value={
                            "title": ["This field is required."],
                            "details": ["This field is required."]
                        }
                    )
                ]
            )
        },
        examples=[
            OpenApiExample(
                "Valid Report",
                value={
                    "title": "Air Quality Report Q1 2025",
                    "details": "Quarterly air quality assessment for urban areas"
                },
                request_only=True
            )
        ]
    )
    def post(self, request):
        """
        POST requests
        """
        serializer = ReportSerializer(data=request.data, context={'request': request})
        print(f"Auth Data: {request.user.id}")
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    @extend_schema(
        summary="Update an environmental report",
        description="Completely replaces an existing environmental report with new data",
        parameters=[
            OpenApiParameter(
                name="report_id",
                description="Unique identifier of the report to update",
                required=True,
                type=OpenApiTypes.UUID,
                location=OpenApiParameter.PATH
            ),
        ],
        request=ReportSerializer,
        responses={
            200: ReportSerializer,
            400: OpenApiResponse(
                description="Invalid input",
                examples=[
                    OpenApiExample(
                        "Validation Error",
                        value={
                            "title": ["Ensure this field has no more than 50 characters."],
                            "details": ["Ensure this field has no more than 250 characters."]
                        }
                    )
                ]
            ),
            404: OpenApiResponse(description="Report not found")
        },
        examples=[
            OpenApiExample(
                "Valid Update",
                value={
                    "title": "Updated Air Quality Report Q1 2025",
                    "details": "Updated quarterly air quality assessment for urban areas"
                },
                request_only=True
            )
        ]
    )
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


    @extend_schema(
        summary="Partially update an environmental report",
        description="Updates specific fields of an existing environmental report",
        parameters=[
            OpenApiParameter(
                name="report_id",
                description="Unique identifier of the report to update",
                required=True,
                type=OpenApiTypes.UUID,
                location=OpenApiParameter.PATH
            ),
        ],
        request=ReportSerializer,
        responses={
            200: ReportSerializer,
            400: OpenApiResponse(description="Invalid input"),
            404: OpenApiResponse(description="Report not found")
        },
        examples=[
            OpenApiExample(
                "Partial Update",
                value={
                    "title": "Renamed Air Quality Report"
                },
                request_only=True
            )
        ]
    )
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



    @extend_schema(
        summary="Delete an environmental report",
        description="Permanently removes an environmental report",
        parameters=[
            OpenApiParameter(
                name="report_id",
                description="Unique identifier of the report to delete",
                required=True,
                type=OpenApiTypes.UUID,
                location=OpenApiParameter.PATH
            ),
        ],
        responses={
            204: OpenApiResponse(
                description="Report successfully deleted",
                examples=[
                    OpenApiExample(
                        "Success",
                        value={"message": "Report deleted successfully"}
                    )
                ]
            ),
            404: OpenApiResponse(description="Report not found")
        }
    )
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


