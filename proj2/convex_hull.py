from which_pyqt import PYQT_VER
if PYQT_VER == 'PYQT5':
	from PyQt5.QtCore import QLineF, QPointF, QObject
elif PYQT_VER == 'PYQT4':
	from PyQt4.QtCore import QLineF, QPointF, QObject
elif PYQT_VER == 'PYQT6':
	from PyQt6.QtCore import QLineF, QPointF, QObject
else:
	raise Exception('Unsupported Version of PyQt: {}'.format(PYQT_VER))

import time

# Some global color constants that might be useful
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)

# Global variable that controls the speed of the recursion automation, in seconds
#
PAUSE = 0
BIGPAUSE = 0

#
# This is the class you have to complete.
#
class ConvexHullSolver(QObject):

# Class constructor
	def __init__( self):
		super().__init__()
		self.pause = False

# Some helper methods that make calls to the GUI, allowing us to send updates
# to be displayed.

	def showTangent(self, line, color):
		self.view.addLines(line,color)
		if self.pause:
			time.sleep(PAUSE)

	def eraseTangent(self, line):
		self.view.clearLines(line)

	def blinkTangent(self,line,color):
		self.showTangent(line,color)
		time.sleep(.05)
		self.eraseTangent(line)

	def showHull(self, polygon, color):
		self.view.addLines(polygon,color)
		if self.pause:
			time.sleep(PAUSE)

	def eraseHull(self,polygon):
		self.view.clearLines(polygon)

	def showText(self,text):
		self.view.displayStatusText(text)

	def slope(self, pointA, pointB):
		return (pointB.y() - pointA.y()) / (pointB.x() - pointA.x())

	def mergeHulls(self, left, right):
		""" 
		Complexity analysis with respect to n (the number of points in the left and right hulls)

		Time complexity:
			Identifying the rightmost point in the left hull is O(n)
			Finding upper tangent is O(n)
			Finding lower tangent is O(n)
			Accessing values and concatenating existing arrays is O(1)
			Overall time complexity: O(n)

		Space complexity:
			Storing initial arrays is O(n)
			Creating temporary variables is O(1)
			Splicing and concatenating existing arrays is O(n)
			Overall space complexity: O(n)
		"""
		upper_left = max(enumerate(left), key= lambda p: p[1].x()) # I think this does argmax
		bottom_left = upper_left
		upper_right = min(enumerate(right), key= lambda p: p[1].x()) # I think this does argmin
		bottom_right = upper_right

		# find upper tangent
		left_tangent = False
		right_tangent = False
		while not (left_tangent and right_tangent): # This overall loop is O(n) time complexity
			while not left_tangent:
				# if the slope is greater than it would be by shifting upper_left to the left (minimize slope)
				if self.slope(upper_left[1], upper_right[1]) > self.slope(left[(upper_left[0] - 1) % len(left)], upper_right[1]):
					index = (upper_left[0] - 1) % len(left)
					point = left[index]
					upper_left = (index, point)
				else:
					left_tangent = True
			while not right_tangent:
				# if the slope is less than it would be by shifting upper_right to the right (maximize slope)
				if self.slope(upper_left[1], upper_right[1]) < self.slope(upper_left[1], right[(upper_right[0] + 1) % len(right)]):
					index = (upper_right[0] + 1) % len(right)
					point = right[index]
					upper_right = (index, point)
				else:
					right_tangent = True
			left_tangent = not self.slope(upper_left[1], upper_right[1]) > self.slope(left[(upper_left[0] - 1) % len(left)], upper_right[1])
			right_tangent = not self.slope(upper_left[1], upper_right[1]) < self.slope(upper_left[1], right[(upper_right[0] + 1) % len(right)])
		
		# find lower tangent
		left_tangent = False
		right_tangent = False
		while not (left_tangent and right_tangent): # This overall loop is O(n) time complexity
			while not left_tangent:
				# if the slope is less than it would be by shifting bottom_left to the right (maximize slope)
				if self.slope(bottom_left[1], bottom_right[1]) < self.slope(left[(bottom_left[0] + 1) % len(left)], bottom_right[1]):
					index = (bottom_left[0] + 1) % len(left)
					point = left[index]
					bottom_left = (index, point)
				else:
					left_tangent = True
			while not right_tangent:
				# if the slope is greater than it would be by shifting bottom_right to the left (minimize slope)
				if self.slope(bottom_left[1], bottom_right[1]) > self.slope(bottom_left[1], right[(bottom_right[0] - 1) % len(right)]):
					index = (bottom_right[0] - 1) % len(right)
					point = right[index]
					bottom_right = (index, point)
				else:
					right_tangent = True
			left_tangent = not self.slope(bottom_left[1], bottom_right[1]) < self.slope(left[(bottom_left[0] + 1) % len(left)], bottom_right[1])
			right_tangent = not self.slope(bottom_left[1], bottom_right[1]) > self.slope(bottom_left[1], right[(bottom_right[0] - 1) % len(right)])

		# Merge hulls on tangent lines
		# This process should be O(1) time complexity
		if upper_right[0] <= bottom_right[0] and upper_left[0] < bottom_left[0]:
			hull = left[:upper_left[0] + 1] + right[upper_right[0]:bottom_right[0] + 1] + left[bottom_left[0]:]
		elif upper_right[0] <= bottom_right[0] and bottom_left[0] == 0:
			hull = left[:upper_left[0] + 1] + right[upper_right[0]:bottom_right[0] + 1]
		elif bottom_right[0] == 0 and bottom_left[0] == 0:
			hull = left[:upper_left[0] + 1] + right[upper_right[0]:] + right[0:1]
		elif bottom_right[0] == 0 and upper_left[0] < bottom_left[0]:
			hull = left[:upper_left[0] + 1] + right[upper_right[0]:] + right[0:1] + left[bottom_left[0]:]
		else:
			print(f"upper_left: {upper_left[0]}")
			print(f"upper_right: {upper_right[0]}")
			print(f"bottom_right: {bottom_right[0]}")
			print(f"bottom_left: {bottom_left[0]}")
			raise Exception("Something went wrong")
		return hull

	def divide_and_conquer(self, points):
		"""
		Complexity analysis with respect to n (the number of points)
		
		Time complexity: O(nlogn)
			General form of recurrence relation is T(n) = aT(n/b) + O(n^d)
			We have a = 2, b = 2, and d = 1 = complexity of mergeHulls()
			Therefore, time complexity is T(n) = O(nlogn) by Master Theorem
		
		Space complexity: O(n)
			Prior to recursive call, space complexity is O(n) to just store the points
			within recursive call, space complexity of mergeHulls() is O(n) to
			store the points and hulls
		"""
		if len(points) < 4:
			assert(len(points) != 0)
			assert(len(points) != 1)
			hull = []
			hull.append(points[0])
			if len(points) == 3:
				if self.slope(points[0], points[1]) > self.slope(points[0], points[2]):
					hull.append(points[1])
					hull.append(points[2])
				else:
					hull.append(points[2])
					hull.append(points[1])
				return hull
			elif len(points) == 2:
				hull.append(points[1])
				return hull
		mid = len(points) // 2
		return self.mergeHulls(self.divide_and_conquer(points[:mid]), self.divide_and_conquer(points[mid:]))


	def compute_hull( self, points, pause, view):
		""" 
		I don't actuall know the time complexity of the front-end showHull() and showText() methods, but I'm assuming
		I can ignore them since they're not part of the algorithm.  I'm also assuming that the time complexity of
		sorting the points is O(nlogn) since I'm using Python's built-in sort() method, which is a Timsort algorithm.

		Overall time complexity is O(nlogn) + O(nlogn) = O(nlogn)
		Overall space complexity is O(n) + O(n) = O(n)
		"""
		self.pause = pause
		self.view = view
		assert( type(points) == list and type(points[0]) == QPointF )

		t1 = time.time()
		points.sort(key=lambda p: p.x())
		t2 = time.time()

		t3 = time.time()
		hull_points = self.divide_and_conquer(points)
		polygon = [QLineF(hull_points[i % len(hull_points)], hull_points[(i + 1) % len(hull_points)]) for i in range(len(hull_points))]
		t4 = time.time()

		self.showHull(polygon,RED)
		self.showText('Time Elapsed (Convex Hull): {:3.3f} sec'.format(t4-t3))
