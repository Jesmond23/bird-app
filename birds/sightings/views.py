from django.shortcuts import redirect, render
from rest_framework import generics, filters
from .models import Species,Observation
from .serializers import SpeciesSerializer,ObservationSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Count
from django.utils.dateparse import parse_datetime
from rest_framework import status

from django.urls import reverse
from django.http import HttpResponseRedirect

from datetime import datetime

from drf_spectacular.utils import extend_schema, OpenApiParameter


# Create your views here.

#Class-based view


#REST API endpoint to list and create species
@extend_schema(tags=["Species"])
class SpeciesListCreate(generics.ListCreateAPIView):
    queryset = Species.objects.all()
    serializer_class = SpeciesSerializer


#REST API endpoint to list and create observation with optional ordering by time
@extend_schema(tags=["Observation"])
class ObservationListCreate(generics.ListCreateAPIView):
    queryset = Observation.objects.all()
    serializer_class = ObservationSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['time']


#REST API endpoint to filter observation based on month through provided query parameter
@extend_schema(
    parameters=[
        OpenApiParameter(
            name='month',
            description='Month (1-12) to filter observations by',
            required=True,
            type=int
        )
    ]
)

class ObservationByMonth(APIView):
    def get(self,request):
        month = request.GET.get('month')
        if not month:
            return Response({'error':'Month Parameter is required'}, status=400)
        
        try:
            month = int(month)
        except ValueError:
            return Response({'error':'Invalid Month'},status =400)

        obs = Observation.objects.filter(time__month = month)
        serializer = ObservationSerializer(obs,many=True)
        return Response(serializer.data)
    


#REST API endpoint to filter observation based on color through provided query parameter
@extend_schema(
    parameters=[
        OpenApiParameter(
            name='color',
            description='Feather color to filter observations by (e.g., "Red")',
            required=True,
            type=str
        )
    ]
)

class ObservationByFeatherColor(APIView):
    def get(self,request):
        color = request.GET.get('color')
        if not color:
            return Response({'error':'Feather color is required'},status = 400)
        
        obs = Observation.objects.filter(species__feather_color__icontains = color)
        serializer = ObservationSerializer(obs,many=True)
        return Response(serializer.data)
    

#REST API endpoint to get species count grouped by observation location
class SpeciesCountByLocation(APIView):
    def get(self,request):
        data = (
            Observation.objects
            .values('location')
            .annotate(species_count = Count('species', distinct=True))
            .order_by('-species_count')
        )
        return Response(data)
    

#Import Django forms for rendering HTML form submissions
from .forms import ObservationForm
from .forms import SpeciesForm

#HTML view-Submit a new bird observation via form
def submit_observation(request):
    if request.method == 'POST':
        form = ObservationForm(request.POST)
        if form.is_valid():
            form.save()
            #Redirect after successful submission
            return HttpResponseRedirect(reverse('sightings:submit_success') + '?type=observation')
    else:
        form = ObservationForm()
    return render(request, 'submit_observation.html', {'form': form})

#HTML view- Submit a new bird species via form
def submit_species(request):
    if request.method =='POST':
        form = SpeciesForm(request.POST)
        if form.is_valid():
            form.save()
            #Redirect after successful submission
            from django.http import HttpResponseRedirect
            return HttpResponseRedirect(reverse('sightings:submit_success') + '?type=species')

    else:
        form = SpeciesForm()
    return render(request,'submit_species.html',{'form': form})

#HTML view-Success page after form submission
def submit_success(request):
    submission_type = request.GET.get('type', 'observation')  # Default to observation
    return render(request, 'submit_success.html', {'type': submission_type})