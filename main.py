import datetime
import requests
import secret
# import telegram_send
url = 'https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByPin'

# Add pincodes for which you want the bot to send alerts
pincodes = [400001, 421301]
today = datetime.date.today()
timern = datetime.datetime.now().strftime("%H")
timern = int(timern)
tomorrow = today + datetime.timedelta(days=1)
tomorrow_date = tomorrow.strftime("%d-%m-%Y")
querydate = today.strftime("%d-%m-%Y")
AcceptLanguage = 'hi_IN'

# Automatically changes date at 6 p.m to search for next day's slots
if timern >= 18:
    querydate = tomorrow_date

for pincode in pincodes:
    params = dict(
        AcceptLanguage=AcceptLanguage,
        pincode=pincode,
        date=querydate,
    )

    reply = requests.get(url=url, params=params)

    if reply.status_code == 200:
        response = reply.json()
        j = 0
        for i in response['sessions']:
            # If you want only Government facilities' alerts, edit line 37 and add "and response['sessions'][j]['fee_type'] != 'Paid'"
            # E.g:
            # if response['sessions'][j]['available_capacity'] != 0 and response['sessions'][j]['fee_type'] != 'Paid'
            if response['sessions'][j]['available_capacity'] != 0:
                message = response['sessions'][j]['name'] + "\n\nAddress: " + str(
                    response['sessions'][j]['address']) + "\nPincode: " + str(
                    response['sessions'][j]['pincode']) + "\nDate: " + response['sessions'][j]['date'] + "\nTime: " + \
                          response['sessions'][j]['from'] + "-" + response['sessions'][j]['to'] + "\nVaccine: " + \
                          response['sessions'][j]['vaccine'] + "\nType: " + response['sessions'][j][
                              'fee_type'] + "\nFee: " + response['sessions'][j]['fee'] + "\nAge Limit: " + str(
                    response['sessions'][j]['min_age_limit']) + "\nAvailable doses: " + str(
                    response['sessions'][j]['available_capacity']) + "\n\t\tDose 1: " + str(
                    response['sessions'][j]['available_capacity_dose1']) + "\n\t\tDose 2: " + str(
                    response['sessions'][j]['available_capacity_dose2'])
                # Uncomment the below line if you want your telegram bot to send you messages personally. You'll have
                # to configure telegram_send first using command: 'telegram-send --configure'
                # telegram_send.send(messages=[message])
                tele_url = 'https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}'.format(secret.api, secret.chat, message)
                resp1 = requests.get(tele_url)
                if resp1.status_code != 200 and resp1.status_code != 429:
                    print("Hey! The script encountered an error with Telegram API. The response code received is: ", requests.get(tele_url).status_code)
            j += 1
    else:
        message = ["Hey! The script encountered an error. The response code received is: ", reply.status_code]
        tele_url = 'https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}'.format(secret.api, secret.chat, message)
        resp1 = requests.get(tele_url)
        # If you want to print the response code in your console, uncomment the below line print(
        # reply.status_code+"\nUh oh! The script encountered an error. Please contact admin with above response code.")
