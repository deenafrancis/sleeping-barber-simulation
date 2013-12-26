from threading import Thread, Lock, Event
import time, random, json

mutex = Lock()

#Interval in seconds
customerIntervalMin = 5
customerIntervalMax = 15
haircutDurationMin = 15
haircutDurationMax = 20

class BarberShop:
	waitingCustomers = []
	actions = []

	def __init__(self, barber, numberOfSeats):
		self.barber = barber
		self.numberOfSeats = numberOfSeats
		self.actions.append('BarberShop initilized with {0} seats'.format(numberOfSeats))
		self.actions.append('Customer min interval {0}'.format(customerIntervalMin))
		self.actions.append('Customer max interval {0}'.format(customerIntervalMax))
		self.actions.append('Haircut min duration {0}'.format(haircutDurationMin))
		self.actions.append('Haircut max duration {0}'.format(customerIntervalMax))
		#print '---------------------------------------'

	def openShop(self):
		self.actions.append('Barber shop is opening')
		workingThread = Thread(target = self.barberGoToWork)
		workingThread.start()

	def barberGoToWork(self):
		while True:
			mutex.acquire()

			if len(self.waitingCustomers) > 0:
				c = self.waitingCustomers[0]
				del self.waitingCustomers[0]
				mutex.release()
				self.actions.append('{0} is having a haircut'.format(c.name))
				self.barber.cutHair(c)
				self.actions.append('{0} is done'.format(c.name))
			else:
				mutex.release()
				self.actions.append('Aaah, all done, going to sleep')
				barber.sleep()
				self.actions.append('Barber woke up')
	
	def enterBarberShop(self, customer):
		mutex.acquire()
		self.actions.append('>> {0} entered the shop and is looking for a seat'.format(customer.name))

		if len(self.waitingCustomers) == self.numberOfSeats:
			self.actions.append('Waiting room is full, {0} is leaving.'.format(customer.name))
			mutex.release()
		else:
			self.actions.append('{0} sat down in the waiting room'.format(customer.name))
			self.waitingCustomers.append(c)	
			mutex.release()
			barber.wakeUp()

class Customer:
	def __init__(self, name):
		self.name = name

class Barber:
	barberWorkingEvent = Event()
	state = "sleeping"
	customer = "none"
	def sleep(self):
		self.state = "sleeping"
		self.customer = "none"
		self.barberWorkingEvent.wait()

	def wakeUp(self):
		self.barberWorkingEvent.set()

	def cutHair(self, customer):
		#Set barber as busy 
		self.barberWorkingEvent.clear()
		self.state = "busy"
		self.customer = customer.name
		#print '{0} is having a haircut'.format(customer.name)

		randomHairCuttingTime = random.randrange(haircutDurationMin, haircutDurationMax+1)
		time.sleep(randomHairCuttingTime)
		#print '{0} is done'.format(customer.name)



def genJson(barbershop):
	while True:
		jsn = []
		first = []
		barber = {"state" : barbershop.barber.state, "customer" : barbershop.barber.customer }
		first.append(barber)
		count = 1
		for cust in barbershop.waitingCustomers:
			c = { "name" : cust.name }
			first.append(c)
			count += 1
		for ii in range(count, barbershop.numberOfSeats+1):
			c = { "name" : "none" }
			first.append(c)
		jsn.append(first)
		jsn.append(barbershop.actions)
		fp = open("bshop.json", "w")
		json.dump(jsn, fp)
		fp.close()
		time.sleep(1)



if __name__ == '__main__':
	customers = []
	customers.append(Customer('Adam'))
	customers.append(Customer('Billy'))
	customers.append(Customer('Chris'))
	customers.append(Customer('Don'))
	customers.append(Customer('Ed'))
	customers.append(Customer('Fred'))
	customers.append(Customer('Greg'))
	customers.append(Customer('Henry'))
	customers.append(Customer('Ian'))
	customers.append(Customer('John'))
	customers.append(Customer('Ken'))
	customers.append(Customer('Lionel'))
	customers.append(Customer('Marty'))
	customers.append(Customer('Ned'))
	customers.append(Customer('Owen'))
	customers.append(Customer('Patrick'))
	customers.append(Customer('Quentin'))

	barber = Barber()

	barberShop = BarberShop(barber, numberOfSeats=3)
	workingThread = Thread(target = genJson, args=(barberShop,))
	workingThread.start()
	barberShop.openShop()

	while len(customers) > 0:
		c = customers.pop()	
		#New customer enters the barbershop
		barberShop.enterBarberShop(c)
		customerInterval = random.randrange(customerIntervalMin,customerIntervalMax+1)
		time.sleep(customerInterval)

		

