__author__ = 'mgchbot'
import httpload,Get,Post

threadnums=[1,2,3,4,5]
for i in range(len(threadnums),1,-1):
    threadnums[i-1]=sum(threadnums[0:i])
print threadnums