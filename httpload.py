#encoding=utf-8
import Post,Get
import threading,time
import random as R
import Global
import sys
import multiprocessing
from pylab import *

from multiprocessing import Process, Queue

def TestGet(Q,threadnum,url,path,T):

    for i in range(0,threadnum):
        try:
            gt=GetThread(url,T,i,path)
            gt.start()
        except Exception as e:
            print i,"falied"
            time.sleep(0.1)
            continue
    lenr=len(Global.result)
    while True:
        time.sleep(T+5)
        if len(Global.result)==lenr:
            break
        lenr=len(Global.result)

    Q.put(Global.result)

def TestPost(Q,threadnum,url,path,postdata,T):

    for i in range(0,threadnum):
        try:
            pt=PostThread(url,T,i,path,postdata)
            pt.start()
        except Exception as e:
            print i,"falied"
            time.sleep(0.1)
            continue
    lenr=len(Global.result)
    while True:
        time.sleep(T+5)
        if len(Global.result)==lenr:
            break
        lenr=len(Global.result)
    Q.put(Global.result)

def UserTest(Q,lock,threadnum,actList,T):
    for i in range(0,threadnum):
        try:
            ut=UserThread(lock,actList,T,i)
            ut.start()
        except Exception as e:
            print i,"falied"
            time.sleep(0.1)
            continue
    lenr=len(Global.result)
    while True:
        time.sleep(T+5)
        if len(Global.result)==lenr:
            break
        lenr=len(Global.result)
    Q.put(Global.result)

def MultiUserTest(Q,lock,threadnum,threadnums,actLists,T,index):
    for i in range(0,threadnum):
        for k in range(0,len(threadnums)):
            if (index*threadnum+i)<threadnums[k]:
                j=k
                break
        try:
            ut=UserThread(lock,actLists[j],T,i)
            ut.start()
        except Exception as e:
            print i,"falied"
            time.sleep(0.1)
            continue
    lenr=len(Global.result)
    while True:
        time.sleep(T+5)
        if len(Global.result)==lenr:
            break
        lenr=len(Global.result)
    Q.put(Global.result)

def TestPostProcess(threadnum,url,path,postdata,T):
    del Global.result[:]
    Q=Queue(Global.CPUs)
    for i in range(0,Global.CPUs):
        p = multiprocessing.Process(target = TestPost, args = (Q,threadnum/Global.CPUs,url,path,postdata,T,))
        p.start()
    st=time.time()
    while True:
        time.sleep(1)
        if Q.qsize()==Global.CPUs:
            break
    for i in range(0,Global.CPUs):
        Global.result.extend(Q.get(i))

def TestGetProcess(threadnum,url,path,T):
    del Global.result[:]
    Q=Queue(Global.CPUs)
    for i in range(0,Global.CPUs):
        p = multiprocessing.Process(target = TestGet, args = (Q,threadnum/Global.CPUs,url,path,T,))
        p.start()
    st=time.time()
    while True:
        time.sleep(1)
        if Q.qsize()==Global.CPUs:
            break
    for i in range(0,Global.CPUs):
        Global.result.extend(Q.get(i))


def TestUserProcess(threadnum,filename,T):
    actList=[]
    for line in open(filename):
        words=line.split("||")
        temp=[]
        for w in words:
            temp.append(w)
        actList.append(temp)
    del Global.result[:]
    Q=Queue(Global.CPUs)
    lock = multiprocessing.Lock()
    for i in range(0,Global.CPUs):
        p = multiprocessing.Process(target = UserTest, args = (Q,lock,threadnum/Global.CPUs,actList,T,))
        p.start()
    st=time.time()
    while True:
        time.sleep(1)
        if Q.qsize()==Global.CPUs:
            break
    for i in range(0,Global.CPUs):
        Global.result.extend(Q.get(i))

def TestMultiUserProcess(filenames,threadnums,T):

    allnums=sum(threadnums)
    eachnums=allnums/Global.CPUs
    actLists=[]
    for i in range(len(threadnums),1,-1):
        threadnums[i-1]=sum(threadnums[0:i])
    for i in range(0,len(filenames)):
        actList=[]
        for line in open(filenames[i]):
            words=line.split("||")
            temp=[]
            for w in words:
                temp.append(w)
            actList.append(temp)
        actLists.append(actList)
    del Global.result[:]
    Q=Queue(Global.CPUs)
    lock = multiprocessing.Lock()
    for i in range(0,Global.CPUs):
        p = multiprocessing.Process(target = MultiUserTest, args = (Q,lock,eachnums,threadnums,actLists,T,i,))
        p.start()
    st=time.time()
    while True:
        time.sleep(1)
        if Q.qsize()==Global.CPUs:
            break
    for i in range(0,Global.CPUs):
        Global.result.extend(Q.get(i))



