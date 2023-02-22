import os
import sys
import json
import time
import requests

if len(sys.argv) != 3:
    print("Wrong number arguments")
    print("Give one argument representing your campus' city and another your project name.")
    exit()

ACCESS_TOKEN = os.getenv('API42_ACCESS_TOKEN')
CAMPUS = sys.argv[1].lower()
PROJECT = sys.argv[2]

campuses = {
    "brussels":"12",
    "paris":"1,42",
    "khouribga":"16",
    "lyon":"9",
    "seoul":"29",
    "tokyo":"26",
    "moscow":"17",
    "amman":"35",
    "adelaide":"36",
    "malaga":"37",
    "lisboa":"38",
    "heilborn":"39",
    "urduliz":"40",
    "nice":"41",
    "abu dhabi":"43",
    "wolfsburg":"44",
    "alicante":"45",
    "barcelona":"46",
    "lousanne":"47",
    "mulhouse":"48",
    "instanbul":"49",
    "kocaeli":"50",
    "berlin":"51",
    "florence":"52",
    "vienna":"53",
    "tetouan":"55",
    "prague":"56",
    "london":"57",
    "porto":"58",
    "luxembourg":"59",
    "perpignan":"60",
    "sao paulo":"61",
    "havre":"62",
    "antwerp":"63",
    "singapore":"64"
}

if CAMPUS not in campuses.keys():
    print("Your campus named '" + CAMPUS + "' was not found")
    print("Choose between: " + ', '.join(campuses.keys()))
    exit()

def find_slots():
    url = "https://api.intra.42.fr/v2/projects/"+PROJECT+"/slots?filter[campus_id]="+campuses[CAMPUS]+"&future=true&sort=begin_at"    
    header = { "Authorization" : "Bearer " + ACCESS_TOKEN }
    x = requests.get(url, headers = header)
    if x.text == "{}":
        print("Specified project not found.")
        print("See correct project slug with: 'make project_notation'")
        exit()
    try:
        slots = json.loads(x.text)
        return slots
    except:
        print("TOKEN EXPIRED REGENEATE NEW TOKEN WITH: 'make setup'")
        os.system('zenity --warning --text="TOKEN EXPIRED" --no-wrap') #Notify
        exit()

def print_slots(slots):
    print("DAY" + "   " + "TIME")
    for slot in slots:
        day = slot['begin_at'][8:-14]
        hour = int(slot['begin_at'][11:-11])
        hour = 0 if hour == 23 else hour + 1; #Set to Brussels time zone -> Brussels = Z + 1
        min = slot['begin_at'][14:-8]
        print(day + "   " + str(hour) + ":" + min)
    print()
        
while 1:
    slots = find_slots()
    if slots != []:
        print_slots(slots)
        os.system('zenity --warning --text="SLOT FOUND" --no-wrap') #Notify        
        y = input('Do you want to continue (y/n): ')
        if y == "n":
            exit()
    else:
        time.sleep(60);
