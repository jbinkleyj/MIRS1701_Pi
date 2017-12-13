from taskMain import Main
from taskPoll import Poll
from taskComm import Communication
from time import sleep

import logging
import logging.config
logging.config.fileConfig('logging.conf')


if __name__ == '__main__':
    main = Main()
    poll = Poll()
    comm = Communication()
    main.start()
    poll.start()
    comm.start()

    sleep(3)

    main.stop()
    poll.stop()
    comm.stop()
