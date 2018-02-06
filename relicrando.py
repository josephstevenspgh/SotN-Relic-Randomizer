#Lets Randomize Relics
#Made by setz

#@splixel on twitter
#twitch.tv/skiffain

#too lazy for licenses, pretend I attached WTFPL
#(do what the fuck you want with this)

#error_recalc comes from https://www.romhacking.net/utilities/1264/

#Conditions for flight are one of the following
	#Soul of Bat (ez mode)
	#Gravity Boots + Leap Stone (chaining gravity jumps)
	#Form of Mist + Power of Mist (fly as mist)

#Requirements for accessing castle 2 are
	#Flight
	#Jewel of Open
	#Mist

import random
from subprocess import call
from binascii import hexlify
from datetime import datetime


FileName = "Castlevania - Symphony of the Night (USA) (Track 1).bin"
#RandomizeBossRelics = False #Not Supported

ShowItemPlacements = True #Print out a log of when items are placed

#RandoSeed = 1234567890
RandoSeed = datetime.time(datetime.now())


#Ability Checks
HasLeapStone = False
HasGravityBoots = False
HasJewelOfOpen = False
HasMist = False
HasPowerOfMist = False
HasBat = False
HasWolf = False
HasSonar = False
HasMermanStatue = False

#TODO
	#accept args
	#args: Player Seed input
	#args for other options
	#Options to not randomize boss relics	
	#Copy files instead of just overwriting
	#do a hash check to ensure its editing the right file
	#possibly make a small frontend for it?

#Known Bugs
	#need to trace relics from left/right as well as up/down because of how sotn loads entities
		#List of known delinquents
		#Cube Of Zoe
		#Spirit Orb
		#Farie Scroll
		#Leap Stone
	
#Some relics have doubles, so..
	#Relic ID/Name 			#RelicLocation ID 	#Cant Be Behind 			RL ID No-Gos
	#00	Soul of Bat 		00					
	#01	Fire of Bat 		01					
	#02	Echo of Bat 		02					Castle 2 					18 19 1a 1b 1c
	#03	Force of Echo 		03					
	#04	Soul of Wolf 		04					
	#05	Power of Wolf  		05					
	#05	Power of Wolf 		05					
	#06	Skill of Wolf 		06					
	#07	Form of Mist 		07					Castle 2, Mist Gates 		18 19 1a 1b 1c 00
	#08	Power of Mist 		08					
	#09	Gas Cloud 			09					
	#0A	Cube of Zoe 		0a					
	#0A Cube of Zoe  		0a					
	#0B	Spirit Orb			0b					
	#0C	Gravity Boots		0c					
	#0D	Leap Stone			0d					
	#0E	Holy Symbol			0e					
	#0F	Faerie Scroll		0f					
	#10	Jewel of Open		10					Castle 2, Jewel Doors 		18 19 1a 1b 1c 0d 0e 11 15
	#11	Merman Statue		11					Holy Snorkel Location 		0e
	#12	Bat Card			12					
	#13	Ghost Card			13					
	#14	Faerie Card			14					
	#15	Demon Card			15					
	#16	Sword Card			16					
	#17	Sprite Card			--					
	#18	Nosedevil Card 		--					
	#19	Heart of Vlad		17					
	#19	Heart of Vlad		17					
	#1A	Tooth of Vlad		18					
	#1A	Tooth of Vlad		18					
	#1B	Rib of Vlad			19					
	#1B	Rib of Vlad			19					
	#1C	Ring of Vlad		1a					
	#1C	Ring of Vlad		1a					
	#1D Eye of Vlad			1b					
	#1D Eye of Vlad			1b					
RelicLocation = [0x047a5b66, 0x0557535e, 0x04aa4156, 0x0526e6a8, 0x049d6596, 0x04b6b9b4, 0x054b1d5a, 0x043c578a, 
	0x05610db8, 0x04cfcb16, 0x04b6b946, 0x048fd1fe, 0x048fc9ba, 0x05610dc2, 0x04c34ee6, 0x047a5720, 
	0x047a321c, 0x04c35174, 0x054b1d58, 0x05611958, 0x047a5784, 0x045ea95e, 0x04aa3f76, 0x06306ab2, 
	0x05051d52, 0x069d2b1e, 0x059bdb30, 0x04da65f2]
