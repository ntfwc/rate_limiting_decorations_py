#Copyright (c) 2014 ntfwc

#Permission is hereby granted, free of charge, to any person obtaining a copy
#of this software and associated documentation files (the "Software"), to deal
#in the Software without restriction, including without limitation the rights
#to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#copies of the Software, and to permit persons to whom the Software is
#furnished to do so, subject to the following conditions:

#The above copyright notice and this permission notice shall be included in all
#copies or substantial portions of the Software.

#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#SOFTWARE.

from threading import Lock as ThreadingLock

#function lock for applications using threading
def functionLock_threading(f):
	lock = ThreadingLock()
	def wrapper(*args, **kargs):
		lock.acquire()
		#print("Lock acquired")
		ret = f(*args, **kargs)
		lock.release()
		#print("Lock released")
	return wrapper

from multiprocessing import Lock as MultiProcessingLock

#function lock for applications using multiprocessing
#def functionLock_multiprocessing(f):
	#lock = MultiProcessingLock()
	#def wrapper(*args, **kargs):
		#lock.acquire()
		##print("Lock acquired")
		#ret = f(*args, **kargs)
		#lock.release()
		##print("Lock released")
	#return wrapper

from time import time,sleep

#synchronous non-thread-safe function rate-limiting
def rateLimit(minSecondsBetweenCalls):
	lastTimeCalledContainer=[0.0]
	def decorator(f):
		def wrapper(*args, **kargs):
			currentTime = time()
			lastTimeCalled = lastTimeCalledContainer[0]
			timeSinceLastCall = currentTime - lastTimeCalled
			if timeSinceLastCall < minSecondsBetweenCalls:
				sleep(minSecondsBetweenCalls - timeSinceLastCall)
			lastTimeCalledContainer[0] = time()
			return f(*args, **kargs)
		return wrapper
	return decorator

#Function global Rate-limiting for applications using threading
def rateLimit_threadingLock(minSecondsBetweenCalls):
	def decorator(f):
		@functionLock_threading
		@rateLimit(minSecondsBetweenCalls)
		def wrapper(*args, **kargs):
			return f(*args, **kargs)
		return wrapper
	return decorator

from multiprocessing import Value


#Function global Rate-limiting for applications using multiprocessing
def rateLimit_multiprocessingLock(minSecondsBetweenCalls):
	lock = MultiProcessingLock()
	lastTimeCalledContainer = Value('d')
	def decorator(f):
		def wrapper(*args, **kargs):
			lock.acquire()
			#print("Lock acquired")
			
			currentTime = time()
			lastTimeCalled = lastTimeCalledContainer.value
			timeSinceLastCall = currentTime - lastTimeCalled
			if timeSinceLastCall < minSecondsBetweenCalls:
				sleep(minSecondsBetweenCalls - timeSinceLastCall)
			lastTimeCalledContainer.value = time()
			ret = f(*args, **kargs)
			
			lock.release()
			#print("Lock released")
			
			return ret
		return wrapper
	return decorator
	
