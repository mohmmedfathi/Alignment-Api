from django.db import models
# from matrix_field import MatrixField

# Create your models here.

class Global_Model(models.Model):
        seq1 = models.CharField(max_length=100,null = False)
        seq2 = models.CharField(max_length=100,null = False)
        
        aligned1 = models.CharField(max_length=100,null = False)
        aligned2 = models.CharField(max_length=100,null = False)

        score_matrix = models.TextField(null = True)
        traceback_matrix = models.TextField(null = True)
