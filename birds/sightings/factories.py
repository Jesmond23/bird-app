import factory
from sightings.models import Species,Observation
from django.utils.timezone import now # type: ignore

#Used to generate test data

#Factory for creating Species object
class SpeciesFactory(factory.django.DjangoModelFactory):
    class Meta:
        model=Species

   #Default Values that are replaced in actual test
    name = "Test Bird"
    description = "A bird used in tests."
    feather_color = "Green"

#Factory for creating Observation object
class ObservationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Observation

    #Links a species automatically
    species = factory.SubFactory(SpeciesFactory)
    location = "Singapore"
    sex = "Female"
    #uses current time
    time = factory.LazyFunction(now)
    