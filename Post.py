__author__ = 'xi'
import socket,time

class Post:

    url=""
    postdata=""
    path=""
    def __init__(self,url,path,postdata):
        self.url=url
        self.postdata=postdata
        self.path=path

    def submit(self):
        host=self.url
        oldtime=time.time()
        try:
            se=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            se.connect((host,80))
            se.send("POST "+self.path+"/ HTTP/1.1\n")
            se.send("Accept:text/html,application/xhtml+xml,*/*;q=0.8\n")
            se.send("Accept-Language:zh-CN,zh;q=0.8,en;q=0.6\n")
            se.send("User-Agent: Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9.2.3) Gecko/20100401 Firefox/3.6.3\r\n")
            se.send("Cache-Control:max-age=0\n")
            se.send("Connection:keep-alive\n")
            se.send("Host:"+host+"\r\n")
            se.send(self.postdata+"\r\n")
            return se.recv(1024).split("\n")[0],(time.time()-oldtime)
        except Exception as e:
            return e,time.time()-oldtime