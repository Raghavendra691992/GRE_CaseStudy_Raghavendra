#Modules used in the code
import sys
import requests
import json
import string
import time
import argparse
import re

parser = argparse.ArgumentParser()
parser.add_argument("routeName", help=" Route name in which user wants to travel",type=str)
parser.add_argument("stopName", help=" Stop name user has to board the bus",type=str)
parser.add_argument("directionValue", help=" Direction of the route ( North, South, East, West)",type=str)
args = parser.parse_args()

def input_check ():

    ''' This is the start of the execution
    function used to format the user input into required format and 
    validates the direction parameter '''

    global routeName 
    global stopName 
    global direction

    #formating the inputs        
    routeName = args.routeName.lower().strip()
    stopName = args.stopName.lower().strip()
    directionValue = args.directionValue.lower().strip()

    #predefined direction values for the inputs
    directdict = dict (south=1, north=4, east=2, west=3)
    
    if directionValue in directdict:
        direction = directdict[directionValue]
    else:
        print("Direction should be any one among SOUTH, NORTH, EAST, WEST")
        sys.exit()
    
    get_route_details()

def get_route_details():
    ''' This function valitades the routeName
    fetch the respective routeNo '''

    global routeNo
    condCheck = ""
    urli = "http://svc.metrotransit.org/NexTrip/Routes"
    headers = {'content-type':'Application/json', 'accept':'Application/json'}

    routes = requests.get(url=urli, headers=headers).json()

    for r in routes:       
        if routeName == r.get("Description").lower() :
                routeNo = r.get("Route")
                break    
    else:
                #print("The Route requested is not avaliable")
                print("Route:"+routeName+" "+"Does not exist")
                print("\n1.)To get the list of supported routes Enter:R\n2)To quit enter:Q")
                condCheck=input("Enter your inputs").lower()
                if condCheck == "" or condCheck == "Q" or condCheck == "q":
                    sys.exit()
                elif condCheck == "routes":
                    for i in routes:
                        print(i.get("Description"))
                    print("See you soon!!!")
                    sys.exit()
    direction_validation()

def direction_validation(): 
    ''' This function with respective to routeNo 
    validates the direction avaliable '''
    dirText = ""
    urli = "http://svc.metrotransit.org/NexTrip/Directions/"
    headers = {'content-type':'Application/json', 'accept':'Application/json'}
    allowedDict = requests.get(url=urli+str(routeNo), headers=headers).json()

    for dire in allowedDict:
        if int(dire.get("Value")) == int(direction):
            dirText = dire.get("Text")
            break
    if not dirText :
        print("No Routes in the request directions")
        print("Below are the allowed direction for requested route")
        for i in allowedDict:
            print(i.get("Text")+"\n")
        sys.exit()
    get_stops()
def get_stops():
    ''' This function valitades the stopName
    fetch the respective stopName'''
    global stopCode
    urli = f"http://svc.metrotransit.org/NexTrip/Stops/{str(routeNo)}/{direction}"
    headers = {'content-type':'Application/json', 'accept':'Application/json'}

    stops = requests.get(url=urli, headers=headers).json()

    for stop in stops: 
        if stopName == stop.get("Text").lower().strip():
            stopCode = stop.get("Value")
            #stopText = stop.get("Text")
            break 
    else:
        print("Matching Stops not found")
        print("Stops:"+stopName+" "+"Does not exist")
        print("To get the list of avaliable stops in this route Enter:Stops\nTo quit enter:Q")
        condCheck=input().lower()
        if condCheck == "" or condCheck == "Q" or condCheck == "q":
            sys.exit()
        elif "stops" in condCheck:
            for i in stops:
                print(i.get("Text"))
            print("Thank you!!!Please Try Again")
            sys.exit()
        else:
            print("Please try again with valid Inputs")
    if not stopCode:
        print("Matching Stops not found")
        print("Stops:"+stopName+" "+"Does not exist")
        print("To get the list of avaliable stops in this route Enter:Stops\nTo quit enter:Q")
        condCheck=input().lower()
        if condCheck == "" or condCheck == "Q" or condCheck == "q":
            sys.exit()
        elif "stops" in condCheck:
            print(stops)
            for i in stops:
                print(i.get("Text"))
            print("See you soon!!!")
            sys.exit()
        else:
            print("Please try again with valid Inputs.See you soon!!!")
            sys.exit()
    get_time()
def get_time():
    ''' Based on the routeNo,direction&stopName
    fetch the next train time avaliable in minutes'''
    urli = f"http://svc.metrotransit.org/NexTrip/{str(routeNo)}/{direction}/{stopCode}"
    headers = {'content-type':'Application/json', 'accept':'Application/json'}

    depart_response = requests.get(url=urli,headers=headers).json()

    #print(depart_response)
    try:
        time_stamp_temp = (depart_response[0].get('DepartureTime'))
        time_stamp_temp= (((int(re.match(r"^(\/Date\()(\d{10})",time_stamp_temp).group(2)) - time.time())/60 ))
        print(f"{round(time_stamp_temp)} Minutes")
    except IndexError:
        print(f"\nLast bus for the day already left from the {stopName}\n")
    
#Start of the program

input_check() # Prepares the input for the program excution




