# # __author__ = 'mgchbot'
# # import socket
# # se=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
# # se.connect(("192.168.3.224",80))
# # se.send("GET / HTTP/1.1\n")
# # se.send("Accept:text/html,application/xhtml+xml,*/*;q=0.8\n")
# # se.send("Accept-Language:zh-CN,zh;q=0.8,en;q=0.6\n")
# # se.send("User-Agent: Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9.2.3) Gecko/20100401 Firefox/3.6.3\r\n")
# # se.send("Cache-Control:max-age=0\n")
# # se.send("Connection:keep-alive\n")
# # se.send("Host:"+"192.168.3.224"+"\r\n")
# # se.send("user-agent: Googlebot\n\n")
# # res=se.recv(1024).split("\n")[0]
# # print res
# #
# # import socket
# # host="192.168.3.224"
# # se=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
# # se.connect((host,80))
# # se.send("GET / HTTP/1.1\n")
# # se.send("Accept:text/html,application/xhtml+xml,*/*;q=0.8\n")
# # #se.send("Accept-Encoding:gzip,deflate,sdch\n")
# # se.send("Accept-Language:zh-CN,zh;q=0.8,en;q=0.6\n")
# # se.send("Cache-Control:max-age=0\n")
# # se.send("Connection:keep-alive\n")
# # se.send("Host:"+host+"\r\n")
# # se.send("Referer:http://www.baidu.com/\n")
# # se.send("user-agent: Googlebot\n\n")
# # print se.recv(1024)
# # import random
# # print random.randint(0,5)
# import multiprocessing,Global
# #
# # #
# def worker_1(lock,interval,o):
#         print interval
#         while(True):
#             Global.AllThread+=1
# def worker_2(lock,interval,o):
#         print interval
#         while(True):
#             print Global.AllThread
#
# #
# if __name__ == '__main__':
#     lock = multiprocessing.Lock()
#     p1 = multiprocessing.Process(target = worker_1, args = (lock,2,1))
#     p2 = multiprocessing.Process(target = worker_2, args = (lock,3,1))
#     p1.start()
#     p2.start()


# import cairo;
# import sys;
# import cairo;
# import pycha.pie;
# from lines import lines;
#
# def pycharDemo(output):
#     surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, 800, 800)
#
#     dataSet = [(line[0], [[0, line[1]]]) for line in lines]
#
#     options = {
#         'axis': {
#             'x': {
#                 'ticks': [dict(v=i, label=d[0]) for i, d in enumerate(lines)],
#             }
#         },
#         'legend': {
#             'hide': True,
#         },
#         'title': 'Pie Chart',
#     }
#     chart = pycha.pie.PieChart(surface, options)
#
#     chart.addDataset(dataSet)
#     chart.render()
#
#     surface.write_to_png(output)
#
# if __name__ == '__main__':
#     if len(sys.argv) > 1:
#         output = sys.argv[1]
#     else:
#         output = 'piechart.png'
#     pycharDemo(output);
import random,tables
print(random.randint(0,2))