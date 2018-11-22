import numpy as np


def func123( thelist ):  #RastriginFunction
	val = 0.0
	for i in range(len(thelist)):
		val += pow(thelist[i], 2)
	return val
def func2( thelist ): #RosenbrockFunction
	val = 0.0
	for i in range(len(thelist)-1):
		val += (100*np.power( np.power(thelist[i],2) - thelist[i+1],2) + np.power(1 - thelist[i],2) )
	return val
def func3( thelist ):
	val = 0.0
	for i in range(len(thelist)):
		val += ((-1 * thelist[i]) * np.sin(np.sqrt(np.fabs(thelist[i]))))
	return val
def func4( thelist) :
	val1 = 0.0
	val2 = 1.0
	for i in range(len(thelist)):
		val1 += (np.power(thelist[i],2) / 4000)
	for i in range(len(thelist)):
		val2 *= np.cos(thelist[i]/np.sqrt(i+1))
	return val1 - val2 + 1


def func5(dimensions):
	return np.cos(dimensions[0]) * np.cos(dimensions[1])

def func666(dimensions):
	return np.sin(np.sin(dimensions[0]*dimensions[1]))

def funcWhat(dimensions):
	return (math.e**dimensions[0])*np.sin(dimensions[1])



def functionSameAs1(coordinates): #SphereFunction
	result = 0.0
	for i in range(0, len(coordinates)):
		result += np.power(coordinates[i],2)

	return result


def AckleyFunction(coordinates): #AckleyFunction
	dim = len(coordinates)
	a = 20
	d = 0.2
	c = 2 * math.pi
	temp1 = 0.0
	temp2 = 0.0
	for i in range(0,dim):
		temp1 += np.power(coordinates[i],2)
		temp2 += np.cos(c*coordinates[i])

	temp11 = -a * np.exp(-0.2 * np.power((0.5*temp1), 1/2))
	temp21 = np.exp(0.5 * temp2)
	result = temp11 - temp21 + a + np.exp(1)
	return result


# SchwefelFunction
def SchwefelFunction(poi):
	result = 0.0
	for i in range(0, len(poi)):
		result += poi[i] * np.sin(np.sqrt(abs(poi[i])))

	result = 418.9829 * len(poi) - result
	return result
