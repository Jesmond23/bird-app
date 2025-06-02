from django.db import models

# Create your models here.

#Species Database Table
class Species(models.Model):
    #Attributes
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    feather_color = models.CharField(max_length = 100)

    #Make instances show by name
    def __str__(self):
        return self.name

#Observation of a bird Database Table
class Observation(models.Model):
    #Attributes
    #Links observation to the bird species
    species = models.ForeignKey(Species, on_delete=models.CASCADE)
    location = models.CharField(max_length=100)
    sex = models.CharField(
        max_length=20,
        choices=[
            ("Male", "Male"),
            ("Female", "Female"),
            ("Unknown", "Unknown")
        ]
    )
    time = models.DateTimeField()