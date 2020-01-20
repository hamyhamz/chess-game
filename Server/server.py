"""Implementation of server part of application
Authors:
   Peter Hamran        xhamra00@stud.fit.vutbr.cz
Date:
   20.01.2020
"""
from numpy import random


class Server:

    def __init__(self):
        self.id = random.random()


if __name__ == '__main__':
    print("PUF")