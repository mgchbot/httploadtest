__author__ = 'mgchbot'
import threading
global mutex
global result
global AllThread
global CPUs
CPUs=4
AllThread=0
result=[]
mutex=threading.Lock()