class GetThread(threading.Thread):

    T=0
    i=0
    url=""
    path=""
    __result=[]
    def __init__(self,url,T,i,path):
        threading.Thread.__init__(self)
        self.url=url
        self.i=i
        self.T=T
        self.path=path

    def run(self):
        startime=time.time()
        gt=Get.Get(self.url,self.path)
        while(time.time()-startime<self.T):
            self.__result.append(gt.submit())
        while True:
            if Global.mutex.acquire(5):
                # print self.i
                Global.result.append(self.__result)
                Global.mutex.release()
                break
            else:
                time.sleep(R.randint(0,3))

class PostThread(threading.Thread):

    T=0
    i=0
    url=""
    path=""
    postdata=""
    __result=[]
    def __init__(self,url,T,i,path,postdata):
        threading.Thread.__init__(self)
        self.url=url
        self.i=i
        self.T=T
        self.path=path
        self.postdata=postdata

    def run(self):
        startime=time.time()
        pt=Post.Post(self.url,self.path,self.postdata)
        while(time.time()-startime<self.T):
            self.__result.append(pt.submit())
        while True:
            if Global.mutex.acquire(5):
                # print self.i
                Global.result.append(self.__result)
                Global.mutex.release()
                break
            else:
                time.sleep(R.randint(0,3))

class UserThread(threading.Thread):
    actList=[]
    __result=[]
    lock=""
    T=0
    i=0
    def __init__(self,lock,actList,T,i):
        threading.Thread.__init__(self)
        self.actList=actList
        self.lock=lock
        self.T=T
        self.i=i

    def run(self):
        startime=time.time()
        while(time.time()-startime<self.T):
            for act in self.actList:
                if time.time()-startime>self.T:
                    return
                if act[0]=="GET":
                    self.__result.append(Get.Get(act[1].strip(),act[2].strip()).submit())
                elif act[0]=="POST":
                    self.__result.append(Post.Post(act[1].strip(),act[2].strip(),act[3].strip()).submit())
                else:
                    if not act[1]=="-1":
                        time.sleep(int(act[1]))
                    else:
                        time.sleep(R.randint(0,5))
        while True:
            if Global.mutex.acquire(5):
                # print self.i
                Global.result.append(self.__result)
                Global.mutex.release()
                break
            else:
                time.sleep(R.randint(0,3))

def CountAndAnalyse(save,filename):
    if len(Global.result)==0:
        print "Server down."
        return
    dt1={}
    dt2={}
    dt2[0]=0
    dt2[1]=0
    dt2[2]=0
    dt2[3]=0
    dt2[4]=0
    dt2[5]=0
    if save:
        towrite=open(filename,"w")
    else:
        towrite=""
    sum=0
    suml=0
    for line in Global.result:
        for word in line:
            w=word[0][0:-1]
            sum+=1
            suml+=word[1]*1000
            # if save:
            #     towrite.write(w.strip()+"\t"+str(word[1]*1000)+"\n")
            if dt1.has_key(w):
                dt1[w][0]+=1
                dt1[w][1]=float(word[1]*1000)
            else:
                dt1[w]=[1,float(word[1]*1000)]
            if word[1]*1000<50:
                dt2[0]+=1
            elif word[1]*1000<100:
                dt2[1]+=1
            elif word[1]*1000<300:
                dt2[2]+=1
            elif word[1]*1000<500:
                dt2[3]+=1
            elif word[1]*1000<1000:
                dt2[4]+=1
            else:
                dt2[5]+=1
    if save:
        towrite.close()
    print "Request times:",sum
    print "<50ms:",dt2[0],"rate:",dt2[0]/float(sum)
    print "50ms-100ms:",dt2[1],"rate:",dt2[1]/float(sum)
    print "100ms-300ms:",dt2[2],"rate:",dt2[2]/float(sum)
    print "300ms-500ms:",dt2[3],"rate:",dt2[3]/float(sum)
    print "500ms-1000ms:",dt2[4],"rate:",dt2[4]/float(sum)
    print ">1000ms:",dt2[5],"rate:",dt2[5]/float(sum)
    print "average:",suml/float(sum)
    for key in dt1.keys():
        print "Response stat:",key,"count:",dt1[key][0],"rate:",dt1[key][0]/float(sum)

    # figure(1, figsize=(6,6))
    # ax = axes([0.1, 0.1, 0.8, 0.8])
    # labels =dt1.keys()
    # fracs=[]
    # for key in dt1.keys():
    #     fracs.append(dt1[key][0])
    # pie(fracs, labels=labels, autopct='%1.1f%%', shadow=True)
    # legend(fracs,labels)
    # title('Analyse', bbox={'facecolor':'0.8', 'pad':5})

    # figure(1, figsize=(6,6))
    # ax = axes([0.1, 0.1, 0.8, 0.8])
    #
    # labels =dt2.keys()
    # fracs=[]
    # for key in dt2.keys():
    #     fracs.append(dt2[key])
    #
    # pie(fracs, labels=labels, autopct='%1.1f%%', shadow=True)
    # title('Analyse', bbox={'facecolor':'0.8', 'pad':5})
    # show()

