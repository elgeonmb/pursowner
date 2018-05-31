import enginelite
import random
from collections import deque

class Passer:
	def __init__(self):
		self.allies = [enginelite.protag, enginelite.miyu, enginelite.long]
		self.enemies = [enginelite.jackfrost, enginelite.min, enginelite.default]
		self.list = self.allies + self.enemies # DO NOT modify any of the passer lists-- not stable
		self.isambush = 0 #-1 for enemy first attacks, 1 for ally firstattacks
		self.items = [enginelite.molotov, enginelite.katana]
		
passer = Passer()

friends = passer.allies
foes = passer.enemies
mallies = passer.allies #mutable
menemies = passer.enemies #mutable
mlist = mallies + menemies
queue = deque()
ambushq = deque()

queue.extend(passer.list)
queue = deque(sorted(queue, key=lambda char: char.persona.agi))

#if it's an ambush, fill the ambush queue
if passer.isambush == 1:
	ambushq.extend(sorted(passer.allies, key=lambda char: char.persona.agi))
elif passer.isambush == -1:
	ambushq.extend(sorted(passer.enemies, key=lambda char: char.persona.agi))
	
active = None
actions = ["Attack", "Skill", "Guard", "Item", "Gun", "Tactics", "Analyze", "Persona"]
onemore = False

#still todo: loops??

def turn():
	global active
	if ambushq:
		active = ambushq.pop()
		#ambushq exhausts itself
	else:
		active = queue.pop()
		queue.appendleft(active)
		#active's next turn comes when everyone else is done
	active.guarding = False
	if active.swapped == True:
		active.swapped == False
	active.ailtimer = max(0, active.ailtimer - 1)
	active.tarutimer = max(0, active.tarutimer - 1)
	active.rakutimer = max(0, active.rakutimer - 1)
	active.sukutimer = max(0, active.sukutimer - 1)
	pulse()
		
def pulse():
	"""Called every time a new pulse is initiated.
	Reminds us of what's going on.
	Will be more relevant in full release.
	Already very important
	Handles people dying when they're killed
	"""
	whodied = []
	if active.ailment == "Burn":
		active.damage(active.hpmax * .05)
	for victim in queue:
		if victim.hp <= 0:
			victim.ailment = "Dead"
			print(victim.name, "died!")
			whodied.append(victim)
		for dead in whodied:
			for a in [passer.allies, passer.enemies, queue, ambushq]:
				if dead in a:
					a.remove(dead)
		if active in passer.allies:
			foes = passer.enemies
			friends = passer.allies
		else:
			foes = allies
			friends = enemies
		if len(foes) == 0:
			print("You win!")
			#todo: save
			quit()
		print("Enemies:", stringify(names(foes)))
		print("Active:", active.name)
		#TODO: have it check for different AI methods
		#TODO: brainwash and fear and despair and whatnot are probably formally AI functions
		if active.ailment == "Freeze":
			print(active.name, "is frozen!")
			turn()
		elif active.ailment == "Shock":
			print(active.name, "is shocked!")
			turn()
		elif active.ailment == "Sleep":
			print(active.name, "is sleeping!")
			active.hp + .1 * active.hpmax
			active.sp + .1 * active.spmax
			turn()
		pcommand()
		
