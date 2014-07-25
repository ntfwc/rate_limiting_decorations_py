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

from multiprocessing import Process
from Decorators import rateLimit_multiprocessingLock

from time import sleep

@rateLimit_multiprocessingLock(2)
def rateLimitedPrintFunction(string):
	print(string)

class TestProcess(Process):
	def __init__(self, threadNum):
		Process.__init__(self)
		self.threadNum = threadNum
		
	def run(self):
		for i in range(8):
			rateLimitedPrintFunction("Testing: i=%s process=%s" % (i, self.threadNum))
			sleep(0.2)


from multiprocessing import Value
def main():
	t1 = TestProcess(1)
	t2 = TestProcess(2)
	t3 = TestProcess(3)
	t1.start()
	t2.start()
	t3.start()

main()
