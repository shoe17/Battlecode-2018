import battlecode as bc
import random
import sys
import traceback
import os
import collections
import heapq
print(os.getcwd())

print("pystarting")

# A GameController is the main type that you talk to the game with.
# Its constructor will connect to a running game.
gc = bc.GameController()
#directions = list(bc.Direction)
directions = [bc.Direction.North, bc.Direction.Northeast, bc.Direction.East, bc.Direction.Southeast, bc.Direction.South, bc.Direction.Southwest, bc.Direction.West, bc.Direction.Northwest, bc.Direction.Center]
tryRotate = [0, -1, 1, -2, 2]

print("pystarted")

# It's a good idea to try to keep your bots deterministic, to make debugging easier.
# determinism isn't required, but it means that the same things will happen in every thing you run,
# aside from turns taking slightly different amounts of time due to noise.
random.seed(6137)



my_team = gc.team()
if my_team == bc.Team.Red:
	other_team = bc.Team.Blue
else:
	other_team = bc.Team.Red


def invert(loc):
	newx = earthMap.width-loc.x - 1
	newy = earthMap.height-loc.y - 1
	return bc.MapLocation(bc.Planet.Earth,newx,newy)

def locToStr(loc):
	return '('+str(loc.x)+','+str(loc.y)+')'

def chooseLandingLocation():
	while True:
		landx = random.randint(0, marsMap.width - 1)
		landy = random.randint(0, marsMap.height - 1)
		land_loc = bc.MapLocation(bc.Planet.Mars, landx, landy)
		if marsMap.is_passable_terrain_at(land_loc):
			return land_loc

class mmap():
	def __init__(self,width,height):
		self.width=width
		self.height=height
		self.arr=[[0]*self.height for i in range(self.width)];
	def onMap(self,loc):
		if (loc.x<0) or (loc.y<0) or (loc.x>=self.width) or (loc.y>=self.height): return False
		return True
	def get(self,mapLocation):
		if not self.onMap(mapLocation):return -1
		return self.arr[mapLocation.x][mapLocation.y]
	def set(self,mapLocation,val):
		self.arr[mapLocation.x][mapLocation.y]=val
	def printout(self):
		print('printing map:')
		for y in range(self.height):
			buildstr=''
			for x in range(self.width):
				buildstr+=format(self.arr[x][self.height-1-y],'2d')
			print(buildstr)
	def addDisk(self,mapLocation,r2,val):
		locs = gc.all_locations_within(mapLocation,r2)
		for loc in locs:
			if self.onMap(loc):
				self.set(loc,self.get(loc)+val)
	def multiply(self,mmap2):
		for x in range(self.width):
			for y in range(self.height):
				ml = bc.MapLocation(bc.Planet.Earth,x,y);
				self.set(ml,self.get(ml)*mmap2.get(ml))
	def findBest(self,mapLocation,r2):
		locs = gc.all_locations_within(mapLocation,r2)
		bestAmt = 0
		bestLoc = None
		for loc in locs:
			amt = self.get(loc)
			if amt>bestAmt:
				bestAmt=amt
				bestLoc=loc
		return bestAmt, bestLoc

from collections import deque

#pathfinding on earth. Uses BFS 
def makePathEarthSmall(enemyLoc, maxIterations):
	counter = 0
	beenVisited = mmap(earthMap.width, earthMap.height);
	start = enemyLoc
	path = [[start for j in range(passableMap.height)] for i in range(passableMap.width)]
	queue = deque()
	queue.append(start)
	while queue and counter < maxIterations:
		counter += 1
		current = queue.popleft()
		if beenVisited.get(current) == 1:
			continue
		beenVisited.set(current, 1)

		for d in directions:
			temp = current.add(d)
			if passableMap.get(temp) == 1 and beenVisited.get(temp) == 0 and path[temp.x][temp.y].distance_squared_to(start) == 0:
				queue.append(temp)
				path[temp.x][temp.y] = current
	return path

def makePathEarth(enemyLoc):
	return makePathEarthSmall(enemyLoc, 9999)

