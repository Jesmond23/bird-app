from rest_framework import serializers
from .models import Species, Observation


class SpeciesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Species
        fields = ['id', 'name', 'description', 'feather_color']

class ObservationSerializer(serializers.ModelSerializer):
    species_id = serializers.PrimaryKeyRelatedField(
        queryset=Species.objects.all(), source='species', write_only=True
    )
    species = SpeciesSerializer(read_only=True)

    class Meta:
        model = Observation
        fields = ['id', 'species', 'species_id', 'location', 'sex', 'time']