import requests
from bs4 import BeautifulSoup
import time

class ListInfo:
    def __init__(self, date, title, price, site):
        self._date = date
        self._title = title
        self._price = price
        self._site = site
        self._compare = 0

    def compare(self, average):
        try:
            self._compare = round((float(average) - float(self._price[1:])), 2)
            #this means that most likely this is not something you are looking
            #for because  you are way out of the price range
            if self._compare > 100:
                return False
            return self._compare
        except:
            return False 

    def get_compare(self):
        return self._compare

    def in_range(self, upper_month, upper_day, lower_month, lower_day):
        date = self._date.split()
        return((upper_month == lower_month and date[0] == upper_month and
            int(date[1]) <= int(upper_day) and int(date[1]) >= int(lower_day))or
           ((upper_month != lower_month) and
            (date[0] == upper_month and int(date[1]) <= int(upper_day)) or
            (date[0] == lower_month and int(date[1]) >= int(lower_day))))


    def __lt__(self, other):
        return self._compare < other._compare

    def __eq__(self, other):
        return self._compare == other._compare

    def __str__(self):
        return (self._title + " was posted on " + self._date + " for " +
                self._price + " on " + self._site + " for a total savings of $"
                + str(self._compare))
    
def search_craigs(search, desc):
    link = "https://tucson.craigslist.org/search/sss?query="
    for i in range(len(search)):
        link += (search[i] + '+')
    link += "&sort=rel"
    r = requests.get(link)
    soup = BeautifulSoup(r.text, "html.parser")
    results = soup.find_all("p", attrs = {"class" : "result-info"})
    upper_month, upper_day, lower_month, lower_day = get_date()
    average = get_average(search)
    for m in range(len(results)):
        desc_info = results[m].text.split("\n")
        i = 0
        while i < len(desc_info):
            if desc_info[i] == '':
                desc_info.pop(i)
            else:
                desc_info[i] = desc_info[i].lower()
                i += 1

        info = ListInfo(desc_info[1], desc_info[2], desc_info[3], "craigslist")
        if info.in_range(upper_month, upper_day, lower_month, lower_day):
            check = info.compare(average)
            if check != False:
                desc.append(info)

def search_marketplace(search, desc):
    link = "https://www.facebook.com/marketplace/tucson/search?query="
    for i in range(len(search)-1):
        link += (search[i] + "%20")
    link += search[-1]
    print(link)
    r = requests.get(link)
    soup = BeautifulSoup(r.text, "html.parser")
    results = soup.find_all("a", attrs = {"class" : "1oem"})
    print(len(results))
    for j in range(len(results)):
        print(results[j].text)

def search_offerup(search, desc):
    link = "https://offerup.com/search/?q="
    for i in range(len(search)-1):
        link += (search[i] + "+")
    r = requests.get(link)
    soup = BeautifulSoup(r.text, "html.parser")
    results = soup.find_all("a" ,attrs = {"class":"_109rpto db-item-tile"})
    for i in range(len(results)):
        print(results[i].text)
    print(len(results))

def get_date():
    search_length = 7
    months = [["jan", 31], ["feb", 28], ["mar", 31], ["apr", 30],["may", 31],
              ["jun", 30], ["jul", 31], ["aug", 31], ["sep", 30], ["oct", 31],
              ["nov", 30], ["dec", 31]]
    curr_date = time.strftime("%m/%d/%Y")
    curr_date = curr_date.split("/")
    curr_day = curr_date[1]
    
    if curr_date[0] == "01":
        curr_month = "jan"
    elif curr_date[0] == "02":
        curr_month = "feb"
    elif curr_date[0] == "03":
        curr_month = "mar"
    elif curr_date[0] == "04":
        curr_month = "apr"
    elif curr_date[0] == "05":
        curr_month = "may"
    elif curr_date[0] == "06":
        curr_month = "jun"
    elif curr_date[0] == "07":
        curr_month = "jul"
    elif curr_date[0] == "08":
        curr_month = "aug"
    elif curr_date[0] == "09":
        curr_month = "sep"
    elif curr_date[0] == "10":
        curr_month = "oct"
    elif curr_date[0] == "11":
        curr_month = "nov"
    elif curr_date[0] == "12":
        curr_month = "dec"

    if int(curr_day) - search_length < 1:
        for i in range(len(months)):
            if curr_month == months[i][0] and i != 0:
                search_month = months[i-1][0]
                print(search_month)
                break
            elif curr_month == months[i][0] and i == 0:
                search_month = months[-1][0]
                break
        search_length -= int(curr_day)
        search_day = int(months[i][1]) - search_length
    else:
        search_month = curr_month
        search_day = int(curr_day) - search_length

    if int(curr_day) < 10:
        curr_day = int(curr_day)
        
    return (curr_month, curr_day, search_month, search_day)

def get_average(search):
    average = 0
    link = "https://www.ebay.com/sch/i.html?_from=R40&_nkw="
    for i in range(len(search)):
        link += (search[i] + '+')
    link += "&_sacat=0&rt=nc&LH_Sold=1&LH_Complete=1"
    r = requests.get(link)
    soup = BeautifulSoup(r.text, "html.parser")
    results = soup.find_all("span", attrs = {"class" : "s-item__price"})
    if len(results) < 30:
        length = len(results)
    else:
        length = 30

    for j in range(length):
        average += float(results[j].text[1:])
    average /= length
    average = round(average, 2)
    
    return average


def main():
    search = input("what would you like to shop for? ")
    search = search.lower()
    search = search.split()
    desc = []
    search_craigs(search, desc)
    ##search_marketplace(search, desc)
    desc = sorted(desc)
    #search_offerup(search, desc)
    print("Your top 5 specials are \n")
    for i in range(len(desc) - 1, len(desc) - 6, -1):
        print(desc[i])
        print()
        if i < 0:
            break

main()
    
    