#set up starting variables
if gc.planet() == bc.Planet.Earth:
	earthMap = gc.starting_map(bc.Planet.Earth)
	marsMap = gc.starting_map(bc.Planet.Mars)
	oneLoc = gc.my_units()[0].location.map_location() #location of my team units
	enemyLoc = invert(oneLoc);							#location of enemy units
	print('worker starts at '+locToStr(oneLoc))
	print('enemy worker presumably at '+locToStr(enemyLoc))
	rangerComp = False										#set default team composition to knights
	numImpassable = 0										#counts terrain tiles
	numTotal = earthMap.width * earthMap.height
	for x in range(earthMap.width):
		for y in range(earthMap.height):
			curr = bc.MapLocation(bc.Planet.Earth, x, y)
			if (not earthMap.is_passable_terrain_at(curr)):
				numImpassable += 1
	percentImpassable = numImpassable / numTotal * 100		#given a certain percentage of terrain, change
	if percentImpassable >= 33:								#composition to rangers
		rangerComp = True
	
	if not rangerComp:
		# let's start off with some research!
		# we can queue as much as we want.
		gc.queue_research(bc.UnitType.Knight) #25
		gc.queue_research(bc.UnitType.Knight) #100
		gc.queue_research(bc.UnitType.Knight) #200
		gc.queue_research(bc.UnitType.Healer) #225
		gc.queue_research(bc.UnitType.Rocket) #275
		gc.queue_research(bc.UnitType.Healer) #375
		gc.queue_research(bc.UnitType.Rocket) #475
		gc.queue_research(bc.UnitType.Rocket) #575
		gc.queue_research(bc.UnitType.Ranger) #600
		gc.queue_research(bc.UnitType.Ranger) #700
		gc.queue_research(bc.UnitType.Worker) #725
	
	#research for ranger comp
	else:
		gc.queue_research(bc.UnitType.Ranger) #25
		gc.queue_research(bc.UnitType.Healer) #50
		gc.queue_research(bc.UnitType.Healer) #150
		gc.queue_research(bc.UnitType.Knight) #175
		gc.queue_research(bc.UnitType.Knight) #250
		gc.queue_research(bc.UnitType.Rocket) #300
		gc.queue_research(bc.UnitType.Knight) #400
		gc.queue_research(bc.UnitType.Healer) #500
		gc.queue_research(bc.UnitType.Ranger) #600
		gc.queue_research(bc.UnitType.Rocket) #700
		gc.queue_research(bc.UnitType.Worker) #725)

			

	#guess enemy starting locations
	passableMap = mmap(earthMap.width,earthMap.height);
	kMap = mmap(earthMap.width,earthMap.height);
	for x in range(earthMap.width):
		for y in range(earthMap.height):
			ml = bc.MapLocation(bc.Planet.Earth,x,y);
			passableMap.set(ml,earthMap.is_passable_terrain_at(ml))
			kMap.set(ml,earthMap.initial_karbonite_at(ml))

	path = makePathEarth(enemyLoc)
	pathTarget = enemyLoc
	for x in range(earthMap.width):
		for y in range(earthMap.height):
			ml = bc.MapLocation(bc.Planet.Earth,x,y);
			if path[x][y].distance_squared_to(pathTarget) == 0:
				kMap.set(ml, 0)
	karbDest = oneLoc #used during karb pathfinding

