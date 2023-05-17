# -*- coding: utf-8 -*-
"""
Created on Tue Mar  8 09:07:41 2022

# Bunch of test functions

@author: EIRU0001
"""
import argparse


def hello():
    print("Hello, World!")
    

def add(x,y):
    z = x+y
    print(z)



def say_hello(name):
    print("hello %s" % (name))

def main():
        parser = argparse.ArgumentParser()
        parser.add_argument('-n', '--name', action="store", help='Provides name')
        args = parser.parse_args()

        say_hello(args.name)

def addparser():
        parser = argparse.ArgumentParser()
        parser.add_argument('x', type=int, help='The first value of the addition')
        parser.add_argument('y', type=int, help='The second value of the addition')
        args = parser.parse_args()

        add(args.x, args.y)



if __name__ == ' __main__':
          main()