DoubleLocation = [0, 0, 0, 0, 0, 0x053f971c, 0, 0, 
	0x0561142C, 0, 0x053F969A, 0, 0, 0, 0, 0,
	0, 0, 0, 0x0561127c, 0, 0, 0, 0x04e335b4, 
	0x067d1630, 0x050fa914, 0x059ee2e4, 0x0662263a]
TripleLocation = [0, 0, 0, 0, 0, 0, 0, 0, 
	0, 0, 0x04b6b08a, 0x048fe280, 0, 0, 0, 0,
	0, 0, 0, 0, 0, 0, 0, 0, 
	0, 0, 0, 0]
QuadrupleLocation = [0, 0, 0, 0, 0, 0, 0, 0, 
	0, 0, 0x053f8e2e, 0, 0, 0, 0, 0,
	0, 0, 0, 0, 0, 0, 0, 0, 
	0, 0, 0, 0]
RelicList = []
RelicList = [bytearray([0x00]),
	bytearray([0x01]),
	bytearray([0x02]),
	bytearray([0x03]),
	bytearray([0x04]),
	bytearray([0x05]),
	bytearray([0x06]),
	bytearray([0x07]),
	bytearray([0x08]),
	bytearray([0x09]),
	bytearray([0x0a]),
	bytearray([0x0b]),
	bytearray([0x0c]),
	bytearray([0x0d]),
	bytearray([0x0e]),
	bytearray([0x0f]),
	bytearray([0x10]),
	bytearray([0x11]),
	bytearray([0x12]),
	bytearray([0x13]),
	bytearray([0x14]),
	bytearray([0x15]),
	bytearray([0x16]),
	bytearray([0x19]),
	bytearray([0x1a]),
	bytearray([0x1b]),
	bytearray([0x1c]),
	bytearray([0x1d])]

RelicsUsed = []
LocationsUsed = []
for i in range(0, len(RelicList)):
	RelicsUsed.append(False)
	LocationsUsed.append(False)

def ReplaceByte(ByteLocation, NewByte):
	with file(FileName, "r+b") as HackThisRom:
		HackThisRom.seek(ByteLocation)
		HackThisRom.write(NewByte)
	return True

def PlaceItem(Item, Location):
	if ShowItemPlacements:
		print("Placing Item: "+hexlify(RelicList[Item]))
		#print("Location a: "+str(hex(RelicLocation[Location])))
	ReplaceByte(RelicLocation[Location], RelicList[Item])

	if (DoubleLocation[Location] != 0):
		#if ShowItemPlacements:
		#	print("Location b: "+str(hex(DoubleLocation[Location])))
		ReplaceByte(DoubleLocation[Location], RelicList[Item])		

	if (TripleLocation[Location] != 0):
		#if ShowItemPlacements:
		#	print("Location b: "+str(hex(DoubleLocation[Location])))
		ReplaceByte(TripleLocation[Location], RelicList[Item])		

	if (QuadrupleLocation[Location] != 0):
		#if ShowItemPlacements:
		#	print("Location b: "+str(hex(DoubleLocation[Location])))
		ReplaceByte(QuadrupleLocation[Location], RelicList[Item])		
	
	#Check abilities if possible
	global HasJewelOfOpen 
	global HasLeapStone
	global HasMist
	global HasPowerOfMist
	global HasGravityBoots
	global HasBat
	global HasWolf
	global HasSonar
	global HasMermanStatue

	if Item == 0x10:
		HasJewelOfOpen = True
	elif Item == 0xd:
		HasLeapStone = True
	elif Item == 0x7:
		HasMist = True
	elif Item == 0x8:
		HasPowerOfMist = True
	elif Item == 0xc:
		HasGravityBoots = True
	elif Item == 0x4:
		HasWolf = True
	elif Item == 0x0:
		HasBat = True
	elif Item == 0x2:
		HasSonar = True
	elif Item == 0x11:
		HasMermanStatue = True

	#Mark as used
	RelicsUsed[Item] = True
	LocationsUsed[Location] = True
	return True

