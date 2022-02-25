from utils.sqs.sqs import Sqs


class HandlerSubscriber:

    def __init__(self):
        self._sqs = Sqs()

    def pull(self):
        for i in self._sqs.pull_apod():
            print(i)


if __name__ == '__main__':
    handler = HandlerSubscriber()
    handler.pull()