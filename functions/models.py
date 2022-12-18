from django.db import models

# Create your models here.

class SwissProt_Model(models.Model):
    url = models.URLField()
    downlaoded = models.BooleanField()
    data = models.TextField()
    
    Identification = models.CharField(max_length=200,null = True)
    Accession_number = models.CharField(max_length=80,null = True)
    Date = models.CharField(max_length=100,null = True)
    Description = models.CharField(max_length=500,null = True)
    Gene_name = models.CharField(max_length=300,null = True)
    Organism_species = models.CharField(max_length=300,null = True)
    Organelle = models.CharField(max_length=300,null = True)
    Organism_classification = models.CharField(max_length=300,null = True)
    Reference_info = models.CharField(max_length=300,null = True)

    Comments_or_notes_attached = models.CharField(max_length=600,null = True)
    Database_cross_references = models.CharField(max_length=600,null = True)
    Keywords = models.CharField(max_length=300,null = True)
    Feature_table_data = models.CharField(max_length=300,null = True)
    Sequence = models.CharField(max_length=300,null = True)

