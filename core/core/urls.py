
from django.contrib import admin
from django.urls import path , include
from django.views.generic import TemplateView



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('imdb.urls')),
    path('api-auth/', include('rest_framework.urls')),
        path(
        "swagger-ui/",
        TemplateView.as_view(
            template_name="swagger-ui.html",
            extra_context={"schema_url": "openapi-schema"},
        ),
        name="swagger-ui",
    ),
]