#same as above but for Mars
if gc.planet() == bc.Planet.Mars:
	earthMap = gc.starting_map(bc.Planet.Earth)
	marsMap = gc.starting_map(bc.Planet.Mars)
	oneLoc = chooseLandingLocation()
	enemyLoc = bc.MapLocation(bc.Planet.Mars, marsMap.width // 2, marsMap.height // 2)
	if not marsMap.is_passable_terrain_at(enemyLoc):
		enemyLoc = chooseLandingLocation()

	passableMap = mmap(marsMap.width,marsMap.height);
	kMap = mmap(marsMap.width,marsMap.height);
	for x in range(marsMap.width):
		for y in range(marsMap.height):
			ml = bc.MapLocation(bc.Planet.Mars,x,y);
			passableMap.set(ml,marsMap.is_passable_terrain_at(ml))
			kMap.set(ml,marsMap.initial_karbonite_at(ml))
	beenVisited = mmap(marsMap.width, marsMap.height);
	start = enemyLoc
	goal = oneLoc
	#finds path to enemy location
	path = [[start for j in range(passableMap.height)] for i in range(passableMap.width)]
	queue = deque()
	queue.append(start)
	while queue:
		current = queue.popleft()
		if current == goal:
			print("path found")
		if beenVisited.get(current) == 1:
			continue
		beenVisited.set(current, 1)

		for d in directions:
			temp = current.add(d)
			if passableMap.get(temp) == 1 and beenVisited.get(temp) == 0 and path[temp.x][temp.y].distance_squared_to(start) == 0:
				queue.append(temp)
				path[temp.x][temp.y] = current
	print("pathing complete")

def rotate(dir, amount):
	ind = directions.index(dir)
	return directions[(ind+amount)%8]

def goto(unit, dest):
	d = unit.location.map_location().direction_to(dest)
	if gc.can_move(unit.id, d):
		gc.move_robot(unit.id, d)

def fuzzygoto(unit, dest):
	toward = unit.location.map_location().direction_to(dest)
	for tilt in tryRotate:
		d = rotate(toward, tilt)
		if gc.is_move_ready(unit.id) and gc.can_move(unit.id, d):
			gc.move_robot(unit.id, d)
			return True
	return False

def existsDirectPath(start, dest):
	toward = start.add(start.direction_to(dest))
	if toward.distance_squared_to(dest) == 0:
		return True
	currMap = earthMap
	if dest.planet == bc.Planet.Mars:
		currMap = marsMap
	if not currMap.is_passable_terrain_at(toward):
		return False
	return existsDirectPath(toward, dest)

def closestUnitIndex(location, nearby):
	minimum = 9999
	minimumIndex = 0
	currIndex = 0
	for other in nearby:
		current = location.distance_squared_to(other.location.map_location())
		if current < minimum:
			minimum = current
			minimumIndex = currIndex
		currIndex += 1
	return minimumIndex

def closestLocationIndex(location, map_locations):
	minimum = 9999
	minimumIndex = 0
	currIndex = 0
	for map_location in map_locations:
		current = location.distance_squared_to(map_location)
		if current < minimum:
			minimum = current
			minimumIndex = currIndex
		currIndex += 1
	return minimumIndex

def onEarth(loc):
	if (loc.x<0) or (loc.y<0) or (loc.x>=earthMap.width) or (loc.y>=earthMap.height): return False
	return True

def onMars(loc):
	if (loc.x<0) or (loc.y<0) or (loc.x>=marsMap.width) or (loc.y>=marsMap.height): return False
	return True

def checkK(loc):
	if not onEarth(loc):
		return 0
	return gc.karbonite_at(loc)

def checkKMars(loc):
	if not onMars(loc):
		return 0
	return gc.karbonite_at(loc)

def bestKarboniteDirectionMars(loc):
	mostK = 0
	bestDir = None
	for dir in directions:
		newK = checkKMars(loc.add(dir))
		if newK>mostK:
			mostK=newK
			bestDir=dir
	return mostK, bestDir

def bestKarboniteDirection(loc):
	mostK = 0
	bestDir = None
	for dir in directions:
		newK = checkK(loc.add(dir))
		if newK>mostK:
			mostK=newK
			bestDir=dir
	return mostK, bestDir


rocketLocs = []

#given a round, we either keep attacking
#or we try to go to mars
def determineAggressiveness():
	if gc.planet() == bc.Planet.Mars:
		return True
	if numOffensiveUnits > 75:
		return False
	if gc.round() > 390:
		return False
	return True

def factoryRatios():
	knights = 0
	rangers = 0
	healers = 0
	if percentImpassable > 33:
		rangers += 10
	return knights, rangers, healers

pathHome = []
pathHomeMade = False
while True:

	try:
		print(gc.get_time_left_ms())
		#unitCount
		numWorkers = 0
		numFactories = 0
		numRockets = 0
		numKnights = 0
		numRangers = 0
		numHealers = 0
		blueprintLocation = None
		blueprintWaiting = False
		for unit in gc.my_units():
			if unit.location.is_on_planet(gc.planet()):
				if unit.unit_type == bc.UnitType.Factory:
					if not unit.structure_is_built():
						ml = unit.location.map_location()
						blueprintLocation = ml
						blueprintWaiting = True
					numFactories += 1
				elif unit.unit_type == bc.UnitType.Worker and unit.location.is_on_map():
					numWorkers += 1
				elif unit.unit_type == bc.UnitType.Rocket:
					numRockets += 1
				elif unit.unit_type  == bc.UnitType.Knight:# and unit.location.is_on_map():
					numKnights += 1
				elif unit.unit_type == bc.UnitType.Ranger: #and unit.location.is_on_map():
					numRangers += 1
				elif unit.unit_type == bc.UnitType.Healer: #and unit.location.is_on_map():
					numHealers += 1
		numOffensiveUnits = numKnights + numRangers

		enemyLocChangedThisTurn = False
		pathChangedThisTurn = False

		#makes path if aggressive
		beAggressive = determineAggressiveness()
		if not beAggressive and not pathHomeMade:
			pathHome = makePathEarth(oneLoc)
			pathHomeMade = True
		#print(gc.round())
		#print(beAggressive)
		
		#for workers, checks if action has been made
		#if not look for nearby karbonite and move towards it
		for unit in gc.my_units():
			if not enemyLocChangedThisTurn and unit.location.is_on_map():
				nearbyWithWorkers = gc.sense_nearby_units_by_team(unit.location.map_location(), 50, other_team)
				nearby = []
				for near in nearbyWithWorkers:
					if near.unit_type != bc.UnitType.Worker:
						nearby.append(near)
				"""
				if not nearby:
					nearby = nearbyWithWorkers
				"""
				if (nearby):
					enemyLoc = nearby[0].location.map_location()
					enemyLocChangedThisTurn = True

					pathingTurns = 2
					if gc.get_time_left_ms() < 5000:
						pathingTurns = 4
					if not pathChangedThisTurn and gc.round() % pathingTurns == 0:
						newPathTarget = enemyLoc
						distance = newPathTarget.distance_squared_to(pathTarget)
						if distance > 50:
							path = makePathEarth(enemyLoc)
						else:
							path = makePathEarthSmall(enemyLoc, 50)
						pathChangedThisTurn = True

			#specific Worker code for replication and going to karb deposits
			if unit.unit_type == bc.UnitType.Worker and unit.location.is_on_map():
				if gc.round() < 35:
					nearby = gc.all_locations_within(unit.location.map_location(), unit.vision_range)
					nearbyKarbCount = 0
					for tile in nearby:
						if not path[tile.x][tile.y].distance_squared_to(pathTarget) == 0:
							nearbyKarbCount += gc.karbonite_at(tile)
					if nearbyKarbCount / len(gc.sense_nearby_units_by_type(unit.location.map_location(), unit.vision_range, bc.UnitType.Worker)) > 65:
						for d in directions:
							if gc.can_replicate(unit.id, d):
								gc.replicate(unit.id, d)
								break
				if gc.round() > 750:
					for d in directions:
						if gc.can_replicate(unit.id, d):
							gc.replicate(unit.id, d)
							break
				if numWorkers < 4:
					for d in directions:
						if gc.can_replicate(unit.id, d):
							gc.replicate(unit.id, d)
							break
				
				#building factories
				adjacentUnits = gc.sense_nearby_units(unit.location.map_location(), 2)
				for adjacent in adjacentUnits: #build
					if gc.can_build(unit.id, adjacent.id):
						gc.build(unit.id, adjacent.id)
						break
				
				#moving towards factories
				if beAggressive and unit.location.is_on_planet(bc.Planet.Earth):
					nearbyFactories = gc.sense_nearby_units_by_type(unit.location.map_location(), unit.vision_range, bc.UnitType.Factory)
					#moves towards unfinished factories
					if nearbyFactories:
						for factory in nearbyFactories:
							if not factory.structure_is_built() and factory.team == my_team:
								fuzzygoto(unit, factory.location.map_location())

					nearbyRockets = gc.sense_nearby_units_by_type(unit.location.map_location(), unit.vision_range, bc.UnitType.Rocket)
					#moves towards unfinished rockets
					if nearbyRockets:
						for rocket in nearbyRockets:
							if not rocket.structure_is_built() and rocket.team == my_team:
								if fuzzygoto(unit, rocket.location.map_location()):
									print("")
									#print("gimme factory")

					#conditions that signal to build factories
					if numFactories < 3 or gc.karbonite() > 300 :
						for d in directions:
							if gc.can_blueprint(unit.id, bc.UnitType.Factory, d):
								gc.blueprint(unit.id, bc.UnitType.Factory, d)
								oneLoc = unit.location.map_location()

					elif gc.karbonite() > bc.UnitType.Rocket.blueprint_cost():
						for d in directions:
							if gc.can_blueprint(unit.id, bc.UnitType.Rocket, d):
								gc.blueprint(unit.id, bc.UnitType.Rocket, d)
				
				#if not aggressive prioritize factories and takeoff
				elif not beAggressive:
					rockets = gc.sense_nearby_units_by_type(unit.location.map_location(), unit.vision_range, bc.UnitType.Rocket)
					unfinishedRockets = []
					nearbyBlueprint = False
					for rocket in rockets:
						if not rocket.structure_is_built():
							nearbyBlueprint = True
							unfinishedRockets.append(rocket)
					if nearbyBlueprint:
						fuzzygoto(unit, unfinishedRockets[closestUnitIndex(unit.location.map_location(), unfinishedRockets)].location.map_location())

					if not unit.worker_has_acted():
						if gc.round() > 500:
							if rockets:
								if gc.can_load(rockets[closestUnitIndex(unit.location.map_location(), rockets)].id, unit.id):
									gc.load(rockets[closestUnitIndex(unit.location.map_location(), rockets)].id, unit.id)
						for d in directions:
							if gc.can_blueprint(unit.id, bc.UnitType.Rocket, d):
								gc.blueprint(unit.id, bc.UnitType.Rocket, d)

				#determines best places to mine
				#checks if unit is ready and moves and acts if possible
				mostK, bestDir = bestKarboniteDirection(unit.location.map_location())
				if mostK > 0:
					if gc.can_harvest(unit.id, bestDir):
						gc.harvest(unit.id, bestDir)
						ml = unit.location.map_location().add(bestDir)
						kMap.set(ml, gc.karbonite_at(ml))
				if gc.is_move_ready(unit.id):
					resources = gc.all_locations_within(unit.location.map_location(), 50)
					karb_loc = []
					for location in resources:
						if gc.karbonite_at(location) != 0:
							karb_loc.append(location)
					if karb_loc:
						closest_karb_loc = karb_loc[closestLocationIndex(unit.location.map_location(), karb_loc)]
						fuzzygoto(unit, closest_karb_loc)
					else:
						if gc.planet() == bc.Planet.Earth:
							nearby = gc.all_locations_within(unit.location.map_location(), unit.vision_range)
							for tile in nearby:
								kMap.set(tile, gc.karbonite_at(tile))
							if kMap.get(karbDest) == 0: #generate new karb path
								karbLocs = []
								for x in range(earthMap.width):
									for y in range(earthMap.height):
										ml = bc.MapLocation(bc.Planet.Earth, x, y)
										if kMap.get(ml) > 0:
											karbLocs.append(ml)
								if karbLocs:
									karbDest = karbLocs[closestLocationIndex(unit.location.map_location(), karbLocs)]
									karbPath = makePathEarth(karbDest)
							fuzzygoto(unit, karbPath[unit.location.map_location().x][unit.location.map_location().y])

			#code for Factory
			#sets ratio of team composition and makes accordingly
			if unit.unit_type == bc.UnitType.Factory:
				garrison = unit.structure_garrison()
				if len(garrison) > 0: #ungarrison()
					for d in directions:
						if gc.can_unload(unit.id, d):
							gc.unload(unit.id, d)
							continue
				if gc.can_produce_robot(unit.id, bc.UnitType.Worker) and numWorkers == 0:
					gc.produce_robot(unit.id, bc.UnitType.Worker)
					numWorkers += 1
				if not rangerComp and gc.round() < 390 and numKnights < 75:
					if gc.can_produce_robot(unit.id, bc.UnitType.Healer) and numKnights > 4 and (numHealers < numKnights / 3) and gc.round() > 100:
						gc.produce_robot(unit.id, bc.UnitType.Healer)
						numHealers += 1
					elif gc.can_produce_robot(unit.id, bc.UnitType.Ranger) and numKnights > 4 and (numRangers < numKnights / 3):
						gc.produce_robot(unit.id, bc.UnitType.Ranger)
						numRangers += 1

					elif gc.can_produce_robot(unit.id, bc.UnitType.Knight): #produce Knights
						gc.produce_robot(unit.id, bc.UnitType.Knight)
						numKnights += 1
				elif rangerComp and gc.round() < 390 and numRangers < 75:
					if gc.can_produce_robot(unit.id, bc.UnitType.Healer) and (numHealers < numRangers / 3):
						gc.produce_robot(unit.id, bc.UnitType.Healer)
						numHealers += 1
					elif gc.can_produce_robot(unit.id, bc.UnitType.Knight) and (numKnights < numRangers / 3): #produce Knights
						gc.produce_robot(unit.id, bc.UnitType.Knight)
						numKnights += 1
					
					elif gc.can_produce_robot(unit.id, bc.UnitType.Ranger):
						gc.produce_robot(unit.id, bc.UnitType.Ranger)
						numRangers += 1
				else:
					continue

			#Rocket Code
			if unit.unit_type == bc.UnitType.Rocket: # and gc.round() % 25 == 0:
				land_loc = chooseLandingLocation()
				nearby_allies = gc.sense_nearby_units_by_team(unit.location.map_location(), unit.vision_range, my_team)
				existsAlly = False
				for ally in nearby_allies:
					if ally.unit_type != bc.UnitType.Rocket:
						existsAlly = True
						continue
				nearby_enemies = gc.sense_nearby_units_by_team(unit.location.map_location(), 25, other_team)
				if gc.can_launch_rocket(unit.id, land_loc) and (len(unit.structure_garrison()) == unit.structure_max_capacity() or not existsAlly or nearby_enemies or gc.round() > 739):
					#rocketLocs.remove(unit.location.map_location())
					gc.launch_rocket(unit.id, land_loc)
					print("launched rocket")
			
			#Knight code
			if unit.unit_type == bc.UnitType.Knight:
				#moving
				if unit.location.is_on_map(): #can't move from inside a factory
					location = unit.location
					if gc.is_move_ready(unit.id):
						if beAggressive:
							nearby = gc.sense_nearby_units_by_team(location.map_location(), unit.vision_range, other_team)
							hasMoved = False

							if nearby:
								for near in nearby:
									if existsDirectPath(unit.location.map_location(), near.location.map_location()):
										fuzzygoto(unit, near.location.map_location())
										break

							if numKnights > 3 and not hasMoved:
								fuzzygoto(unit, path[location.map_location().x][location.map_location().y])
							if not hasMoved:
								fuzzygoto(unit, oneLoc)
						else:
							#if (rocketLocs):
							#closestRocketLoc = rocketLocs[closestLocationIndex(location.map_location(), rocketLocs)]
							nearby = gc.sense_nearby_units_by_type(location.map_location(), 50, bc.UnitType.Rocket)
							if nearby and gc.planet() == bc.Planet.Earth:
								if (gc.can_load(nearby[0].id, unit.id)):
									#print("loaded knight")
									gc.load(nearby[0].id, unit.id)
								else:
									#if nearby[0].structure_is_built():
									fuzzygoto(unit, nearby[0].location.map_location())
							else:
								if pathHomeMade:
									fuzzygoto(unit, pathHome[location.map_location().x][location.map_location().y])


					if gc.is_javelin_ready(unit.id):
						nearby_targets = gc.sense_nearby_units_by_team(location.map_location(), unit.ability_range(), other_team)
						for other in nearby_targets:
							try:
								if gc.can_javelin(unit.id, other.id):
									print("javelined")
									gc.javelin(unit.id, other.id)
									break
							except Exception as e:
								#do nothing
								print("")

					nearby = gc.sense_nearby_units(location.map_location(), unit.attack_range())
					for other in nearby:
						if other.team != my_team and gc.is_attack_ready(unit.id) and gc.can_attack(unit.id, other.id):
							gc.attack(unit.id, other.id)
							continue
			#healer code
			if unit.unit_type == bc.UnitType.Healer:
				if not unit.location.is_in_garrison():
					allies = gc.sense_nearby_units_by_team(unit.location.map_location(),unit.attack_range(),my_team)
					if beAggressive:
						if len(allies) > 0:
							#hasHealed = False
							for ally in allies:
								#heals anything in range and damaged and not a worker
								if gc.is_heal_ready(unit.id) and gc.can_heal(unit.id, ally.id) and ally.health < ally.max_health and ally.unit_type != bc.UnitType.Worker: #TODO targetting
									gc.heal(unit.id, ally.id)
									#hasHealed = True
									continue
						if gc.is_move_ready(unit.id):
							#nearbyEnemies = gc.sense_nearby_units_by_team(unit.location.map_location(),unit.vision_range,enemy_team)
							#if len(nearbyEnemies) == 0:
							nearbyEnemies = gc.sense_nearby_units_by_team(unit.location.map_location(), unit.attack_range(), other_team)
							fuzzygoto(unit, path[unit.location.map_location().x][unit.location.map_location().y])
					else:
						allies = gc.sense_nearby_units_by_team(unit.location.map_location(),unit.attack_range(),my_team)
						if len(allies) > 0:
							#hasHealed = False
							for ally in allies:
								if gc.is_heal_ready(unit.id) and gc.can_heal(unit.id, ally.id) and ally.health < ally.max_health and ally.unit_type != bc.UnitType.Worker: #TODO targetting
									gc.heal(unit.id, ally.id)

						nearby = gc.sense_nearby_units_by_type(unit.location.map_location(), 50, bc.UnitType.Rocket)
						if nearby and gc.planet() == bc.Planet.Earth:
							if (gc.can_load(nearby[0].id, unit.id)):
								#print("loaded healer")
								gc.load(nearby[0].id, unit.id)
							else:
								if nearby[closestUnitIndex(unit.location.map_location(), nearby)].structure_is_built():
									fuzzygoto(unit, nearby[closestUnitIndex(unit.location.map_location(), nearby)].location.map_location())
									print("healer to rocket")
						else:
							if gc.is_move_ready(unit.id) and pathHomeMade:
								fuzzygoto(unit, pathHome[unit.location.map_location().x][unit.location.map_location().y])
								#fuzzygoto(unit, path[unit.location.map_location().x][unit.location.map_location().y])
			#Ranger code
			if unit.unit_type == bc.UnitType.Ranger:
				if not unit.location.is_in_garrison():#can't move from inside a factory
					attackableEnemies = gc.sense_nearby_units_by_team(unit.location.map_location(),unit.attack_range(),other_team)
					if (gc.round() < 390 and numKnights < 75 and unit.location.is_on_planet(bc.Planet.Earth)) or unit.location.is_on_planet(bc.Planet.Mars):
						if len(attackableEnemies) > 0:
							for attackable in attackableEnemies:
								if gc.is_attack_ready(unit.id) and gc.can_attack(unit.id, attackable.id): #TODO targetting
									gc.attack(unit.id, attackable.id)
									continue
						elif gc.is_move_ready(unit.id) and ((gc.round() < 390 and numKnights < 75 and unit.location.is_on_planet(bc.Planet.Earth)) or unit.location.is_on_planet(bc.Planet.Mars)):
							#nearbyEnemies = gc.sense_nearby_units_by_team(unit.location.map_location(),unit.vision_range,enemy_team)
							#if len(nearbyEnemies) == 0:
							nearbyEnemies = gc.sense_nearby_units_by_team(unit.location.map_location(), unit.attack_range(), other_team)
							fuzzygoto(unit, path[unit.location.map_location().x][unit.location.map_location().y])
					else:
						attackableEnemies = gc.sense_nearby_units_by_team(unit.location.map_location(),unit.attack_range(),other_team)
						if len(attackableEnemies) > 0:
							for attackable in attackableEnemies:
								if gc.is_attack_ready(unit.id) and gc.can_attack(unit.id, attackable.id): #TODO targetting
									gc.attack(unit.id, attackable.id)

						nearby = gc.sense_nearby_units_by_type(unit.location.map_location(), 50, bc.UnitType.Rocket)
						if nearby and gc.planet() == bc.Planet.Earth:
							if (gc.can_load(nearby[0].id, unit.id)):
								#print("loaded ranger")
								gc.load(nearby[0].id, unit.id)
							else:
								if nearby[0].structure_is_built():
									fuzzygoto(unit, nearby[0].location.map_location())
						else:

							if gc.is_move_ready(unit.id) and pathHomeMade:
								fuzzygoto(unit, pathHome[unit.location.map_location().x][unit.location.map_location().y])
								#fuzzygoto(unit, path[unit.location.map_location().x][unit.location.map_location().y])

			if unit.unit_type == bc.UnitType.Rocket and gc.planet() == bc.Planet.Mars:
				for d in directions:
					if gc.can_unload(unit.id, d):
						gc.unload(unit.id, d)


	except Exception as e:
		print('Error:', e)
		# use this to show where the error was
		traceback.print_exc()

	# send the actions we've performed, and wait for our next turn.
	gc.next_turn()

	# these lines are not strictly necessary, but it helps make the logs make more sense.
	# it forces everything we've written this turn to be written to the manager.
	sys.stdout.flush()
	sys.stderr.flush()
