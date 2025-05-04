from drf_spectacular.openapi import AutoSchema

from drf_spectacular.utils import OpenApiParameter, OpenApiResponse, OpenApiExample
from drf_spectacular.types import OpenApiTypes


class HeaderAutoSchema(AutoSchema):
    global_params = [
        OpenApiParameter(
            name="X-API-KEY",
            type=str,
            location=OpenApiParameter.HEADER,
            description="Application API key",
            required=True
        ),
        OpenApiParameter(
                name='Authorization',
                type=OpenApiTypes.STR,
                location=OpenApiParameter.HEADER,
                description='Knox authentication token in format "Token {token}"',
                required=False,
                examples=[
                    OpenApiExample(
                        'Auth Example',
                        value='Token abc123def456ghi789'
                    )
                ]
        ),
        OpenApiParameter(
                name='X-RESOURCE',
                type=OpenApiTypes.STR,
                location=OpenApiParameter.HEADER,
                description='The main resource being accessed',
                required=True
        ),
        OpenApiParameter(
                name='X-SUB-RESOURCE',
                type=OpenApiTypes.STR,
                location=OpenApiParameter.HEADER,
                description='The specific sub-resource being accessed',
                required=True
        ),
        OpenApiParameter(
                name='X-METHOD',
                type=OpenApiTypes.STR,
                location=OpenApiParameter.HEADER,
                description='The HTTP method that will be used (GET, POST, PUT, PATCH, DELETE)',
                required=False,
                default='GET',
                enum=['GET', 'POST', 'PUT', 'PATCH', 'DELETE']
        ),
    ]

    def get_override_parameters(self):
        params = super().get_override_parameters()
        return params + self.global_params