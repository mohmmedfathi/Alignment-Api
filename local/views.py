from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from . import models
from . import serializers
from Bio import pairwise2
from Bio.Seq import Seq

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
				matrix[i][j-1] + score.gap,
				matrix[i-1][j] + score.gap,
				matrix[i-1][j-1] + (score.match if x[j-1] == y[i-1] else score.mismatch),
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

# {
# "seq1": "ATGCT",
# "seq2": "AGCT",
# "gap": -2,
# "match": 1,
# "mismatch":-1
# }

@api_view(['GET','POST'])
def Local_Get_Post(request):
    # GET
    if request.method == 'GET':
        sequences = models.Local_Model.objects.all()
        serializer = serializers.LocalSerializer(sequences, many=True)
        return Response(serializer.data)
    # POST
    elif request.method == 'POST':
        x = request.data["seq1"]
        y = request.data["seq2"]

        g = request.data["gap"]
        m = request.data["match"]
        mis = request.data["mismatch"]
      
        print('Input sequences are: ')
        print(x)
        print(y)
        print()
        

        score = ScoreParams(g,m,mis)
        best, optLoc, matrix = localAlign(x,y,score)

        print('Score matrix:')
        printMatrix(matrix)

        

        
        
        xx = pairwise2.align.localxx("AATCG", "AACG")
        align1 = xx[0][0]
        align2 = xx[0][1]
        dic = {"seq1":x,
                "seq2":y,

                "score_matrix":matrix,
                "best_score":'The best score obtained is: '+str(best),
                "alignment1":align1,
                "alignment2":align2
                }
        
        print("before")
        serializer = serializers.LocalSerializer(data=dic)
        
        if serializer.is_valid():
            print("valid")
            serializer.save()
            return Response(serializer.data, status= status.HTTP_201_CREATED)
        print("not valid")
        print(serializer.data)
        return Response(serializer.data, status= status.HTTP_400_BAD_REQUEST)