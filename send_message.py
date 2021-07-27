import json
from twilio.rest import Client

account_sid = "ACc40ea0171e8e286e01a088a435b2850d"  # Twilio Account Sid
auth_token = "879f470ce57abdfd3175d73ca732ffd6" # Twilio Auth Token 

def message(driver, hospital, contact, distance, lat, log):
    
    contact_list = []

    with open("driver_info.json", "r") as read_file:
        data = json.load(read_file)
        name = data[driver][0]["name"]
        age = data[driver][0]["age"]
        health = data[driver][0]["health"]
        relative_no1 = data[driver][0]["relatives"][0]["1"]
        relative_no2 = data[driver][0]["relatives"][0]["2"]
        friend_no1 = data[driver][0]["friend"][0]["1"]
        friend_no2 = data[driver][0]["friend"][0]["2"]

        contact_list = [relative_no2, friend_no2]
        print(contact_list)

        for number in contact_list:
            
            # print(type(number))
            client = Client(account_sid, auth_token)
            message = client.messages.create(
                from_= "+19034965809",
                body = "There has been an accident at http://maps.google.com/?q={},{}  driver: {}, neariest hospital: http://maps.google.com/?q={}".format(lat, log, driver, hospital),
                to= number,
            )
            #print(message.sid)

    ####### Hospital message #########

    client = Client(account_sid, auth_token)
    message = client.messages.create(
        from_= "+19034965809",
        body = "There has been an accident at http://maps.google.com/?q={},{}  patient details : name: {}\
            age: {} medical details: {}, contact_details: {}".format(lat, log, name, age, health, contact_list),
        to= "+918303531702",
    )
    # print(message.sid)