def pcommand(mode = "Free", action=None):
	"""The base command function.
	Action, if set, is a deque of strings that will be fed to the choice-making machinery because I'm a fucking idiot tbh 
	"""
	#TODO: restructure so we can re-enter the loop at any subloop
	#Potential implementation of action: have input take an arg that if non-null substitutes for picking, much like pcommand(mode=) but less fucking stupid
	#WON'T WORK, Select and Target are two seperate functions. Have them share a queue I guess? It's also a lot harder to fetch strings for this arg than I anticipated
	#genuinely easier just to have two versions of all relevant procs tbfh
	print(stringify(actions))
	if mode == "Free":
		choice = input(">")
		choice = choice.title()
	else:
		choice = mode
	if choice == "Attack":
		select(active.attack) 
	elif choice == "Skill":
		if active.ailment == "Forget":
			print("You can't remember how to do that!")
			pcommand()
		print("Choose a skill!")
		for x in active.persona.skills:
			print(x.name, x.cost, x.costtype)
		choice = input(">")
		if choice.title() in names(active.persona.skills):
			using = unname(choice.title(), active.persona.skills)
			if using.costtype == "HP":
				if active.hp < using.cost + 1:
					print("Not enough HP!")
					pcommand(mode = "Skill")
			elif using.costtype == "SP":
				if active.sp < using.cost:
					print("Not enough SP!")
					pcommand(mode = "Skill")
			select(unname(choice.title(), active.persona.skills))
		else:
			print("Invalid choice")
			pcommand()
	elif choice == "Guard":
		if confirm():
			active.guarding = True
			print("Guarding.")
			turn()
		else:
			pcommand()
	elif choice == "Item":
		#TODO: clean those unname statements
		#TODO: move itemcount deincrimenting somewhere else so items are only consumed if we actually decide to use them
		#TODO: there's a bug somewhere here with invalid item names. IDK how to handle it.
		print("Items:")
		for y in passer.items:
			if y.count > 0:
				print(y.name, "x" + str(y.count))
		print("Select an item:")
		choice = input(">")
		choice = choice.title()
		try:
			if unname(choice, passer.items).count == 0:
				print("Out of", choice + "!")
				pcommand(mode = "Item")
			else:
				unname(choice, passer.items).count -= 1
				select(unname(choice, passer.items).move)
		except AssertionError:
			print("No such item!")
			pcommand()
	elif choice == "Gun":
		pass
	elif choice == "Tactics":
		print("This will be useful in the future!")
		turn()
	elif choice == "Analyze":
		target = targ(foes)
		analyze(target)
		pcommand()
	elif choice == "Persona":
		if isinstance(active, enginelite.Wildcard) and not active.swapped:
			print("Chose a Persona.")
			print(stringify(names(active.plist)))
			choice = input(">")
			choice = choice.title()
			if choice in names(active.plist):
				active.persona = unname(choice, active.plist)
				active.swapped = True
				pcommand()
			else:
				print("No such Persona.")
				pcommand()
		else:
			if isinstance(active, enginelite.Wildcard):
				print("You have already changed Personas this turn!")
				pcommand()
			else:
				print("You are not a Wild Card!")
				pcommand()		
	else:
		print("Please print a valid action.")
		pcommand()
		
def confuse():
	heali = []
	if random.random < .5:
		print(active.name, "is confused!")
		turn()
	elif random.random < .5:
		print(active.name, "threw away money!")
		#todo: money
		turn()
	for x in passer.items:
		if x.move.element == "Recovery":
			heali.append(x)
				
def fear():
	if random.random < .8:
		print(active.name, "is paralyzed with fear!")
		turn()
	else:
		if random.random < .5 and not isinstance(active, enginelite.Wildcard):
			print(active.name, "runs away!")
			queue.remove(active)
			try:
				ambushq.remove(active)
			except ValueError:
				pass
			turn()
		else:
			pcommand()
				
def select(move):
	"""Handles target selection for skills."""
	#todo: restructure to allow returns
	if "Single" in move.flags:
		if "Them" in move.flags:
			target = targ(foes)
			attack(move, target)
		elif "Us" in move.flags:
			target = targ(friends)
			attack(move, target)
		elif "Any" in move.flags:
			target = targ(friends + foes)
			attack(move, target)
	elif "Double" in move.flags:
		if "Them" in move.flags:
			print("Targetting:", foes)
			if confirm():
				attack(move, foes)
			else:
				select(move)
		elif "Us" in move.flags:
			print("Targetting:", friends)
			if confirm():
				attack(move, friends)
			else:
				select(move)
		elif "Any" in move.flags:
			print("Targetting:", friends + foes)
			if confirm():
				attack(move, friends + foes)
			else:
				select(move)
					
def targ(candidates):
	"""Helper method that given a list will let the player pick one from the list and then return that member"""
	print("Choose a target.")
	print("Targets:", stringify(names(candidates)))
	while True:
		target = input(">")
		target = target.title()
		if target in names(candidates):
			return unname(target, candidates)
		else:
			print("Invalid target.")
			
