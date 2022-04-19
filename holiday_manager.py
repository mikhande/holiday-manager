from datetime import datetime
import json
from bs4 import BeautifulSoup
import requests
from dataclasses import dataclass

# -------------------------------------------
# Modify the holiday class to 
# 1. Only accept Datetime objects for date.
# 2. You may need to add additional functions
# 3. You may drop the init if you are using @dataclasses
# --------------------------------------------
@dataclass
class Holiday: 
    name: str
    date: datetime.date

    def __str__(self):
        return self.name + " (" + self.date.strftime('%Y-%m-%d') + ")"
    #def __str__ (self):
        # String output
        # Holiday output when printed.
          
# -------------------------------------------
# The HolidayList class acts as a wrapper and container
# For the list of holidays
# Each method has pseudo-code instructions
# --------------------------------------------
class Calendar:
    def __init__(self):
        self.innerHoliday = []

   
    def addHoliday(self, holidayObj):
        print("you're in!")
        if type(holidayObj): #is this ok?
           self.innerHoliday.append(holidayObj)
           print("You've just added " + str(holidayObj))
        else:
            print("That's not a valid input. Try again.")
            return


        # Make sure holidayObj is an Holiday Object by checking the type
        # Use innerHolidays.append(holidayObj) to add holiday
        # print to the user that you added a holiday

    def findHoliday(self, name, date):
        for i in self.innerHoliday:
            if i.__name == name and i.__date == date:
                return i
        # Find Holiday in innerHolidays
        # Return Holiday

    def removeHoliday(self, name, date):
        for i in self.innerHoliday:
            if i.__name == name and i.__date == date:
                self.innerHoliday.remove(i)
                print("You've deleted the holiday.")

        # Find Holiday in innerHolidays by searching the name and date combination.
        # remove the Holiday from innerHolidays
        # inform user you deleted the holiday

    def read_json(self, filelocation):
        with open(filelocation, "r") as f:
            data = json.load(f)
            for i in data["holidays"]:
                dateString = i["date"]
                date_format = datetime.strptime(dateString, "%Y-%m-%d")
                holiday = Holiday(i["name"], date_format)
                self.innerHoliday.append(holiday)
        


    def save_to_json(self, filelocation):
        # Write out json file to selected file.
        with open(filelocation, "w", encoding = 'utf-8') as f:
            data = []
            for i in self.innerHoliday:
                new_list = {}
                data.append({'Name': i.name, 'Date': i.date})
            new_list.update({'Holidays': data})
            json.dump(new_list, f, indent = 4)
        
    def scrapeHolidays(self, year):
        years = [year]

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



        # Scrape Holidays from https://www.timeanddate.com/holidays/us/ 
        # Remember, 2 previous years, current year, and 2  years into the future. You can scrape multiple years by adding year to the timeanddate URL. For example https://www.timeanddate.com/holidays/us/2022
        # Check to see if name and date of holiday is in innerHolidays array
        # Add non-duplicates to innerHolidays
        # Handle any exceptions.     

    def numHolidays(self):
        # Return the total number of holidays in innerHolidays
        return len(self.innerHoliday)
    
    def filter_holidays_by_week(self, year, week):
        query = list(filter(lambda x: x.date.isocalendar().year == year and x.date.isocalendar().week == week, self.innerHoliday))
        return query
        # Use a Lambda function to filter by week number and save this as holidays, use the filter on innerHolidays
        # Week number is part of the the Datetime object
        # Cast filter results as list
        # return your holidays

    def displayHolidaysInWeek(self, year, week):
        # Use your filter_holidays_by_week to get list of holidays within a week as a parameter
        # Output formated holidays in the week. 
        # * Remember to use the holiday __str__ method.

        chosen_week = self.filter_holidays_by_week(year, week)
        holiday_counter = 0
        if len(chosen_week) == 0:
            print("No holidays this week. We will now go back to the main menu")
            print("============================================================")
            main()
        else: 
            for holiday in chosen_week:
                print('\n')
                print(chosen_week[holiday_counter])
                holiday_counter += 1
                print("We will now go back to the main menu.")
                print("=======================================")




    def getWeather(weekNum):

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
        # Convert weekNum to range between two days
        # Use Try / Except to catch problems
        # Query API for weather in that week range
        # Format weather information and return weather string.

    def viewCurrentWeek():
        week = range(0,52)
        # Use the Datetime Module to look up current week and year
        # Use your filter_holidays_by_week function to get the list of holidays 
        # for the current week/year
        # Use your displayHolidaysInWeek function to display the holidays in the week
        # Ask user if they want to get the weather
        # If yes, use your getWeather function and display results
        current_week = datetime.date.today()

    




