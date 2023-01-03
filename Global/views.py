from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from . import models
from . import serializers
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
class ScoreParams:
    '''
    Define scores for each parameter
    '''
    def __init__(self,gap,match,mismatch):
        self.gap = gap
        self.match = match
        self.mismatch = mismatch

    def misMatchChar(self,x,y):
        if x != y:
            return self.mismatch
        else:
            return self.match

def getMatrix(sizeX,sizeY,gap):
    '''
    Create an initial matrix of zeros, such that its len(x) x len(y)
    '''
    matrix = []
    for i in range(len(sizeX)+1):
        subMatrix = []
        for j in range(len(sizeY)+1):
            subMatrix.append(0)
        matrix.append(subMatrix)

    # Initializing the first row and first column with the gap values
    for j in range(1,len(sizeY)+1):
        matrix[0][j] = j*gap
    for i in range(1,len(sizeX)+1):
        matrix[i][0] = i*gap
    return matrix

def getTraceBackMatrix(sizeX,sizeY):
    '''
    Create an initial matrix of zeros, such that its len(x) x len(y)
    '''
    matrix = []
    for i in range(len(sizeX)+1):
        subMatrix = []
        for j in range(len(sizeY)+1):
            subMatrix.append('0')
        matrix.append(subMatrix)

    # Initializing the first row and first column with the up or left values
    for j in range(1,len(sizeY)+1):
        matrix[0][j] = 'left'
    for i in range(1,len(sizeX)+1):
        matrix[i][0] = 'up'
    matrix[0][0] = 'done'
    return matrix


def globalAlign(x,y,score):
    '''
    Fill in the matrix with alignment scores
    '''
    matrix = getMatrix(x,y,score.gap)
    traceBack = getTraceBackMatrix(x,y)

    for i in range(1,len(x)+1):
        for j in range(1,len(y)+1):
            left = matrix[i][j-1] + score.gap
            up = matrix[i-1][j] + score.gap
            diag = int(matrix[i-1][j-1]) + score.misMatchChar(x[i-1],y[j-1])
            matrix[i][j] = max(left,up,diag)
            if matrix[i][j] == left:
                traceBack[i][j] = 'left'
            elif matrix[i][j] == up:
                traceBack[i][j] = 'up'
            else:
                traceBack[i][j] = 'diag'
    return matrix,traceBack

def getAlignedSequences(x,y,matrix,traceBack):
    '''
    Obtain x and y globally aligned sequence arrays using the bottom-up approach
    '''
    xSeq = []
    ySeq = []
    i = len(x)
    j = len(y)
    while(i > 0 or j > 0):
        if traceBack[i][j] == 'diag':
            # Diag is scored when x[i-1] == y[j-1]
            xSeq.append(x[i-1])
            ySeq.append(y[j-1])
            i = i-1
            j = j-1
        elif traceBack[i][j] == 'left':
            # Left holds true when '-' is added from x string and y[j-1] from y string
            xSeq.append('-')
            ySeq.append(y[j-1])
            j = j-1
        elif traceBack[i][j] == 'up':
            # Up holds true when '-' is added from y string and x[j-1] from x string
            xSeq.append(x[i-1])
            ySeq.append('-')
            i = i-1
        elif traceBack[i][j] == 'done':
            # Break condition when we reach the [0,0] cell of traceback matrix
            break
    return xSeq,ySeq

def printMatrix(matrix):
    '''
    Create a custom function to print the matrix
    '''
    for i in range(len(matrix)):
        print(matrix[i])
    

@api_view(['GET','POST'])
def Global_Get_Post(request):
    # GET
    if request.method == 'GET':
        sequences = models.Global_Model.objects.all()
        serializer = serializers.GlobalSerializer(sequences, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        #{ "seq1":"aaac", "seq2":"agc", "gap" : -2, "match":1, "mismatch" : -1 }
    
        x = request.data["seq1"]
        y = request.data["seq2"]
        g = request.data["gap"]
        m = request.data["match"]
        mis = request.data["mismatch"]

        
        score = ScoreParams(g,m,mis)
        matrix,traceBack = globalAlign(x,y,score)

        xSeq,ySeq = getAlignedSequences(x,y,matrix,traceBack)

        xSeqStr = ''.join(xSeq[::-1])
        ySeqStr = ''.join(ySeq[::-1])
       
        
        matrix_str = ','.join(str(v) for v in matrix)

        traceBack_str = ','.join(str(v) for v in traceBack)
        
        data_dictionary = {

                "seq1":x,
                "seq2":y,

                "aligned1":xSeqStr,
                "aligned2":ySeqStr,

                "score_matrix":matrix_str,
                "traceback_matrix":traceBack_str

                }
        
        
        serializer = serializers.GlobalSerializer(data=data_dictionary)
        
        if serializer.is_valid():    
            serializer.save()
            return Response(serializer.data, status= status.HTTP_201_CREATED)
        
        return Response({"status": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)