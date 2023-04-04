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
		print(f"DefaultRandomTour: {results['cost']}")
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
		bssf = None
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
		results['cost'] = bssf.cost if bssf else math.inf
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
		start_time = time.time()
		bssf = self.greedy(time_allowance=time_allowance)['soln']		
		if bssf is None:
			print("Greedy failed to find a solution")
		else:
			heappush(S, costMatrix)
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
			if i % 1000 == 0:
				assert stateCount - solnCount - pruneCount - intNodeCount - len(S) == 0, "stateCount - solnCount - pruneCount - intNodeCount - len(S) != 0"
				print(f"i: {i}\tlen(S): {len(S)}\tmaxQueueSize: {maxQueueSize}\tstateCount: {stateCount}\tpruneCount: {pruneCount}\tintNodeCount: {intNodeCount}\tsolnCount: {solnCount}\tbssf: {bssf.cost}")
		end_time = time.time()
		elapsed_time = end_time - start_time
		if elapsed_time > time_allowance and bssf:
			pruneCount += len([state for state in S if state.cost > bssf.cost])

		results = {}
		results['cost'] = bssf.cost if bssf else math.inf
		results['time'] = elapsed_time
		results['count'] = solnCount
		results['soln'] = bssf
		results['max'] = maxQueueSize
		results['total'] = stateCount
		results['pruned'] = pruneCount
		print(f"Results for branch and bound: {results}")
		if self._bssf is None or results['cost'] < self._bssf.cost:
			self._bssf = bssf
		elif bssf is not None and len(S) == 0:
			print("Optimal result!!!")
		return results
	
	def _expand(self, costMatrix):
		states = []
		mostRecentCityIndex = costMatrix.path[-1]
		for cityIndex in range(len(costMatrix.matrix[mostRecentCityIndex])):
			if costMatrix.matrix[mostRecentCityIndex][cityIndex] < math.inf:
				newMatrix = copy.deepcopy(costMatrix)
				newMatrix.addCity(cityIndex)
				states.append(newMatrix)
		return sorted(states) # maybe don't sort?


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
