from django.urls import path
#Import all endpoints
from .views import (SpeciesListCreate,
 ObservationListCreate,
 ObservationByMonth,
 ObservationByFeatherColor,
 SpeciesCountByLocation,
 submit_observation,
 submit_species,
 submit_success,
 )

#Namespace declaration to ensure reverse URL resolution works
app_name = 'sightings'

#Connect API endpoints to their logic
urlpatterns=[
    path('species/', SpeciesListCreate.as_view(), name='species'),
    path('observations/', ObservationListCreate.as_view(), name='observations'),
    path('observations/by_month/', ObservationByMonth.as_view(), name='observations-by-month'),
    path('observations/by_feather_color/', ObservationByFeatherColor.as_view(), name='observations-by-feather-color'),
    path('summary/species_count_by_location/', SpeciesCountByLocation.as_view(), name='species-count-by-location'),

    #HTML form submission for POST request(Species, Observation)
    path('submit_observation/', submit_observation,name='submit-observation'),
    path('submit_species/', submit_species,name='submit-species'),
    path('submit_success/', submit_success, name='submit_success')
]

