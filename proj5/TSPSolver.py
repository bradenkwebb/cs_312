#!/usr/bin/python3

from which_pyqt import PYQT_VER
if PYQT_VER == 'PYQT5':
	from PyQt5.QtCore import QLineF, QPointF
elif PYQT_VER == 'PYQT4':
	from PyQt4.QtCore import QLineF, QPointF
elif PYQT_VER == 'PYQT6':
	from PyQt6.QtCore import QLineF, QPointF
else:
	raise Exception('Unsupported Version of PyQt: {}'.format(PYQT_VER))


import time
import numpy as np
from TSPClasses import *
from heapq import *
import copy
import itertools


class TSPSolver:
	def __init__( self, gui_view ):
		self._scenario = None
		self._bssf = None

	def setupWithScenario( self, scenario ):
		self._scenario = scenario


	''' <summary>
		This is the entry point for the default solver
		which just finds a valid random tour.  Note this could be used to find your
		initial BSSF.
		</summary>
		<returns>results dictionary for GUI that contains three ints: cost of solution,
		time spent to find solution, number of permutations tried during search, the
		solution found, and three null values for fields not used for this
		algorithm</returns>
	'''

	def defaultRandomTour( self, time_allowance=60.0 ):
		results = {}
		cities = self._scenario.getCities()
		ncities = len(cities)
		foundTour = False
		count = 0
		bssf = None
		start_time = time.time()
		while not foundTour and time.time()-start_time < time_allowance:
			# create a random permutation
			perm = np.random.permutation( ncities )
			route = []
			# Now build the route using the random permutation
			for i in range( ncities ):
				route.append( cities[ perm[i] ] )
			bssf = TSPSolution(route)
			count += 1
			if bssf.cost < np.inf:
				# Found a valid route
				foundTour = True
		end_time = time.time()
		results['cost'] = bssf.cost if foundTour else math.inf
		results['time'] = end_time - start_time
		results['count'] = count
		results['soln'] = bssf
		results['max'] = None
		results['total'] = None
		results['pruned'] = None
		print(f"Results for defaultRandomTour: {results}")
		if self._bssf is None or results['cost'] < self._bssf.cost:
			self._bssf = bssf
		return results


	''' <summary>
		This is the entry point for the greedy solver, which you must implement for
		the group project (but it is probably a good idea to just do it for the branch-and
		bound project as a way to get your feet wet).  Note this could be used to find your
		initial BSSF.
		</summary>
		<returns>results dictionary for GUI that contains three ints: cost of best solution,
		time spent to find best solution, total number of solutions found, the best
		solution found, and three null values for fields not used for this
		algorithm</returns>
	'''
	def greedy( self, time_allowance=60.0):
		## I need to come back to this! Not working with seed 999, prob size 15, hard (deterministic)

		cities = self._scenario.getCities()
		costMatrix = TSPCostMatrix(cities)
		S = []
		heappush(S, costMatrix)
		start_time = time.time()
		while S and time.time() - start_time < time_allowance:
			P = heappop(S)
			states = self._expand(P)
			for state in states:
				if len(state.path) == len(cities):
					potSolution = TSPSolution(state.getRoute(cities))
					if potSolution.cost < math.inf:
						bssf = potSolution
						print(f"new bssf found: {bssf.cost}")
						end_time = time.time()
						results = {}
						results['cost'] = bssf.cost
						results['time'] = end_time - start_time
						results['count'] = 0
						results['soln'] = bssf
						results['max'] = None
						results['total'] = None
						results['pruned'] = None
						print(f"Results for branch and bound: {results}")
						if self._bssf is None or results['cost'] < self._bssf.cost:
							self._bssf = bssf
						return results
				else:
					heappush(S, state)

		end_time = time.time()
		results = {}
		results['cost'] = bssf.cost
		results['time'] = end_time - start_time
		results['count'] = 0
		results['soln'] = bssf
		results['max'] = None
		results['total'] = None
		results['pruned'] = None
		print(f"Results for branch and bound: {results}")
		if self._bssf is None or results['cost'] < self._bssf.cost:
			self._bssf = bssf
		return results


		# cities = self._scenario.getCities()
		# bssf = None
		# start_time = time.time()
		
		# for start_city in sorted(cities, key= lambda x: x._name):
		# 	results = {}
		# 	visited = set()
		# 	ignore = set()
		# 	not_visited = set(cities)
			
		# 	cur_city = start_city
		# 	route = [cur_city]
		# 	visited.add(cur_city)
		# 	not_visited.remove(cur_city)

		# 	while not_visited and time.time() - start_time < time_allowance:
		# 		next = min(not_visited.difference(ignore), key = lambda x: cur_city.costTo(x), default=None)
		# 		if next == None: # this should happen only if the city can't reach any of the other cities
		# 			prev_city = route.pop()
		# 			not_visited.add(prev_city)
		# 			visited.remove(prev_city)
		# 			ignore.clear()
		# 			ignore.add(cur_city)
		# 			cur_city = route[-1]
		# 		if cur_city.costTo(next) == math.inf:
		# 			ignore.add(next)
		# 			prev_city = route.pop()
		# 			not_visited.add(prev_city)
		# 			visited.remove(prev_city)
		# 			cur_city = route[-1]
		# 			continue
		# 		else:
		# 			ignore.clear()
		# 		visited.add(next)
		# 		not_visited.remove(next)
		# 		route.append(next)
		# 		cur_city = next
			
		# 	print(f"start_city: {start_city._name}")
		# 	print(f"route at end: {[city._name for city in route]}")
		# 	if len(route) == len(cities):
		# 		if route[-1].costTo(route[0]) < math.inf:
		# 			break
		# print([city._name for city in route])
		# bssf = TSPSolution(route)
		# end_time = time.time()
		
		# results['cost'] = bssf.cost
		# results['time'] = end_time - start_time
		# results['count'] = 0 #maybe this should just be 0
		# results['soln'] = bssf
		# results['max'] = None
		# results['total'] = None
		# results['pruned'] = None
		# print(f"Results for greedy: {results}")
		# if self._bssf is None or results['cost'] < self._bssf.cost:
		# 	self._bssf = bssf
		# return results


	''' <summary>
		This is the entry point for the branch-and-bound algorithm that you will implement
		</summary>
		<returns>results dictionary for GUI that contains three ints: cost of best solution,
		time spent to find best solution, total number solutions found during search (does
		not include the initial BSSF), the best solution found, and three more ints:
		max queue size, total number of states created, and number of pruned states.</returns>
	'''
	def branchAndBound( self, time_allowance=60.0 ):
		cities = self._scenario.getCities()
		costMatrix = TSPCostMatrix(cities)
		pruneCount = 0
		stateCount = 1
		solnCount = 0
		intNodeCount = 0
		maxQueueSize = 0
		S = []
		heappush(S, costMatrix)
		start_time = time.time()
		bssf = self.greedy(time_allowance=time_allowance)['soln']
		i = 0
		while S and time.time() - start_time < time_allowance:
			i += 1
			maxQueueSize = max(maxQueueSize, len(S))
			P = heappop(S)
			if P.cost < bssf.cost:
				states = self._expand(P)
				stateCount += len(states)
				intNodeCount += 1
				for state in states:
					if len(state.path) == len(cities):
						potSolution = TSPSolution(state.getRoute(cities))
						if potSolution.cost < bssf.cost:
							bssf = potSolution
							print(f"new bssf found: {bssf.cost}")
							solnCount += 1
						else:
							pruneCount += 1
					elif state.cost < bssf.cost:
						heappush(S, state)
					else:
						pruneCount += 1
			else:
				pruneCount += 1
			if i % 200 == 0:
				assert stateCount - solnCount - pruneCount - intNodeCount - len(S) == 0, "stateCount - solnCount - pruneCount - intNodeCount - len(S) != 0"
				print(f"i: {i}\tlen(S): {len(S)}\tmaxQueueSize: {maxQueueSize}\tstateCount: {stateCount}\tpruneCount: {pruneCount}\tintNodeCount: {intNodeCount}\tsolnCount: {solnCount}\tbssf: {bssf.cost}")
		
		end_time = time.time()
		results = {}
		results['cost'] = bssf.cost
		results['time'] = end_time - start_time
		results['count'] = solnCount
		results['soln'] = bssf
		results['max'] = maxQueueSize
		results['total'] = stateCount
		results['pruned'] = pruneCount
		print(f"Results for branch and bound: {results}")
		if self._bssf is None or results['cost'] < self._bssf.cost:
			self._bssf = bssf
		return results
	
	def _expand(self, costMatrix):
		states = []
		mostRecentCityIndex = costMatrix.path[-1]
		for cityIndex in range(len(costMatrix.matrix[mostRecentCityIndex])):
			if costMatrix.matrix[mostRecentCityIndex][cityIndex] < math.inf:
				newMatrix = copy.deepcopy(costMatrix)
				newMatrix.addCity(cityIndex)
				states.append(newMatrix)
		return sorted(states)


	''' <summary>
		This is the entry point for the algorithm you'll write for your group project.
		</summary>
		<returns>results dictionary for GUI that contains three ints: cost of best solution,
		time spent to find best solution, total number of solutions found during search, the
		best solution found.  You may use the other three field however you like.
		algorithm</returns>
	'''

	def fancy( self,time_allowance=60.0 ):
		pass