def attack(move, targets):
	"""Handles using skills, including healing and buffs.
	Target can be either a character object or a list of character objects.
	Deals only with the mechanical effects of the move and not their impact on combat flow"""
	if type(targets) is not list:
		#hacky but hey it fucking works
		oldtargets = targets
		targets = []
		targets.append(oldtargets)
	for target in targets:
		for n in range(move.hits):
			if "Damage" in move.effects:
				if hitcheck(active, target, move):
					#first, do the damage shit
					#TODO: *karn checks
					if target.guarding :
						guardvalue = .8
					else:
						guardvalue = 1
					if move.element in target.persona.weak:
						print("Hit", target.name + "'s Weakness!")
						target.damage(damage(active, target, move) * 1.7 * guardvalue)
						if not target.guarding and not target.fallen:
							onemore = True
							target.fallen = True
						target.guarding = False
					elif move.element == "Wind" and target.ailment == "Burn":
						print("Technical on", target.name)
						target.damage(damage(active, target, move) * 1.7 * guardvalue)
						target.guarding = False
					elif move.element in ["Phys", "Gun"] and target.ailment in ["Shock", "Freeze"]:
						print("Technical on", target.name)
						target.damage(damage(active, target, move) * 1.7 * guardvalue)
						target.guarding = False
					elif move.element == "Nuke" and target.ailment in ["Burn", "Shock", "Freeze"]:
						print("Technical on", target.name)
						target.damage(damage(active, target, move) * 1.7 * guardvalue)
						target.guarding = False
					elif move.element == "Psi" and target.ailment in ["Forget", "Sleep", "Confuse", "Fear", "Despair", "Rage", "Brainwash"]:
						print("Technical on", target.name)
						target.damage(damage(active, target, move) * 1.7 * guardvalue)
						target.guarding = False
					elif move.element in target.persona.strong:
						print(target.name, "Resists!")
						target.damage(damage(active, target, move) * .4 * guardvalue)
						target.guarding = False
					elif move.element in target.persona.null:
						print(target.name, "Nulls!")
					elif move.element in target.persona.absorb:
						print(target.name, "Absorbed!")
						target.heal(damage(active, target, move)) 
					elif move.element in target.persona.repel:
						print(target.name, "Repelled!")#will break for reflected multi-hit moves (eg reflected hassou tobi hits 64 times)
						#TODO: make reflected area attacks hit non-protected enemies normally (fixing this will cause the above break, fix that too)
						attack(move, active)
					elif critcheck(active, target, move):
						print("Critical On", target.name + "!")
						target.damage(damage(active, target, move) * 1.7 * guardvalue)
						if not target.guarding:
							onemore = True	
						target.guarding = False
					else:
						print(target.name, "Hit!")
						target.damage(damage(active, target, move))
						target.guarding = False
				else:
					print("Missed" + target.name)
					# apply effects
					# a good way to do this: dictionary comprehensions
					# how I'm actually doing this: elif chains. Nested elif chains.
			if "Tarukaja" in move.effects:
				target.buffs["atk"] = min(target.buffs["atk"] + 1, 1)
				print(target.name, "attack up!")
				target.tarutimer = 3
			if "Rakukaja" in move.effects:
				target.buffs["def"] = min(target.buffs["def"] + 1, 1)
				print(target.name, "defense up!")
				target.rakutimer = 3
			if "Sukukaja" in move.effects:
				target.buffs["agi"] = min(target.buffs["agi"] + 1, 1)
				print(target.name, "agility up!")
				target.sukutimer = 3
			if "Tarunda" in move.effects:
				target.buffs["atk"] = max(target.buffs["atk"] - 1, -1)
				print(target.name, "attack down!")
				target.tarutimer = 3
			if "Rakunda" in move.effects:
				target.buffs["def"] = max(target.buffs["def"] - 1, -1)
				print(target.name, "defense down!")
				target.rakutimer = 3
			if "Sukunda" in move.effects:
				target.buffs["agi"] = max(target.buffs["agi"] - 1, -1)
				print(target.name, "agility down!")
				target.sukutimer = 3
			if "Dekunda" in move.effects:
				for x in target.buffs:
					if x < 0:
						x = 0
			if "Dekaja" in move.effects:
				for x in target.buffs:
					if x > 0:
						x = 0
			if "Deailment" in move.effects:
				if target.ailment in move.effects:
					target.ailment = "Healthy"
			if "Wall" in move.effects:
				for x in move.effects:
					if x in elements:
						if x in target.persona.weak:
							target.persona.wallo = ("Weak", x)
							target.persona.weak.remove(x)
							print(target.name + "'s", x, "resistance increased!")
							target.persona.walltimer = 3
						else:
							print("No effect!")
			if "Break" in move.effects:
				for x in move.effects:
					if x in elements:
						if x in target.persona.strong:
							target.persona.breko = ("Strong", x)
							target.persona.strong.remove(x)
							print(target.name + "'s", x, "resistance was removed!")
							target.persona.brektimer = 3
						elif x in target.persona.null:
							target.persona.breko = ("Null", x)
							target.persona.null.remove(x)
							print(target.name + "'s", x, "resistance was removed!")
							target.persona.brektimer = 3
						elif x in target.persona.absorb:
							target.persona.breko = ("Absorb", x)
							target.persona.absorb.remove(x)
							print(target.name + "'s", x, "resistance was removed!")
							target.persona.brektimer = 3
						elif x in target.persona.repel:
							target.persona.breko = ("Repel", x)
							target.persona.repel.remove(x)
							print(target.name + "'s", x, "resistance was removed!")
							target.persona.brektimer = 3
						else:
							print("No effect!")
			if "Tetrakarn" in move.effects:
				target.tetrakarn = True
			if "Makarakarn" in move.effects:
				target.makarakarn = True
			if "Ailment3" in move.effects:
				ailmod = 1
			elif "Ailment2" in move.effects:
				ailmod = .67
			elif "Ailment1" in move.effects:
				ailmod = .33
			else:
				continue #anything that goes beyond here should have an ailment flag
					#see how pretty this is? Why can't you do it like this
			if ailmod * (active.persona.luc / target.persona.luc) > random.random():
				for x in move.effects:
					if x in ailments:
						ailtimer = 3
						target.ailment = x
						print(target.name, x + "ed")
			else:
				print("Missed!")
	if move.costtype == "HP":
		active.hp -= move.cost
	elif move.costtype == "SP":
		active.sp -= move.cost
	elif move.costtype == "Item":
		for x in passer.items:
			if x.move == move:
				x.count -= 1
			#todo: error handling
	if onemore == True:
		onemore = False
		print("One more!")
		pulse()
	else:
		turn()
		