def FindUnplacedRelic():
	#print(len(RelicList))
	RandIndex = random.randint(0, len(RelicList)-1)
	if RelicsUsed[RandIndex]:
		return FindUnplacedRelic()
	else:
		return RandIndex

def FindUnplacedLocation(InputArray):
	RandIndex = InputArray[random.randint(0, len(InputArray)-1)]
	if LocationsUsed[RandIndex]:
		return FindUnplacedLocation(InputArray)
	else:
		return RandIndex

def SoftUnlock():
	#print(str(HasJewelOfOpen)+" | "+str(HasLeapStone)+" | "+str(HasMist)+" | "+str(HasPowerOfMist)+" | "+str(HasGravityBoots)+" | "+str(HasBat)+" | "+str(HasSonar)+" | "+str(HasMermanStatue))
	#List of available locations
	LocationsAvailable = []
	#Starting Areas
	if LocationsUsed[0x04] == False:
		LocationsAvailable.append(0x04)
	if LocationsUsed[0x0a] == False:
		LocationsAvailable.append(0x0a)
	if LocationsUsed[0x0b] == False:
		LocationsAvailable.append(0x0b)
	if LocationsUsed[0x0f] == False:
		LocationsAvailable.append(0x0f)
	if LocationsUsed[0x10] == False:
		LocationsAvailable.append(0x10)
	
	#Restricted Areas
	if HasMist and (HasLeapStone or HasGravityBoots or HasBat):
		#Soul of Bat Vanilla
		if LocationsUsed[0x00] == False:
			LocationsAvailable.append(0x00)
	if HasBat or (HasGravityBoots and HasLeapStone) or (HasMist and HasPowerOfMist):
		#Flight only
		if LocationsUsed[0x01] == False:
			LocationsAvailable.append(0x01)
		if LocationsUsed[0x05] == False:
			LocationsAvailable.append(0x05)
		if LocationsUsed[0x08] == False:
			LocationsAvailable.append(0x08)
		if LocationsUsed[0x0c] == False:
			LocationsAvailable.append(0x0c)
		if LocationsUsed[0x13] == False:
			LocationsAvailable.append(0x13)
		if LocationsUsed[0x16] == False:
			LocationsAvailable.append(0x16)
	if (HasBat or (HasMist and HasPowerOfMist) or (HasGravityBoots and HasLeapStone)) and (HasMist or HasWolf or HasBat):
		if LocationsUsed[0x02] == False: #Olrox's Prize
			LocationsAvailable.append(0x02)
	if HasGravityBoots or HasBat or (HasMist and HasPowerOfMist):
		#Gravity Boots or better
		if LocationsUsed[0x06] == False:
			LocationsAvailable.append(0x06)
		if LocationsUsed[0x12] == False:
			LocationsAvailable.append(0x12)
		if LocationsUsed[0x14] == False:
			LocationsAvailable.append(0x14)
	if HasLeapStone or HasGravityBoots or HasBat or (HasMist and HasPowerOfMist):
		#Leapstone or better
		if LocationsUsed[0x07] == False:
			LocationsAvailable.append(0x07)
		if LocationsUsed[0x0d] == False:
			LocationsAvailable.append(0x0d) #Colosseum - only required if leap stone?
	if HasJewelOfOpen:
		#Bottom of the castle
		if LocationsUsed[0x11] == False:
			LocationsAvailable.append(0x11)
	if HasJewelOfOpen and HasLeapStone or HasBat or (HasMist and HasPowerOfMist):
		if LocationsUsed[0x15] == False: #Demon card a bitch
			LocationsAvailable.append(0x15)
	if HasMermanStatue and HasJewelOfOpen:
		#holy snorkel vanilla
		if LocationsUsed[0x0e] == False:
			LocationsAvailable.append(0x0e)
	if HasJewelOfOpen and HasMist and (HasBat or HasPowerOfMist or (HasLeapStone and HasGravityBoots)) and (HasPowerOfMist or HasSonar):
		#Castle 2 - Flight, Mist, Jewel of Open, and sonar or power of mist
		if LocationsUsed[0x03] == False:
			LocationsAvailable.append(0x03)
		if LocationsUsed[0x09] == False:
			LocationsAvailable.append(0x09)
		if LocationsUsed[0x17] == False:
			LocationsAvailable.append(0x17)
		if LocationsUsed[0x18] == False:
			LocationsAvailable.append(0x18)
		if LocationsUsed[0x19] == False:
			LocationsAvailable.append(0x19)
		if LocationsUsed[0x1a] == False:
			LocationsAvailable.append(0x1a)
		if LocationsUsed[0x1b] == False:
			LocationsAvailable.append(0x1b)

	ThisRel = FindUnplacedRelic()
	if len(LocationsAvailable) == 1:
		#Only one location left?
		#Check to see if its the last item in the game
		#If not, give an item that will unlock more items
		#I need to actually think this through and place the correct items, but this will do for now
		if HasJewelOfOpen == False:
			ThisRel = 0x10
		elif HasLeapStone == False:
			ThisRel = 0x0D
		elif HasGravityBoots == False:
			ThisRel = 0x0C
		elif HasBat == False:
			ThisRel = 0x00
		elif HasMist == False:
			ThisRel = 0x07
		elif HasMermanStatue == False:
			ThisRel = 0x11
	else:
		ThisRel = FindUnplacedRelic()

	ThisLoc = FindUnplacedLocation(LocationsAvailable)

	#Items are never allowed in these locations
	if ThisRel == 0x02:
		if ThisLoc == 0x18 or ThisLoc == 0x19 or ThisLoc == 0x1a or ThisLoc == 0x1b or ThisLoc == 0x1c:
			return SoftUnlock()
	elif ThisRel == 0x07:
		if ThisLoc == 0x18 or ThisLoc == 0x19 or ThisLoc == 0x1a or ThisLoc == 0x1b or ThisLoc == 0x1c or ThisLoc == 0x00:
			return SoftUnlock()
	elif ThisRel == 0x10:
		if ThisLoc == 0x18 or ThisLoc == 0x19 or ThisLoc == 0x1a or ThisLoc == 0x1b or ThisLoc == 0x1c or ThisLoc == 0x0d or ThisLoc == 0x0e or ThisLoc == 0x11 or ThisLoc == 0x15:
			return SoftUnlock()
	elif ThisRel == 0x11:
		if ThisLoc == 0x0e:
			return SoftUnlock()

	retval = [ThisRel, ThisLoc]
	return retval

def main():
	print("Sotn Relic Randomizer")
	print("Your file name should be \""+FileName+"\"")
	print("To show spoilers, edit the script and set ShowItemPlacements to True")
	print("If this is your first time running, you will need to download error_recalc.exe and put it in the same directory as this script. You can grab it here: https://www.romhacking.net/utilities/1264/")
	print("")
	
	random.seed(RandoSeed)
	print("Seed is \""+str(RandoSeed)+"\"")

	#Do some shuffling things, make sure things arent impossible to access
	#Make things always possible later
	print("Shuffling Relics..")

	#Place the rest of the items
	for i in range(0, len(RelicList)):
		PlsNoSoftlock = SoftUnlock()
		ThisRelic = PlsNoSoftlock[0]
		ThisLocation = PlsNoSoftlock[1]
		PlaceItem(ThisRelic, ThisLocation)

	print("Bytes Written, Fixing ECC..")

	#Windows
	#call(["error_recalc.exe", FileName, "1"])

	#Not Windows
	call(["wine", "error_recalc.exe", FileName, "1"])

	print("Done")

if __name__ == '__main__':
	main()
