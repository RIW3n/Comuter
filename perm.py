import requests
from bs4 import BeautifulSoup
import time
from itertools import permutations

days_of_week = ["monday","tuesday","wednesday","thursday","friday","saturday","sunday"]* 100

headers = {
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"}
def fromto(start_time,day,dep,arr):
    start_time12 = int(start_time.split(' hrs')[0])
    lastzero=False
    if str(start_time12)[-1]=='0':
        lastzero=True
    if start_time12<=100:
        start_time12 = str(12+round(start_time12/100,2))+'am'*(not lastzero) + '0am'*(lastzero)
    elif start_time12<=1200:
        start_time12 = str(round(start_time12/100,2))+'am'*(not lastzero) + '0am'*(lastzero)
    else:
        start_time12 = str(round((start_time12-1200)/100,2))+'pm'*(not lastzero) + '0pm'*(lastzero)
    print(f'time from {dep} to {arr} on {day} {start_time12}')
        
    response2 = requests.get("https://www.google.com/search?",
                            params={'q': f'time from {dep} to {arr} on {day} {start_time12}'}, headers=headers)
    DAY,HR,MIN,SEC = 0,0,0,0
    #print(response2.status_code)
    # print(response2.text)
    if response2.status_code == 200:
        soup = BeautifulSoup(response2.text, 'html.parser')
        search_results = soup.find("span", class_="UdvAnf")
        # search_results2 = soup.find_all("span", class_="iQIYjb")[0].text
        

        if search_results:
            travel_time = search_results.text
            
            if travel_time.split('day')[0].split()[-1].isdigit():
                DAY = int(travel_time.split('day')[0].split()[-1])
            if travel_time.split('hr')[0].split()[-1].isdigit():
                HR = int(travel_time.split('hr')[0].split()[-1])
            if travel_time.split('min')[0].split()[-1].isdigit():
                MIN = int(travel_time.split('min')[0].split()[-1])
            if travel_time.split('sec')[0].split()[-1].isdigit():
                SEC = int(travel_time.split('sec')[0].split()[-1])
    return ((SEC/60)+(MIN)+(HR*60)+(DAY*24*60))


dep = input('enter departure point: ')
the_list = input('enter all intermediate destinations with comma between them: ')
final_arr = input('enter final destination point: ')
day = input('enter the day of departure: ')
start_time_original = input('enter the time of departure: ')
the_list = the_list.split(",")

perms = list(permutations(the_list))
DUR = []
ARRANGEMENT = []
for i in range(len(perms)):
    dep_dep = dep
    perms_perms = perms[i]+(final_arr,)
    dur = 0
    start_time = start_time_original
    for arr in perms_perms:
        time_time = fromto(start_time + " hrs",day,dep_dep,arr)
        time.sleep(1)
        
        dur += time_time
        dep_dep = arr

        if int(time_time)<60:
            aaaahrs = 0
            aaaamins = int(time_time) % 60
        else:
            aaaahrs = int(time_time)//60
            aaaamins = int(time_time) % 60

        #bbbbhrs = int(start_time[0:2])
        if len(start_time)<=2:
            bbbbhrs = 0
        elif len(start_time)<=3:
            bbbbhrs = int(start_time[0:1])
        else:
            bbbbhrs = int(start_time[0:2])
        


        
        bbbbmins = int(start_time[-2])

        ccccmins = aaaamins+bbbbmins

        if int(ccccmins)<60:
            ddddhrs = 0
            ddddmins = int(ccccmins)
        else:
            ddddhrs = int(ccccmins)//60
            ddddmins = int(ccccmins) % 60

        

        aaaa = int( str(aaaahrs+bbbbhrs+ddddhrs) +str('0'*(ddddmins<10))  +str(ddddmins)    )

        
        start_time = str(aaaa)
        #print(start_time)
        if int(start_time) > 2359:
            diff = int(start_time)- 2400
            start_time = str(diff)
            day = [days_of_week [i + (diff//24)] for i in range(7) if day.lower() in days_of_week[i].lower()][0]
        time.sleep(5)
    DUR.append(dur)
    ARRANGEMENT.append((dep,)+perms_perms)

best_plan = [ARRANGEMENT[i] for i in range(len(ARRANGEMENT)) if DUR[i] == min(DUR)][0]

print(best_plan)
print(min(DUR))
