import selectors
import socket
import time


#1.Future
#2.生成器
#3.Task
class Future():
    def __init__(self):
        self.callbacks = []
    def resolve(self):
        for func in self.callbacks:
            func()

class Task():
    def __init__(self,gen):
        self.gen = gen
        self.step()

    def step(self):
        try:
            f = next(self.gen)
        except StopIteration:
            return
        f.callbacks.append(self.step)


class asynhttp:
    def __init__(self):
        self.selecter = selectors.DefaultSelector()

    def get(self,url,optiondict = None):
        global reqcount
        reqcount += 1
        s = socket.socket()
        s.setblocking(False)
        try:
            s.connect(('127.0.0.1',5555))
        except BlockingIOError:
            pass
        requset = 'GET %s HTTP/1.0\r\n\r\n' % url
        f = Future()
        self.selecter.register(s.fileno(),selectors.EVENT_WRITE,f)
        yield f
        self.selecter.unregister(s.fileno())
        s.send(requset.encode())
        chunks = []
        while True:
            f = Future()
            self.selecter.register(s.fileno(), selectors.EVENT_READ, f)
            yield f
            self.selecter.unregister(s.fileno())
            chunk = s.recv(1024)
            if chunk:
                chunks.append(chunk)
            else:
                reqcount -= 1
                # request_first,request_headers,request_content,_ = ParserHttp.parser(b''.join(chunks))
                # print("解析数据：",request_first,request_headers,request_content)
                print((b''.join(chunks)).decode())
                return (b''.join(chunks)).decode()
reqcount = 0
starttime = time.time()
asynhttper = asynhttp()
Task(asynhttper.get('/bar'))
Task(asynhttper.get('/foo'))
Task(asynhttper.get('/bar'))
Task(asynhttper.get('/foo'))
Task(asynhttper.get('/bar'))
Task(asynhttper.get('/foo'))
while reqcount:
    events = asynhttper.selecter.select()
    for event,mask in events:
        fut = event.data
        fut.resolve()
print("消耗时间：" ,time.time() - starttime)
