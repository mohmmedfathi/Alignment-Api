from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from . import models
from . import serializers
from Bio import pairwise2


# Create your views here.

class ScoreParams:
	'''
	Define scores for each parameter
	'''
	def __init__(self,gap,match,mismatch):
		self.gap = gap
		self.match = match
		self.mismatch = mismatch

def getMatrix(sizeX,sizeY):
	'''
	Create an empty matrix of zeros, such that its len(y) x len(x)
	'''
	matrix = []
	for i in range(len(sizeY)+1):
		subMatrix = []
		for j in range(len(sizeX)+1):
			subMatrix.append(0)
		matrix.append(subMatrix)
	return matrix

def localAlign(x,y,score):
	'''
	Fill in the matrix with alignment scores and obtain the best score and position
	'''
	matrix = getMatrix(x,y)
	best = 0
	optLoc = (0,0)

	for i in range(1,len(y)+1):
		for j in range(1,len(x)+1):
			matrix[i][j] = max(
                matrix[i][j - 1] + int(score.gap),
                matrix[i - 1][j] + int(score.gap),
                matrix[i - 1][j - 1] + (int(score.match) if x[j - 1] == y[i - 1] else int(score.mismatch)),
                0
				)

			if matrix[i][j] >= best:
				best = matrix[i][j]
				optLoc = (i,j)

	return best, optLoc, matrix

def printMatrix(matrix):
	'''
	Create a custom function to print the matrix
	'''
	for i in range(len(matrix)):
		print(matrix[i])
	print()

def getSequence(x,best,optLoc,matrix):
	'''
	Obtaining the locally aligned sequence using matrix
	'''
	seq = ''
	i = optLoc[0]
	j = optLoc[1]

	while(i > 0 or j > 0):

		diag = matrix[i-1][j-1]
		up = matrix[i-1][j]
		left = matrix[i][j-1]

		if min(diag,left,up) == diag:
			# Break condition when diag score is the maximum
			break
		else:
			# Adding to the sequence
			i = i - 1
			j = j - 1
			seq += x[j]
	return seq[::-1]

{
"seq1": "ATGCT",
"seq2": "AGCT",
"gap": -2,
"match": 1,
"mismatch":-1
}


@api_view(['GET','POST'])
def Local_Get_Post(request):
    
    if request.method == 'GET':
        sequences = models.Local_Model.objects.all()
        serializer = serializers.LocalSerializer(sequences, many=True)
        return Response(serializer.data)
    

    elif request.method == 'POST':
        x = request.data["seq1"]
        y = request.data["seq2"]

        g = request.data["gap"]
        m = request.data["match"]
        mis = request.data["mismatch"]

        score = ScoreParams(g,m,mis)
        best, optLoc, matrix = localAlign(x,y,score)

        
        xx = pairwise2.align.localxx(x, y)
        align1 = xx[0][0]
        align2 = xx[0][1]
		
		
        matrix_str = ','.join(str(v) for v in matrix)
		
    
        
        data_dicitonary = {
				"seq1":x,
                "seq2":y,

                "score_matrix":matrix_str,
                "best_score":best,

                "alignment1":align1,
                "alignment2":align2
                }
        
    
        serializer = serializers.LocalSerializer(data=data_dicitonary)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status= status.HTTP_201_CREATED)

        
        return Response({"status": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)