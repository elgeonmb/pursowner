class Attack:
	def __init__(self, name, element, pwr, hits, flags, effects, hitrate, critrate, costtype, cost):
		self.name = name
		self.element = element
		assert self.element in ["Phys", "Gun", "Fire", "Ice", "Wind", "Elec", "Nuke", "Psi", "Light", "Dark", "Recovery", "Almighty", "Ailment"]
		self.pwr = pwr
		self.hits = hits
		self.flags = flags #a list of strings? need to maintain canonical list somewhere decent
		self.effects = effects
		self.hitrate = hitrate #float between 0 and 1
		self.critrate = critrate
		self.costtype = costtype
		self.cost = cost
		
	def __repr__(self):
		return self.name
		
agim = Attack("Agi", "Fire", 1, 1, ["Single", "Magic", "Attack", "Them"], ["Damage", "Ailment1", "Burn"], .9, 0, "SP", 1)
htobi = Attack("Hassou Tobi", "Phys", 1, 8, ["Double", "Physical", "Attack", "Them"], ["Damage"], .5, .1, "HP", 0) #hassou tobi shouldn't actually be in the final game please
molotov_a = Attack("Molotov Cocktail", "Fire", 1, 1, ["Single", "Magic", "Attack", "Them"], ["Damage", "Ailment1", "Burn"], .9, 0, "Item", 1)
		
class Item:
	def __init__(self, name, move, count=1):
		self.name = name
		self.move = move
		self.count = count
	
	def __repr__(self):
		return self.name
		
molotov = Item("Molotov Cocktail", molotov_a)	
katana = Item("Edgy Katana", htobi, 0)	
		
class Persona:
	def __init__(self, name="Error", skills=[], str=1, mag=1, end=1, agi=1, luc=1, weak=[], strong=[], null=[], absorb=[], repel=[], arcana="Fool"):
		self.name = name
		self.skills = [agim, htobi] #skills # TODO: strip out passive skills
		self.str = str
		self.mag = mag
		self.end = end
		self.agi = agi
		self.luc = luc
		self.weak = weak
		self.strong = strong
		self.null = null
		self.absorb = absorb
		self.repel = repel
		self.arcana = arcana
		
		self.walltimer = 0
		self.wallo = None # becomes a tuple ("Original resistance", "Element")
		self.brektimer = 0
		self.brektimer = None #becomes a tuple ("Original resistance", "Element")
	
	def __repr__(self):
		return self.name
		

prometheus = Persona("Prometheus", [], 1, 1, 1, 6, 1, [], [], [], [], ["Phys"], "Fool")
styx = Persona("Styx", [], 1, 1, 1, 1, 1, [], [], [], [], [],  "Priestess")
phoebe = Persona("Phoebe", [], 1, 1, 1, 1, 1, [], [], [], [], [],  "Hanged Man")
pallas = Persona("Pallas", [], 1, 1, 1, 1, 1, [], [], [], [], [],  "Emperor")

armor_jackfrost = Persona("Jack Frost", [], 1, 1, 1, 1, 1, repel=[], arcana="Magician")
armor_pixie = Persona("Pixie", [], 1, 1, 1, 1, 1, repel=[], arcana="High Priestess")
armor_default = Persona()

class Character:
	def __init__(self, name="Error", gender="Plural", hpmax=1, hp=1, spmax=1, sp=1, ammo=1, ammomax=1, weapon=1, level=1, persona=armor_default):
		self.name = name
		self.gender = gender
		self.hpmax = hpmax
		self.hp = hp
		self.spmax = spmax
		self.sp = sp
		self.ammomax = ammomax
		self.ammo = ammomax
		self.buffs = {"atk" : 1, "def" : 1, "agi" : 1} # 0 = debuffs, 1 = normal, 2 = buffed
		self.charge = None # can be "mind", "body", or None
		self.guarding = False
		self.ailment = "Healthy"
		self.weapon = weapon #int now, will change to a weapon item w/ a pwr attribute as an int
		self.level = level
#		self.gun = False #default gun here
#		self.access = ""
		self.attack = Attack("Attack", "Phys", self.weapon, 1, ["Single", "Physical", "Attack", "Them"], ["Damage"], .9, .05, "HP", 0) #high crit value good for testing, bad for actual gameplay
		self.persona = persona
		
		self.fallen = False
		
		self.ailtimer = 0
		self.tarutimer = 0
		self.rakutimer = 0
		self.sukutimer = 0
		self.tetrakarn = False
		self.makarakarn = False
		
	def __repr__(self):
		return self.name
		
	def heal(self, amount):
		amount = int(amount)
		print("Healed", self.name, amount, "HP.")
		self.hp = min(self.hpmax, self.hp + amount)
		
	def damage(self, amount):
		amount = int(amount)
		print(self.name, "took", amount, "damage.")
		self.hp = max(0, self.hp - amount)
		
class Wildcard(Character):
	def __init__(self, name="Error", gender="Plural", hpmax=1, hp=1, spmax=1, sp=1, ammo=1, ammomax=1, weapon=1, level=1, persona=armor_default, plist=[]):
		super().__init__(name, gender, hpmax, hp, spmax, sp, ammo, ammomax, weapon, level, persona)
		self.plist = plist
		self.swapped = False
		
		
protag = Wildcard("Protag Onist", "Plural", 1, 1, 1, 1, 1, 1, 1, 1, prometheus, plist=[armor_pixie, prometheus])
min = Character("Min Zhao", "Male", 1, 1, 1, 1, 1, 1, 1, 1, styx)
miyu = Character("Miyu Kirijou", "Female", 1, 1, 1, 1, 1, 1, 1, 1, phoebe)
long = Character("Irvin Long", "Male", 1, 1, 1, 1, 1, 1, 1, 1, pallas)

jackfrost = Character("Jack Frost", "Neuter", 1, 1, 1, 1, 1, 1, persona=armor_jackfrost)
default = Character()

def gender(string, gender):
	"""Takes a string to be formatted and a string representing a gender and formats a string accordingly"""
	if gender == "Male":
		pronouns = {"they" : "he", "them" : "him", "their" : "his", "theirs" : "his", "themselves" : "himself", "They" : "He", "Them" : "Him", "Their" : "His", "Theirs" : "His", "Themselves" : "Himself"}
	elif gender == "Female":
		pronouns = {"they" : "she", "them" : "her", "their" : "her", "theirs" : "hers", "themselves" : "herself", "They" : "She", "Them" : "Her", "Their" : "Her", "Theirs" : "Hers", "Themselves" : "Herself"}
	elif gender == "Plural":
		pronouns = {"they" : "they", "them" : "them", "their" : "their", "theirs" : "theirs", "themselves" : "themself", "They" : "They", "Them" : "Them", "Their" : "Their", "Theirs" : "Theirs", "Themselves" : "Themself"}
	elif gender == "Plural2": #for collectives; probably unused
		pronouns = {"they" : "they", "them" : "them", "their" : "their", "theirs" : "theirs", "themselves" : "themselves", "They" : "They", "Them" : "Them", "Their" : "Their", "Theirs" : "Theirs", "Themselves" : "Themselves"}
	else:
		pronouns = {"they" : "it", "them" : "it", "their" : "its", "theirs" : "its", "themselves" : "itself", "They" : "It", "Them" : "It", "Their" : "Its", "Theirs" : "Its", "Themselves" : "Itself"}
	try:
		return string.format(**pronouns)
	except:
		return string