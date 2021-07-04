import csv
from random import randrange
from datetime import datetime, timedelta
import pandas as pd
from sqlalchemy import create_engine
import pymysql

currentTime = datetime.now()
zeroTime = currentTime - timedelta(hours = 2, minutes = 50)


with open ('sample.csv', 'w', newline = '\n', encoding="utf-8") as file:
    writer = csv.writer(file, delimiter=",")
    writer.writerow(["S_No", "order_id","user", "productId",
    "productName","brand","zone","state","city","store","machine",
    "isVeg","MinWeight","Weight","MaxWeight","weightCheckRequired",
    "weightSimulated","MinTemp","Temp","MaxTemp","tempCheckRequired",
    "tempSimulated","foodImage","foodImageSimulated","faceImage",
    "faceImageSimulated","date","date_no","month_no","week_day",
    "week_no","year","orderRecievedAt","timeTaken","passed","failed",
    "interval"])
    tot_days = 100
    entriesPerDay = 100
    tot_records = entriesPerDay*tot_days
    all_records = []
    S_No = 0
    currentTime = zeroTime
    
    for i in range(1, tot_days+1):
         
        for j in range(100):
            current_record = []
            S_No += 0
            currentTime += timedelta(minutes = randrange(1440//entriesPerDay))

            current_record.append(S_No)
            order_id = 10011000+S_No
            current_record.append(order_id)
            user = randrange(10)+1
            
            current_record.append(user)
            productId = 68450+randrange(10)
            current_record.append(productId)
            productName = "\'Subz-E-Falafel Biryani (Regular)\'"
            current_record.append(productName)
            brand = randrange(12)+1
            current_record.append(brand)
            zone = randrange(4)+1
            current_record.append(zone)
            state = zone + randrange(2)*4
            #state = randrange(4)+1
            current_record.append(state)
            city = state
            #city = randrange(4)+1
            current_record.append(city)
            store = city
            #store = randrange(4)+1
            current_record.append(store)
            machine = randrange(4)+1
            current_record.append(machine)
            isVeg = randrange(2)
            current_record.append(isVeg)
            MinWeight = randrange(50, 250, 5)
            current_record.append(MinWeight)
            Weight = randrange(30, 1000, 5)
            current_record.append(Weight)
            MaxWeight = randrange(300, 900, 5)
            current_record.append(MaxWeight)
            weightCheckRequired = 1
            current_record.append(weightCheckRequired)
            weightSimulated = 0
            current_record.append(weightSimulated)
            MinTemp = randrange(20, 40, 2)
            current_record.append(MinTemp)
            Temp = randrange(10, 100, 2)
            current_record.append(Temp)
            MaxTemp = randrange(50, 90, 2)
            current_record.append(MaxTemp)
            tempCheckRequired = 1
            current_record.append(tempCheckRequired)
            tempSimulated = 0
            current_record.append(tempSimulated)
            foodImage = "https://rebel-sqc-data.s3-ap-south-1.amazonaws.com/liveqcdata/11/11_01/Subz-E-Falafel_Biryani_(Regular)_"+currentTime.strftime("%H:%M:%S")+".png"
            current_record.append(foodImage)
            foodImageSimulated = 0
            current_record.append(foodImageSimulated)
            faceImage = ""
            current_record.append(faceImage)
            faceImageSimulated = 0
            current_record.append(faceImageSimulated)
            date = currentTime.date()
            current_record.append(date)    
            date_no = currentTime.day
            current_record.append(date_no)
            month_no = currentTime.month
            current_record.append(month_no)
            week_day = currentTime.weekday()
            current_record.append(week_day)
            week_no = currentTime.isocalendar()[1]
            current_record.append(week_no)
            year = currentTime.isocalendar()[0]
            current_record.append(year)
            orderRecievedAt = currentTime
            current_record.append(orderRecievedAt)
            timeTaken = 10
            current_record.append(timeTaken)
            if Temp <= MaxTemp and Temp >= MinTemp and Weight <= MaxWeight and Weight >= MinWeight: 
                passed = 1
                failed = 0
            else:
                passed = 0
                failed = 1 
            current_record.append(passed)
            current_record.append(failed)
            
            interval = currentTime.hour*4
            interval += currentTime.minute//15
            current_record.append(interval)

            all_records.append(current_record)
    
    for record in all_records:
        writer.writerow(record)
    print(f"Data created for {tot_days}")

sampleDB = pd.read_csv('sample.csv')

engine=create_engine('mysql+mysqlconnector://root:root@localhost:3306/kms', connect_args={'auth_plugin':'mysql_native_password'}, echo=True)
dbConnection = engine.connect()
print("Opened Connection!")

try:
    frame = sampleDB.to_sql("dashboard", dbConnection, if_exists = 'replace')

except ValueError as vx:
    print(vx)

except Exception as ex:
    print(ex)

else:
    print("Table created sucessfully")

finally:
    dbConnection.close