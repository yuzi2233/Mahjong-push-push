import os
import socket
from datetime import datetime
from Mahjong import *



def startGame():
    my_array = [[Mahjong() for j in range(5)] for i in range(9)]
    my_array[0][0].form = 1
    print(my_array[0][0].form)

startGame()
