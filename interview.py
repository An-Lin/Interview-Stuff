import requests
import json
import MySQLdb



#connect to db
conn = MySQLdb.connect(host= "localhost",
                  user="root",
                  passwd="newpassword",
                  db="engy1")
x = conn.cursor()
#-----------------------------------------------------------------------------


userInput = raw_input("Please enter something to search on google: ")
print "The following are the 20 top result "
print " "

# Create a 3 dimenstional array [index][url][title]
Matrix = [[0 for x in range(3)] for x in range(20)] 

#query for 20 result 
query1 = userInput+"&rsz=8"
query2 = userInput+"&rsz=8&start=8"
query3 = userInput+"&rsz=4&start=15"
r1 = requests.get('http://ajax.googleapis.com/ajax/services/search/web?v=1.0&q=' + query1)
r2 = requests.get('http://ajax.googleapis.com/ajax/services/search/web?v=1.0&q=' + query2)
r3 = requests.get('http://ajax.googleapis.com/ajax/services/search/web?v=1.0&q=' + query3)
#-----------------------------------------------------------------------------

#Read the data and also store the information into array to later insert into db
theJson = r1.content
theObject = json.loads(theJson)
for index,result in enumerate(theObject['responseData']['results']):
    print str(index+1) + ") " + result['titleNoFormatting']
    print result['url']
    Matrix[index][0] = index+1
    Matrix[index][1] = result['url']
    Matrix[index][2] = result['titleNoFormatting']

theJson = r2.content
theObject = json.loads(theJson)
for index,result in enumerate(theObject['responseData']['results']):
    print str(index+1+8) + ") " + result['titleNoFormatting']
    print result['url']
    Matrix[index+8][0] = index+1+8
    Matrix[index+8][1] = result['url']
    Matrix[index+8][2] = result['titleNoFormatting']

theJson = r3.content
theObject = json.loads(theJson)
for index,result in enumerate(theObject['responseData']['results']):
    print str(index+1+16) + ") " + result['titleNoFormatting']
    print result['url']
    Matrix[index+16][0] = index+1+16
    Matrix[index+16][1] = result['url']
    Matrix[index+16][2] = result['titleNoFormatting']
#-----------------------------------------------------------------------------

conn.close()

#Display what is going to be save into the db
for x in range(0, 20):
	print Matrix[x][0]
	print Matrix[x][1]
	print Matrix[x][2]
    try:
        x.execute("""INSERT INTO interview VALUES (%s,%s,%s)""",(Matrix[x][0],Matrix[x][1],Matrix[x][2]))
        conn.commit()
    except:
        conn.rollback()

conn.close()

