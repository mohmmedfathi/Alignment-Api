from django.db import models
# from matrix_field import MatrixField

# Create your models here.

class Local_Model(models.Model):
        seq1 = models.CharField(max_length=200,null = False)
        seq2 = models.CharField(max_length=100,null = False)
        
        score_matrix = models.TextField(null = True)
        best_score = models.IntegerField()

        alignment1 = models.CharField(max_length=100,null = False)
        alignment2 = models.CharField(max_length=100,null = False)

        
        
