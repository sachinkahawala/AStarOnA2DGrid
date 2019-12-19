import numpy
from heapq import *
import math

def heuristic(a, b):
	xd,yd=b[0] - a[0],b[1] - a[1]
	# Euclidian Distance
	d=math.sqrt(xd*xd+yd*yd)
	# Manhattan distance
	# d = abs(xd) + abs(yd)
	# Chebyshev distance
	# d = max(abs(xd), abs(yd))
	return d

def aStar(array, start, end , x, y):
	tempHeap = []
	neighbors = [(0,1),(0,-1),(1,0),(-1,0),(1,1),(1,-1),(-1,1),(-1,-1)]
	finished = set()
	pred = {}
	gScore = {start:0}
	fScore = {start:heuristic(start, end)}
	heappush(tempHeap, (fScore[start], start))
	while tempHeap:
		#print(tempHeap)
		current = heappop(tempHeap)[1]
		if current == end:
			Answer = []
			while current in pred:
				Answer.append(current)
				current = pred[current]
			return Answer
		finished.add(current)
		for i, j in neighbors:
			#print(1)
			neighborX, neighborY = current[0] + i, current[1] + j
			neighbor = (neighborX, neighborY)
			newScore = gScore[current] + heuristic(current, neighbor)
			if 0<=neighborX<x and 0<=neighborY<y and array[neighborX][neighborY] == 1 :
				continue
			if neighbor in finished and neighbor in  gScore and newScore >= gScore[neighbor]:
				continue
			if 0<=neighborX<x and 0<=neighborY<y:
				if  (neighbor in  gScore and newScore < gScore[neighbor]) or neighbor not in [i[1]for i in tempHeap]:
					pred[neighbor] = current
					gScore[neighbor] = newScore
					fScore[neighbor] = newScore + heuristic(neighbor, end)
					heappush(tempHeap, (fScore[neighbor], neighbor))

	return []
