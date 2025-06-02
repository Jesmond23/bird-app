from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('api/', include('sightings.urls')),

    # OpenAPI schema
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    
    # Swagger UI
    path('', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),

    path('api/', include('sightings.urls', namespace='sightings')),

]
