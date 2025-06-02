from django.test import TestCase
import json
from django.urls import reverse
from django.urls import reverse_lazy
from rest_framework.test import APITestCase
from sightings.models import Species, Observation
from sightings.serializers import SpeciesSerializer,ObservationSerializer
from datetime import datetime
from sightings.factories import SpeciesFactory, ObservationFactory
from django.utils.timezone import make_aware
# Create your tests here.

class SpeciesSerializerTest(APITestCase):
    def setUp(self):
        self.species = SpeciesFactory(name='Blue Jay', feather_color = 'Blue and Black')


        self.serializer = SpeciesSerializer(instance = self.species)

    #Test whether SpeciesSerializer returns correct fields and data for a species object
    def test_species_serializer_fields(self):
        data = self.serializer.data
        self.assertEqual(set(data.keys()),{'id','name','description','feather_color'})
        
    def test_species_serializer_name(self):
        data = self.serializer.data
        self.assertEqual(data['name'],'Blue Jay')

#Create a Species and an Observation object using factories
class ObservationEndpointTest(APITestCase):
    def setUp(self):
       self.species = SpeciesFactory(name = 'Northern Cardinal', feather_color = 'Red')

       self.observation = ObservationFactory(
           species = self.species,
           location='Chicago',
           sex='Male',
           time=make_aware(datetime.strptime('2023-06-15 08:30', '%Y-%m-%d %H:%M'))
       )

    #Test to see if the given observation returns true
    def test_list_observations(self):
        response = self.client.get(reverse('sightings:observations'))
        self.assertEqual(response.status_code,200)
        self.assertEqual(len(response.data),1)
        self.assertEqual(response.data[0]['location'],'Chicago')

    #Test to see if the given month corresponds to the test month
    def test_observations_by_month(self):
        response = self.client.get(reverse('sightings:observations-by-month') + '?month=6')
        self.assertEqual(response.status_code,200)
        self.assertEqual(len(response.data),1)
        self.assertEqual(response.data[0]['species']['feather_color'],'Red')

    #Test to see if the number of sightings based on location corresponds to test value
    def test_species_count_by_location(self):
        ObservationFactory(
            species=self.species,
            location='Chicago',
            sex='Female',
            time = make_aware(datetime.now())
        )
        response = self.client.get(reverse('sightings:species-count-by-location'))
        self.assertEqual(response.status_code,200)
        self.assertGreaterEqual(response.data[0]['species_count'],1)