def main(argv):

     while(True):
         try:
             print "Testing..."
             if argv[1]=='-g':
                N=0
                url=""
                path=""
                T=""
                s=False
                filename=""
                for i in range(2,len(argv)):
                    if argv[i]=="-n":
                        N=int(argv[i+1])
                    elif argv[i]=="-u":
                        url=argv[i+1]
                    elif argv[i]=="-p":
                        path=argv[i+1]
                    elif argv[i]=="-t":
                        T=int(argv[i+1])
                    elif argv[i]=="-s":
                        s=True
                        file=argv[i+1]
                TestGetProcess(N,url,path,T)
                CountAndAnalyse(s,filename)
             elif argv[1]=='-p':
                N=0
                url=""
                path=""
                postdata=""
                T=""
                s=False
                filename=""
                for i in range(2,len(argv)):
                    if argv[i]=="-n":
                        N=int(argv[i+1])
                    elif argv[i]=="-u":
                        url=argv[i+1]
                    elif argv[i]=="-p":
                        path=argv[i+1]
                    elif argv[i]=="-t":
                        T=int(argv[i+1])
                    elif argv[i]=="-d":
                        postdata=(argv[i+1])
                    elif argv[i]=="-s":
                        s=True
                        file=argv[i+1]
                TestPostProcess(N,url,path,postdata,T)
                CountAndAnalyse(s,filename)
             elif argv[1]=='-u':
                N=0
                path=""
                T=""
                s=False
                filename=""
                for i in range(2,len(argv)):
                    if argv[i]=="-n":
                        N=int(argv[i+1])
                    elif argv[i]=="-f":
                        path=argv[i+1]
                    elif argv[i]=="-t":
                        T=int(argv[i+1])
                    elif argv[i]=="-s":
                        s=True
                        file=argv[i+1]
                TestUserProcess(N,path,T)
                CountAndAnalyse(s,filename)
             elif argv[1]=='-m':
                N=[]
                path=[]
                T=""
                s=False
                filename=""
                for i in range(2,len(argv)):
                    if argv[i]=="-n":
                        k=i+1
                        while not argv[k][0]=="-":
                            N.append(int(argv[k]))
                            k+=1
                    elif argv[i]=="-f":
                        k=i+1
                        while not argv[k][0]=="-":
                            path.append(argv[k])
                            k+=1
                    elif argv[i]=="-t":
                        T=int(argv[i+1])
                    elif argv[i]=="-d":
                        postdata=(argv[i+1])
                TestMultiUserProcess(path,N,T)
                CountAndAnalyse(s,filename)
                print "Finished."
             break
         except Exception as e:
             print e
             break


if __name__ == '__main__':
    # main(sys.argv)

    # a=["user1.txt","user2.txt"]
    # b=[80,40]
    # TestMultiUserProcess(a,b,10)

    # TestUserProcess(40,"./user.txt",10)
    TestGetProcess(4,"192.168.7.200","",10)
    # TestPostProcess(40,"192.168.3.224","","",10)
    CountAndAnalyse(True,"save.xls")

