from datetime import datetime
import json
from bs4 import BeautifulSoup
import requests
from dataclasses import dataclass


@dataclass
class Holiday: 
    name: str
    date: datetime.date

    def __str__(self):
        return self.name + " " + str(self.date)


class Calendar:
    def __init__(self):
        self.innerHoliday = []

   
    def addHoliday(self, holidayObj):
        if holidayObj not in self.innerHoliday:
           self.innerHoliday.append(holidayObj)
           print("You've just added " + str(holidayObj))
        else:
            print("That's already in the system.")
            print('\n')
            return

    def findHoliday(self, name, date):
        for i in self.innerHoliday:
            if i.name == name and i.date == date:
                return i

    def removeHoliday(self, name, date):
        holiday_to_remove = self.findHoliday(name, date)
        if holiday_to_remove in self.innerHoliday:
            self.innerHoliday.remove(holiday_to_remove)
            print("You've deleted the holiday.")
            print('\n')
        else:
            print("That holiday is not in the list.")
            print('\n')


    def read_json(self, filelocation):
        with open(filelocation, "r") as f:
            data = json.load(f)
            for i in data["holidays"]:
                dateString = i["date"]
                date_format = datetime.strptime(dateString, "%Y-%m-%d")
                holiday = Holiday(i["name"], date_format)
                self.innerHoliday.append(holiday)
        


    def save_to_json(self, filelocation): 

            data = []
            for i in self.innerHoliday:
                new_list = {}
                if i not in data and new_list:
                    data.append({'name': i.name, 'date': datetime.strftime(i.date, "%Y-%m-%d")})
                new_list.update({'holidays': data})
                with open(filelocation, 'w') as f:
                    json.dump(new_list, f, indent = 4)
        
    def scrapeHolidays(self):
        years = [2020,2021,2022,2023,2024]

        try:

            for year in years:

                page = requests.get(f"https://www.timeanddate.com/calendar/custom.html?country=1&year={year}&hol=9564161")

                soup = BeautifulSoup(page.text, "html.parser")

                table = soup.find('tbody')

                rows = table.find_all('tr')

                row_count = 0

                for item in rows:
                    if not item.find('td', class_='cadjhol small pn'):
                        row_count += 1
                        if row_count > 2:
                            hol_date = item.find('td')
                            holiday_date = f'{hol_date.text}, {year}'
                            formatted_date = datetime.strptime(holiday_date, '%b %d, %Y').date() 
                            hol_name = item.find('a')
                            holiday_name = hol_name.text
                            self.innerHoliday.append(Holiday(holiday_name, formatted_date))            

        except:
            print("The website is currently having issues being reached.")
        
        return self.innerHoliday



    def numHolidays(self):
       
        return len(self.innerHoliday)
    
    def filter_holidays_by_week(self, year, week):

        query = list(filter(lambda x: x.date.isocalendar().year == year and x.date.isocalendar().week == week, self.innerHoliday))
        return query


    def displayHolidaysInWeek(self, year, week):

        chosen_week = self.filter_holidays_by_week(year, week)
        holiday_counter = 0
        if len(chosen_week) == 0:
            print("No holidays this week. We will now go back to the main menu")
            print("============================================================")
            main()
        else: 
            for holiday in chosen_week:
                print(chosen_week[holiday_counter])
                holiday_counter += 1





    def getWeather(self, weekNum):

        url = "https://community-open-weather-map.p.rapidapi.com/forecast"

        querystring = {"q":"minneapolis,us"}

        headers = {
            "X-RapidAPI-Host": "community-open-weather-map.p.rapidapi.com",
            "X-RapidAPI-Key": "297eeab973mshfe84240f74c4444p18c747jsnb7c35ab4b990"
        }

        response = requests.request("GET", url, headers=headers, params=querystring)

        weather = json.loads(response.text)
        #
        print(weather["list"][0])
        counter = 0
        for i in weather['list']:
            if counter % 8 == 0:
                x = i["weather"][0]["description"]
                print(x)
                print(i["dt_txt"])
            counter += 1


    def viewCurrentWeek(self, year, week):

        self.displayHolidaysInWeek(year, week)
        weather_input = input("Would you like do to see the weather for this week as well? [y/n]: ")
        if weather_input == 'y':
            self.getWeather(week)
            
        else:
            main()




def main():

    main_list = Calendar()
    main_list.scrapeHolidays() 
    main_list.read_json('holidays.json')
  
    
    
    while True:
        print("Welcome to the holiday manager.")
        print('\n')
        print(f"There are currently this many holidays in the system: " + str(main_list.numHolidays()))
        print("===============================")
        print("Main Menu:")
        print("________________________________")
        print("1: Add Holiday")
        print("2: Remove Holiday")
        print("3: View Holidays")
        print("4: Save Changes")
        print("5: Exit Program")

        menu_select = input("Please enter a number 1-5 corresponding to the menu: ")

        if menu_select == "1": #Add holiday
            print("You've chosen to add a holiday.")
            holiday_name_input = input("please type the name of your holiday: ")
            holiday_date_input = input("type the date. Ex: yyyy-mm-dd: ")
            if holiday_date_input.isalpha():
                print("That's not a valid input")
            else:
                holidayObj = Holiday(holiday_name_input, holiday_date_input)
                main_list.addHoliday(holidayObj)
            
        elif menu_select == "2": #Remove holiday
            print("Remove Holiday")
            remove_input = input("Please enter the name of the holiday you would like to remove: ")
            date_input = input("Please enter the date of the holiday in this format: yyyy-mm-dd: ")
            main_list.removeHoliday(remove_input, date_input)


        elif menu_select == "3": #View holidays
            print("View Holidays") 
            print("================")
            user_year = input(f"Please pick a year between 2020 - 2024.\n")
            user_week = input("Please pick a week between 1-52. If you hit enter it will select the current week.\n")
            if user_year in [2020,2021,2022,2023] and user_week in range(1,53):
                main_list.displayHolidaysInWeek(int(user_year), int(user_week))
            elif user_week == "":
                user_week = datetime.now().isocalendar()[1]
                main_list.viewCurrentWeek(int(user_year), int(user_week))
            else:
                print("That is not between 2020 and 2024 or the week is not between 1 and 52")
                main()

        elif menu_select == "4": #Save changes to json
            save_input = input("Are you sure you want to save your changes? [y/n]: ")
            if save_input == "y":
                main_list.save_to_json('holidays.json') 
            elif save_input == "n":
                print("You have selected not to save your input. You will return to the main menu.")
                print("============================================================================")
                main()
            else:
                print("That is not a valid input.")
                main()

        elif menu_select == "5":#Exit program
            print("Exit Program")
            break

        else: 
            print("that's not one of the options.")
            main()



main()




