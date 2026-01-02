import csv
import json
import random
def get_users_db(email_user):
    with open("db.csv",newline="") as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row["email"] == email_user:
                return row
    return False 


def create_user_db(data):
    with open("db.csv","w",newline="") as file:
        id = random.randint(1, 1000000)
        data["id"] = id
        data["auth"] = "admin"
        writer = csv.DictWriter(file, fieldnames=["id","email", "password", "name","auth"])
        writer.writeheader()
        writer.writerow(data)
    return True

