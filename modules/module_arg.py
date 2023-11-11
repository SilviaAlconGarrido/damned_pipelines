#import library
import argparse

#argument parser functions
def argument_parser():
    parser = argparse.ArgumentParser(description= 'Application for arithmetic calculations' )
    help_message ='You have two options. Option 1: "mult" performs multiplication of two given numbers. Option 2: "sum" performs the sum of two given numbers' 
    parser.add_argument('-f', '--function', help=help_message, type=str)
    args = parser.parse_args()
    return args