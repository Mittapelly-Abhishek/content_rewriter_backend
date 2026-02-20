from django.contrib import admin
from django.urls import path, include

# Swagger imports
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


# -------------------------------
# SWAGGER CONFIG
# -------------------------------
schema_view = get_schema_view(
    openapi.Info(
        title="Content Rewriter API",
        default_version='v1',
        description="API for AI Content Rewriting, Voice, and History Management",
        contact=openapi.Contact(email="support@example.com"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


# -------------------------------
# URL PATTERNS
# -------------------------------
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('core.urls')),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='redoc'),
]