import os 
import sys
import django
import csv
from datetime import datetime

#Setup DJANGO environment
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE','birds.settings')
django.setup()

from sightings.models import Species, Observation

#Import CSV File
DATA_FILE = 'Birdsoftheworld.csv'

#Clear existing records if any
Observation.objects.all().delete()
Species.objects.all().delete()

species_cache = {}

with open(DATA_FILE, newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        species_name = row['species'].strip()
        description = row['description of bird'].strip()
        feather_color = row['feather color'].strip()

        #GET or CREATE species
        if species_name not in species_cache:
            species_obj, created = Species.objects.get_or_create(
                name=species_name,
                defaults={
                    'description':description,
                    'feather_color':feather_color
                }
            )

            species_cache[species_name] =species_obj
        else:
            species_obj = species_cache[species_name]
        
        try:
            observation_time = datetime.strptime(row['time'].strip(),'%d-%m-%Y %H:%M')
        except ValueError:
            print(f"Invalid date format for row:{row}")
            continue

        Observation.objects.create(
            species=species_obj,
            location=row['location'].strip(),
            sex=row['sex'].strip() or "Unknown",
            time=observation_time
        )
print("Data successfully loaded")