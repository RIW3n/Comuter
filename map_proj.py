from flask import Flask, render_template, request, session, redirect, url_for,flash
import os
import csv

app = Flask(__name__)

import requests
from bs4 import BeautifulSoup
import time

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"
}

buses = {
    'bus1J': '08:00 AM',
    'bus2K': '08:30 AM',
    'bus3P': '09:00 AM',
    'bus4k': '09:30 AM',
    'bus5I': '10:00 AM',
    'bus6G': '10:30 AM',
    'bus7J': '11:00 AM',
    'bus8P': '11:30 AM',
    'bus9L': '12:00 PM',
    'bus10Y': '12:30 PM',
    'bus11P': '01:00 PM',
    'bus12N': '01:30 PM',
    'bus13J': '02:00 PM',
    'bus14K': '02:30 PM',
    'bus15L': '03:00 PM',
    'bus16P': '03:30 PM',
    'bus17J': '04:00 PM',
    'bus18J': '04:30 PM',
    'bus19P': '05:00 PM',
    'bus20L': '05:30 PM',
    'bus21K': '06:00 PM',
    'bus22K': '06:30 PM',
    'bus23J': '07:00 PM',
    'bus24K': '07:30 PM',
    'bus25K': '08:00 PM',
    'bus26J': '08:30 PM',
    'bus27P': '09:00 PM',
    'bus28K': '09:30 PM',
    'bus29K': '10:00 PM',
    'bus39K': '10:30 PM',
    'bus49K': '11:00 PM',
    'bus69K': '11:30 PM',
}

bus_stop = [
    "bank bus stop", "7.429849, 3.893174", "church bus stop", "sango bus stop", "7.418358, 3.896350",
    "7.413523, 3.894855", "7.409540, 3.893170", "7.408117, 3.896140", "7.406294, 3.901628", "7.406887, 3.906136",
    "secretariat bus stop", "7.406168, 3.912989", "7.401196, 3.921775", "idiape bus stop", "7.403719, 3.934660",
    "academy bus stop"
]


bus_stop1 = bus_stop[1]
bus_stop2 = bus_stop[2]
bus_stop3 = bus_stop[3]
bus_stop4 = bus_stop[4]
bus_stop5 = bus_stop[5]
bus_stop6 = bus_stop[6]
bus_stop7 = bus_stop[7]
bus_stop8 = bus_stop[8]
bus_stop9 = bus_stop[9]
bus_stop10 = bus_stop[10]
bus_stop11 = bus_stop[11]
bus_stop12 = bus_stop[12]
bus_stop13 = bus_stop[13]
bus_stop14 = bus_stop[14]




@app.route('/', methods=['GET', 'POST'])
def home():
    expected_arrival_time = None
    message = None
    bus_coming = None
    travel_time = None
    bank = None
    
    if request.method == "POST":
        
        
        
        bank1 = request.form.get('dp')
        academy1 = request.form.get('ad')
        day1 = request.form.get('day')
        bank = str(bank1)
        academy = str(academy1)
        day = str(day1)

        def convert_to_24_hour_format(time_str):
            
            parts = time_str.split()
            if len(parts) != 2:
                return None  

            
            hour, meridian = parts[0], parts[1]
            
            if ':' in hour:
                hours, minutes = map(int, hour.split(':'))
            else:
                hours = int(hour)
                minutes = 0  

            
            if meridian.lower() == 'pm' and hours < 12:
                hours += 0
            elif meridian.lower() == 'am' and hours == 12:
                hours = 0



        input_time = request.form.get("time")
        converted_time = convert_to_24_hour_format(input_time)
        # fro_m = input("Enter departure location: ")
        # to = input("Enter arrival destination: ")

        

        if converted_time:
            return f'{hours:02d}:{minutes:02d} {meridian}'
            
            current_time = time.strptime(converted_time, "%I:%M %p")

            next_bus_hour = current_time.tm_hour
            next_bus_minute = 0

            if current_time.tm_min >= 30:
                next_bus_hour += 1
                next_bus_minute = 0
            else:
                next_bus_minute = 30

            formatted_next_bus_time = time.strftime("%I:%M %p", time.struct_time(
                (current_time.tm_year, current_time.tm_mon, current_time.tm_mday, next_bus_hour, next_bus_minute, 0, 0, 0, -1)))

            if current_time.tm_hour < next_bus_hour or (current_time.tm_hour == next_bus_hour and current_time.tm_min < next_bus_minute):
                message = formatted_next_bus_time
            else:
                message = formatted_next_bus_time

            

            bus_coming = None

            for bus, timesi in buses.items():
                if timesi == message:
                    bus_coming = bus
                    break

            if bus_coming is not None:
                print("Bus is available for the provided departure time.\n")
            else:
                print("No bus matches the given time:", message)
        else:
            print('Invalid input')

        response2 = requests.get("https://www.google.com/search?",
                                params={'q': f'time from {bank} to {academy} on {day} {converted_time}'}, headers=headers)

        if response2.status_code == 200:
            soup = BeautifulSoup(response2.text, 'html.parser')
            search_results = soup.find("span", class_="UdvAnf")
            # search_results2 = soup.find_all("span", class_="iQIYjb")[0].text

            if search_results:
                travel_time = search_results.text
                print(f"The Estimated travel time to your destination is {travel_time}.\n\nThe next bus from {bank} to {academy} is {bus_coming}.\n\nIt's scheduled to depart at {message}.\n")

                
                next_bus_time = formatted_next_bus_time

        
        next_bus_time = next_bus_time.replace("AM", "").replace("PM", "")

        
        expected_arrival_time = None
        if travel_time:
            estimated_travel_time_minutes = int(travel_time.split(' ')[0])
            next_bus_hour, next_bus_minute = map(int, next_bus_time.split(':'))
            next_bus_minute += estimated_travel_time_minutes + 5

            
            if next_bus_minute >= 60:
                next_bus_hour += 1
                next_bus_minute -= 60

            
            if next_bus_hour >= 12:
                next_bus_hour -= 12
                meridian = "PM"
            else:
                meridian = "AM"

            expected_arrival_time = f"{next_bus_hour:02d}:{next_bus_minute:02d}" #{meridian}

        if expected_arrival_time:
            print("You are expected to reach your destination", expected_arrival_time)

    return render_template("bus_schedule.html",expected_arrival_time =expected_arrival_time, bus_coming =bus_coming, travel_time = travel_time, message = message, bank = bank)
    

if __name__ == '__main__':
    app.run(debug=True)