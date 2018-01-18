from abc import ABCMeta, abstractclassmethod
from multiprocessing import Process, Pipe
from time import sleep


class ProcessTask(Process):

    INTERVAL = 1

    def __init__(self):
        self.pipe = None
        self.buf = {}
        self.killer_r, self.killer_s = Pipe(False)
        Process.__init__(self)

    def __del__(self):
        """
        デストラクタです。スレッドを止めます。
        :return: None
        """
        self.stop()

    def set_pipe(self, duplex=True):
        r, s = Pipe(duplex)
        self.pipe = r
        return s
        
    def stop(self):
        self.killer_s.send("die")

    def is_dead(self):
        if self.killer_r.poll():
            if self.killer_r.recv() == "die":
                return True
        return False

    def run(self):
        while not self.is_dead():
            self.work()
            sleep(self.INTERVAL)

    @abstractclassmethod
    def work(self):
        """
        タスクの本体です。
        抽象メソッドです。
        :return: None
        """
        pass

    def recv(self):
        if self.pipe.poll():
            self.buf = self.pipe.recv()
            return self.buf
        else:
            return False

    def send(self, data):
        self.pipe.send(data)