def main():

    main_list = Calendar()
    # year = (2020,2021,2022,2023,2024)
    # main_list.scrapeHolidays(year) # This isn't working to scrape holidays at beginning
    main_list.read_json('holidays.json')
  
    
    
    


    # Large Pseudo Code steps
    # -------------------------------------
    # 1. Initialize HolidayList Object
    # 2. Load JSON file via HolidayList read_json function
    # 3. Scrape additional holidays using your HolidayList scrapeHolidays function.
    # 3. Create while loop for user to keep adding or working with the Calender
    # 4. Display User Menu (Print the menu)
    # 5. Take user input for their action based on Menu and check the user input for errors
    # 6. Run appropriate method from the HolidayList object depending on what the user input is
    # 7. Ask the User if they would like to Continue, if not, end the while loop, ending the program.  If they do wish to continue, keep the program going. 
    while True:
        
        # main_list = Calendar()
        # main_list.read_json('holidays.json')
        print(f"There are currently this many holidays in the system: {len(main_list.innerHoliday)}")

        print("Welcome to the holiday manager.")
        print("===============================")
        print("Main Menu:")
        print("________________________________")
        print("1: Add Holiday")
        print("2: Remove Holiday")
        print("3: View Holidays")
        print("4: Save Changes")
        print("5: Exit Program")

        menu_select = input("Please enter a number 1-5 corresponding to the menu: ")
        if menu_select == "1":
            print("You've chosen to add a holiday.")
            holiday_name_input = input("please type the name of your holiday: ")
            holiday_date_input = input("type the date. Ex: yyyy-mm-dd: ")
            formatted_date = datetime.strptime(holiday_date_input, '%Y-%m-%d').date()
            holidayObj = Holiday(holiday_name_input, formatted_date)
            main_list.addHoliday(holidayObj)
            
        elif menu_select == "2":
            print("Remove Holiday")

        elif menu_select == "3":
            print("View Holidays") 
            print("================")
            user_year = input(f"Please pick a year between 2020 - 2024.\n")
            user_week = input("Please pick a week between 1-52. If you hit enter it will select the current week.\n")
            user_week = int(user_week)
            if user_year in ['2020', '2021', '2022', '2024'] and user_week in range(1,53):

                holiday_dict = main_list.scrapeHolidays(user_year)
                chosen_holidays = main_list.displayHolidaysInWeek(int(user_year), int(user_week))
            else:
                print("That is not between 2020 and 2024 or the week is not between 1 and 52")
                main()
        elif menu_select == "4":
            print("Save Changes")

        elif menu_select == "5":
            print("Exit Program")

        else: 
            print("that's not one of the options.")
            main()



     

        



        
if __name__ == "__main__":
    main();


# Additional Hints:
# ---------------------------------------------
# You may need additional helper functions both in and out of the classes, add functions as you need to.
#
# No one function should be more then 50 lines of code, if you need more then 50 lines of code
# excluding comments, break the function into multiple functions.
#
# You can store your raw menu text, and other blocks of texts as raw text files 
# and use placeholder values with the format option.
# Example:
# In the file test.txt is "My name is {fname}, I'm {age}"
# Then you later can read the file into a string "filetxt"
# and substitute the placeholders 
# for example: filetxt.format(fname = "John", age = 36)
# This will make your code far more readable, by seperating text from code.








