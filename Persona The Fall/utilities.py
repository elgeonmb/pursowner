import pygame
from pygame.locals import *

def goodload(thing):
    '''Because the default load function is long and I'm lazy'''
    return pygame.image.load("images/" + thing).convert()
	
def makesound(thing):
	'''It's like goodload, but for sound.'''
	return pygame.mixer.Sound("sounds/" + thing)

def makemusic(thing):
	'''I love snowflake code.'''
	return pygame.mixer.Sound("music/" + thing)
    
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