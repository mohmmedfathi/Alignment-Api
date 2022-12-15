from rest_framework.decorators import renderer_classes, api_view
from rest_framework_swagger.renderers import OpenAPIRenderer, SwaggerUIRenderer
import coreapi
from rest_framework import response
# noinspection PyArgumentList
@api_view()
@renderer_classes([SwaggerUIRenderer, OpenAPIRenderer])
def schema_view(request):
    print("---inside schema view-----")
    # noinspection PyArgumentList
    schema = coreapi.Document(
    title='Your Title',
    url='Your host url',
    content={
        'search': coreapi.Link(
            url='/search/',
            action='get',
            fields=[
                coreapi.Field(
                    name='from',
                    required=True,
                    location='query',
                    description='City name or airport code.'
                ),
                coreapi.Field(
                    name='to',
                    required=True,
                    location='query',
                    description='City name or airport code.'
                ),
                coreapi.Field(
                    name='date',
                    required=True,
                    location='query',
                    description='Flight date in "YYYY-MM-DD" format.'
                )
            ],
            description='Return flight availability and prices.'
        )
    }
)
    # schema = generator.get_schema(request)
    return response.Response(schema)