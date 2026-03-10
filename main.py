##################### Extra Hard Starting Project ######################

# 1. Update the birthdays.csv

# 2. Check if today matches a birthday in the birthdays.csv
import pandas
import datetime as dt
import smtplib
import os
import random

today = dt.datetime.today()
count = -1

df = pandas.read_csv("birthdays.csv", header=0)
month = df["month"].to_list()
day = df["day"].to_list()
name = df["name"].to_list()
email = df["email"].to_list()

for _ in month:
    count +=1
    print(count)
    if _ == today.month:
        if day[count] == today.day:
            print(f"It's {name[count]}'s birthday!")

# dict = df.to_dict("records")
# print(dict)
# 3. If step 2 is true, pick a random letter from letter templates and replace the [NAME] with the person's actual name from birthdays.csv
            all_letters = os.listdir("letter_templates")

            select = random.choice(all_letters)
            print(select)
            filename = "letter_templates/" + select

            with open(filename,"r") as f:
                template = f.read()
                letter = template.replace("[NAME]",name[count])

            with open(filename,"w") as f:
                f.write(letter)

# 4. Send the letter generated in step 3 to that person's email address.
            sender_email = os.environ.get("sender_email")
            send_pw = os.environ.get("send_pw")
            
            to_email = email[count]
            message = f"Subject: Happy Birthday!!\n\n {letter}"

            with smtplib.SMTP("smtp.gmail.com", 587) as connection:
                # connection = smtplib.SMTP("smtp.gmail.com", port=587)
                connection.starttls()
                connection.login(user="xuyuesheila", password=send_pw)
                connection.sendmail(
                    from_addr=sender_email,
                    to_addrs=to_email,
                    msg=message
                )


