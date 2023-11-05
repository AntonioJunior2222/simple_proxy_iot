import socket
import threading
import json
import traceback
import sys
from threading import Lock

class Broker:
    
    def __init__(
        self
    ):
        self.__subscribers = dict()
        self.__mutex = Lock()


    def add_publisher(self, pub_id):
        with self.__mutex:
            if not(pub_id in self.__subscribers):
                self.__subscribers[pub_id] = [[],True]
                return True
            elif self.__subscribers[pub_id][1] == True:
                return False
            else:
                self.__subscribers[pub_id][1] = True
                return True

    def add_subscriber(self, pub_id, sub):
        with self.__mutex:
            if not(pub_id in self.__subscribers):
                self.__subscribers[pub_id] = [[],False]
            if not(sub in self.__subscribers[pub_id]):
                self.__subscribers[pub_id][0].append(sub)

    def publish(self, pub_id, data):
        with self.__mutex:
            if pub_id in self.__subscribers:
                for sub in self.__subscribers[pub_id][0]:
                    try:
                        sub.send_data(data)
                    except Full:
                        print("Fila de mensagens cheia")

    def remove_pub(self, pub_id):
        with self.__mutex:
            self.__subscribers.pop(pub_id, None)

    def remove_sub(self, sub):
        with self.__mutex:
            for key in self.__subscribers:
                if sub in self.__subscribers[key]:
                    self.__subscribers[key][0].remove(sub)