def stringify(thing):
	"""Takes a list and returns a human-readable comma-seperated string"""
	x = ''
	for n in range(len(thing)):
		x += thing[n]
		if n != len(thing)-1:
			x += ", "
	return str(x)
	
	
def names(notakeyword):
	"""Takes a list of objects with the name property and returns a list of their names.
	Not to be used for printing; define __repr__() instead
	"""
	x = []
	for n in range(len(notakeyword)):
		x.append(notakeyword[n].name)
	return x
	
	
def unname(name, sort):
	"""Takes a string and a list of objects with the name property and returns an object with the given name."""
	for x in range(len(sort)):
		if sort[x].name == name:
			return sort[x]
	raise AssertionError


def analyze(shadow):
	"""Prints analysis info for a given shadow"""
	print("Name:", shadow.name)
	print("Persona:", shadow.persona.name)
	print("Max HP:", shadow.hpmax)
	print("Max SP:", shadow.spmax)
	print("Buffs:", shadow.buffs)
	print("Weakness:", stringify(shadow.persona.weak))
	print("Resists:", stringify(shadow.persona.strong))
	print("Nulls:", stringify(shadow.persona.null))
	print("Absorbs:", stringify(shadow.persona.absorb))
	print("Reflects:", stringify(shadow.persona.repel))
	print("Arcana:", shadow.persona.arcana)
	
def confirm():
	print("Confirm? Y/N")
	response = input(">")
	if response.title() in ["Y", "Yes"]:
		return True
	else:
		return False


def hitcheck(actor, target, move):
	"""takes two characters and an attack and determines randomly if it hits"""
	if move.element in ["Recovery", "Ailment"]:
		return True
	if actor.buffs['agi'] == 2:
		hitmod = 1.3
	elif actor.buffs['agi'] == 0:
		hitmod = .7
	else:
		hitmod = 1
	if target.buffs['agi'] == 2:
		dodgemod = .7
	elif target.buffs['agi'] == 0:
		dodgemod = 1.3
	else:
		dodgemod = 1
	if actor.persona.agi / target.persona.agi * move.hitrate * hitmod * dodgemod > random.random(): #might be actor + (actor - target) / actor?
		return True
	else:
		return False


def critcheck(actor, target, move):
	"""checks for a crit (critrate should be 0 for non-physical moves)"""
	if actor.persona.luc / target.persona.luc * move.critrate > random.random():
		return True
	else:
		return False
		
def damage(actor, target, move):
	"""For some fucking reason this got totaled by a more foolish past me
	Probably still kinda janky
	please make it good
	"""
	levelmod = {-10:.33, -9:.35, -8:.4, -7:.43, -6:.5, -5:61, -4:.77, -3:.89, -2:.95, -1:0, 0:0, 1:0, 2:1.05, 3:1.12, 4:1.3, 5:1.62, 6:2, 7:2.3, 8:2.5, 9:2.8, 10:3}
	if actor.buffs['atk'] == 2:
		atkmod = 1.5
	elif actor.buffs ['atk'] == 0:
		atkmod = .5
	else:
		atkmod = 1
	if target.buffs['def'] == 2:
		defmod = .5 # inverse of the above for better maths
	elif target.buffs['def'] == 0:
		defmod = 1.5
	else:
		defmod = 1
	if actor.charge == "Body" and "Physical" in move.flags:
		atkmod *= 2
	elif actor.charge == "Mind" and "Magic" in move.flags:
		atkmod *=2
	if "Recovery" == move.element:
		#TODO: figure out this formula??????????????????????????????????????????
		pass
	elif "Magic" in move.flags:
		return int((5 * sqrt(actor.persona.mag/target.persona.end) * move.pwr * levelmod[min(-10, max(10, actor.level-target.level))] * atkmod * defmod * random.uniform(.95, 1.05))//1)
	elif "Physical" in move.flags:
		return int((5 * sqrt(actor.persona.str/target.persona.end) * move.pwr * levelmod[min(-10, max(10, actor.level-target.level))] * atkmod * defmod * random.uniform(.95, 1.05))//1)
		
turn()