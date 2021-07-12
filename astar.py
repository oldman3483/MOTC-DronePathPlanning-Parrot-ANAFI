# -*- coding: utf-8 -*-
"""
Created on Tue Apr 27 14:24:17 2021

@author: ZXLi
"""
# Enter your code here. Read input from STDIN. Print output to STDOUT
class Node (object):
	def __init__(self,value,point):
		self.value = value
		self.point = point
		self.refresh()

	def refresh(self):
		self.parent = None
		self.H = 0
		self.G = 0

	def move_cost(self,other):
		return 0 if self.value == '.' else 1
		
def children(point,grid):
	x,y = point.point

	links = []
	# for d in [(max(0, x-1), y),(x,max(0, y - 1)),(x,min(len(grid[0])-1, y + 1)),(min(len(grid)-1, x+1),y)]:
	for i in [x-1, x, x+1]:
		for j in [y-1, y, y+1]:
			if i != x or j != y:
				if (i >= 0 and j >= 0 and i < len(grid) and j < len(grid[0])):
					links.append(grid[i][j])

	ret = [link for link in links if (link.value != '%')]

	return ret

def manhattan(point,point2):
	return abs(point.point[0] - point2.point[0]) + abs(point.point[1]-point2.point[1])

def euclidean(point, point2):    
    dx = point.point[0] - point2.point[0] 
    dy = point.point[1]  -point2.point[1]
    return math.sqrt(math.pow(dx, 2)+math.pow(dy, 2))

def aStar(start, goal, grid):
	#The open and closed sets
	openset = set()
	closedset = set()
	#Current point is the starting point
	current = start
	#Add the starting point to the open set
	openset.add(current)
	#While the open set is not empty
	while openset:
		#Find the item in the open set with the lowest G + H score
		current = min(openset, key=lambda o:o.G + o.H)
		#If it is the item we want, retrace the path and return it
		if current == goal:
			path = []
			while current.parent:
				path.append(current)
				current = current.parent
			path.append(current)
			return path[::-1]
		#Remove the item from the open set
		openset.remove(current)
		#Add it to the closed set
		closedset.add(current)
		#Loop through the node's children/siblings
		for node in children(current,grid):
			#If it is already in the closed set, skip it
			if node in closedset:
				continue
			#Otherwise if it is already in the open set
			if node in openset:
				#Check if we beat the G score 
				new_g = current.G + current.move_cost(node)
				if node.G > new_g:
					#If so, update the node to have a new parent
					node.G = new_g
					node.parent = current
			else:
				#If it isn't in the open set, calculate the G and H score for the node
				node.G = current.G + current.move_cost(node)
				node.H = euclidean(node, goal)
				#Set the parent to our current item
				node.parent = current
				#Add it to the set
				openset.add(node)
	#return empty list, as there is not path leading to destination
	return []
def next_move(pacman,food,grid):
	#Convert all the points to instances of Node
	for x in range(len(grid)):
		for y in range(len(grid[x])):
			grid[x][y] = Node(grid[x][y],(x,y))
	#Get the path
	path = aStar(grid[pacman[0]][pacman[1]],grid[food[0]][food[1]],grid)
	path = aStar(grid[pacman[0]][pacman[1]],grid[food[0]][food[1]],grid)
	path = aStar(grid[pacman[0]][pacman[1]],grid[food[0]][food[1]],grid)
	path = aStar(grid[pacman[0]][pacman[1]],grid[food[0]][food[1]],grid)
	#Output the path
	print (len(path) - 1)
	for node in path:
		x, y = node.point
		print (x, y)

pacman_x, pacman_y = [ int(i) for i in input().strip().split() ]
food_x, food_y = [ int(i) for i in input().strip().split() ]
x,y = [ int(i) for i in input().strip().split() ]
 
grid = []
for i in range(0, x):
	grid.append(list(input().strip()))
 
next_move((pacman_x, pacman_y),(food_x, food_y), grid)

