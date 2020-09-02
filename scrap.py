import requests,csv,os,subprocess
from datetime import datetime,timedelta
from bs4 import BeautifulSoup


url = "https://www.worldometers.info/coronavirus/"
r = requests.get(url)
#print (r.content)
soup = BeautifulSoup(r.content,'html5lib')
#print(soup.prettify())

table = soup.find("table",attrs = {'id':'main_table_countries_today'})
tableYesterday = soup.find("table",attrs = {'id':'main_table_countries_yesterday'})
header = {}
th = table.findAll("thead")[0].findAll("tr")[0].findAll("th")
tbody = table.findAll("tbody")

tbodyYesterday = tableYesterday.findAll("tbody")

#get table header
i=0
while i < len(th):
    header[th[i].text] = th[i].text
    i=i+1


def getFileName(day):
    if(day == 'today'):
        date_time_obj = str(datetime.today())[:10]
    else:#yesterday
        date_time_obj = str(datetime.today() - timedelta(days = 1))[:10]
    dateArr = date_time_obj.split("-")
    newDate = dateArr[1]+"-"+dateArr[2]+"-"+dateArr[0]

    return newDate

def getBodyContent(arr):
    contents = []
    for tbody in arr:
        for tr in tbody.findAll("tr"):
            td = tr.findAll("td")
            body = {}
            i=0
            while i < len(td):
                body[th[i].text] = td[i].text.replace("\n","").replace("\n","").replace(" ","")
                i=i+1
            
            contents.append(body)
    return contents
fileContent = []
#csv file to save content in

file = "data/"+getFileName('today')+'.csv'
fileYesterday = "data/"+getFileName('yesterday')+'.csv'


covidData = getBodyContent(tbody)
covidDataYesterday = getBodyContent(tbodyYesterday)
#covidData.insert(0, header)

with open(file,'w') as f:
    w = csv.DictWriter(f,header)
    w.writeheader()
    for row in covidData:
        w.writerow(row)


with open(fileYesterday,'w') as f:
    w = csv.DictWriter(f,header)
    w.writeheader()
    for row in covidDataYesterday:
        w.writerow(row)

#upload file to server
# os.system("cp "+file+" ~/Documents")
# os.system("cp "+fileYesterday+" ~/Documents")
os.system("scp "+file+" user@domain:public_html/path/"+file)

#sts = os.waitpid(p.pid, 0)
