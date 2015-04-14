import math
from copy import deepcopy

def fileToData(f):
	data = f.readlines()
	return data[9:]

def lineSpliter(line):
	SplitedList = line.split()
	for i in range(3):
		SplitedList[i]=int(SplitedList[i])
	for i in range(3,len(SplitedList)):
		SplitedList[i]=float(SplitedList[i])
	return SplitedList

def dataToDict(data):
	Dict = {}
	for line in data:
		line = lineSpliter(line)
		AtomInfo = {}
		AtomInfo['id']   = line[0]
		AtomInfo['mol']  = line[1]
		AtomInfo['type'] = line[2]
		AtomInfo['x']    = line[3]
		AtomInfo['y']    = line[4]
		AtomInfo['z']    = line[5]
		AtomInfo['xu']   = line[6]
		AtomInfo['yu']   = line[7]
		AtomInfo['zu']   = line[8]
		AtomInfo['vx']   = line[9]
		AtomInfo['vy']   = line[10]
		AtomInfo['vz']   = line[11]
		Dict[line[0]] = AtomInfo
	return Dict

def reviseDict(referencedict,newdict):
	'''

	xu, yu, x, y need to be revised 
	since the size of the box has been changed in NPT system.

	'''
	thisdict = deepcopy(newdict)
	AtomID = [1,100]

	# here
	reference1 = referencedict[AtomID[0]]
	reference2 = referencedict[AtomID[1]]
	thisdict1 = thisdict[AtomID[0]]
	thisdict2 = thisdict[AtomID[1]]

	assert reference1['vx'] == 0
	assert reference2['vx'] == 0
	def reviseXu(xu):
		xu = (xu - thisdict1['xu'])\
			/(thisdict2['xu']-thisdict1['xu'])\
			*(reference2['xu']-reference1['xu'])\
			+ reference1['xu']
		return xu
	def reviseYu(yu):
		yu = (yu - thisdict1['yu'])\
			/(thisdict2['yu']-thisdict1['yu'])\
			*(reference2['yu']-reference1['yu'])\
			+ reference1['yu']
		return yu

	for Atom in thisdict:
		thisdict[Atom]['xu'] = reviseXu(thisdict[Atom]['xu'])
		thisdict[Atom]['yu'] = reviseYu(thisdict[Atom]['yu'])
		thisdict[Atom]['x'] = reviseXu(thisdict[Atom]['x'])
		thisdict[Atom]['y'] = reviseYu(thisdict[Atom]['y'])		

	return thisdict



def allDisplacement(dict1,dict2):
	size1 = len(dict1)
	size2 = len(dict2)
	assert size1==size2

	AllDisplacementDict = {}
	for i in range(1,size1+1):
		OneDisplacementDict = {}

		OneDisplacementDict['xu'] = dict2[i]['xu']-dict1[i]['xu']
		OneDisplacementDict['yu'] = dict2[i]['yu']-dict1[i]['yu']
		OneDisplacementDict['zu'] = dict2[i]['zu']-dict1[i]['zu']
		OneDisplacementDict['disp'] = math.sqrt(	OneDisplacementDict['xu']*OneDisplacementDict['xu']+
											OneDisplacementDict['yu']*OneDisplacementDict['yu']+
											OneDisplacementDict['zu']*OneDisplacementDict['zu']) 

		AllDisplacementDict[i] = OneDisplacementDict
	return AllDisplacementDict



NeedSteps= [0,1,10]
ReferenceStep = 10


f=[]
for i in range(len(NeedSteps)):
	FileName = 'data.' + str(NeedSteps[i])
	print FileName
	f.append(open(FileName,'r'))


AllDict = {}
for Files in f:
	NewData = fileToData(Files)
	NewDict = dataToDict(NewData)
	AllDict[NeedSteps[f.index(Files)]] = NewDict
	# print NewDict[1]

AllRevisedDict = {}
# print AllDict[ReferenceStep][1]
for Dict in AllDict:
	NewRevisedDict = reviseDict(AllDict[ReferenceStep],AllDict[Dict])
	AllRevisedDict[ReferenceStep]=NewRevisedDict
	# print NewRevisedDict[1]


