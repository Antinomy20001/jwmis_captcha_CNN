import requests
import threading

url = 'http://jwmis.hnie.edu.cn/jwweb/'


def set_params(ss, key, value):
    ss.headers[key] = value

def create(path):
    session = requests.session()
    set_params(session, 'User-Agent',
               'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36')
    set_params(session, 'Referer', url)
    set_params(session, 'Upgrade-Insecure-Requests', '1')
    html = session.get(url)
    set_params(session, 'Cookie', 'ASP.NET_SessionId=%s' %
               session.cookies['ASP.NET_SessionId'])
    set_params(session, 'Referer', url + '_data/index_LOGIN.aspx')
    set_params(session, 'Accept',
               'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8')
    set_params(session, 'Accept-Encoding', 'gzip, deflate')
    set_params(session, 'Accept-Language',
               'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7')
    html = session.get(url + 'sys/ValidateCode.aspx', stream=True)
    with open(path, 'wb') as f:
        f.write(html.content)


class Worker(threading.Thread):
    def __init__(self, low, high):
        super(Worker, self).__init__()
        self.low = low
        self.high = high
        self.isStop = False

    def run(self):
        i = self.low
        while not self.isStop:
            try:
                create('dataset/%d.jpg' % i)
                print('dataset/%d.jpg' % i)
                i += 1
                if i == self.high:
                    self.stop()
            except:
                pass

    def stop(self):
        self.isStop = True


if __name__ == '__main__':
    import sys
    cnt = int(sys.argv[1]) // 4
    worker1 = Worker(0, cnt)
    worker2 = Worker(cnt, cnt * 2)
    worker3 = Worker(cnt * 2, cnt * 3)
    worker4 = Worker(cnt * 3, cnt * 4)
    worker1.start()
    worker2.start()
    worker3.start()
    worker4.start()

    worker1.join()
    worker2.join()
    worker3.join()
    worker4.join()
