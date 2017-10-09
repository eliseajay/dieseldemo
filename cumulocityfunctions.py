# Functions to interact with the cumulocity platform

############################################################################
import IoTdevice
import requests as HTTP
from time import sleep
import time
from datetime import datetime
import random
import pytz

isdst_now_in = lambda zonename: bool(datetime.now(pytz.timezone(zonename)).dst())


# This function will first register the device on the platform, and will then save the returned data to the
# sysinfo.txt file for future use. To do this it must continuously ping the server with the registraionID.
# Once the device is accepted on the server it will pong back the Username and Password.

# The ping variable is used to control the pinging of the server, once the registration process is complete the
# Ping will be set to false, and the device will stop pinging the server.
def registerdevice(mydevice):
    ping = True

    name = mydevice.getname()
    tenant = mydevice.gettenant()

    print(name)
    print(tenant)

    urlRegistration = "https://" + tenant + ".iot.telstra.com/devicecontrol/deviceCredentials"
    print(urlRegistration)

    # Device registration payload in JSON format. DO NOT COMMENT.
    deviceRegID = {
        "id" : name
    }



    # Registration Loop. This will output to the console the result of each ping and a count to show how long it has
    # been running for.
    counter = 1
    while ping is True:
        # This post is sent to the platform using a special set of credentials provided by Cumulocity. These credentials
        # will only work for this API.
        deviceRegistrationResponse = HTTP.post(urlRegistration, json=deviceRegID,
                                               auth=("management/devicebootstrap", "Fhdt1bb1f"))

        # This will print the server response. 404s will occur whilst the admin has not accepted the new device.
        # 201 will occur once the device is registered.
        httpStatus = deviceRegistrationResponse.status_code
        print(httpStatus)
        print(deviceRegistrationResponse.text)

        # This if/else statement will print the status of the registration. This assists the user as they will be able
        # to see the name of the device that needs to be accepted on the platform.
        if httpStatus == 404:
            print("The Device is still waiting, please accept " + name + " on the platform. (" + str(counter) + ")")
        elif httpStatus == 201:
            print("The Device is registered")
            ping = False # Set ping to false to break the while loop.
        else:
            print("Non expected HTTP response returned")

        if ping is False:
            break

        counter += 1
        # This will stop the while loop from uploading as fast as possible. The user will have a slight delay between
        # HTTP pings.
        sleep(5)

    # Parse request response for device creds. The data variable will be key value pairs, so the keys can be used later.
    data = deviceRegistrationResponse.json()
    print(data)

    # Saving the received username and password to the info.txt file
    mydevice.setusername(data['username'])
    mydevice.setpassword(data['password'])

def checkdevice(mydevice):
    # Checks if device is already created on the platform
    print("## DEVICE CHECK ##")
    # define variables
    tenant = mydevice.gettenant()
    identifier = mydevice.getid()
    serial = mydevice.getserialnumber()
    username = mydevice.getusername()
    password = mydevice.getpassword()
    urlCheckDevice = "https://" + tenant + ".iot.telstra.com/identity/externalIds/c8y_Serial/"+serial
    urlSelf = "https://" + tenant + ".iot.telstra.com/managedObjects/"+identifier

    # Build device payload for device check. This is a JSON payload. (DO NOT COMMENT)
    deviceCheck = {
        "externalId": serial,
        "managedObject": {
            "id": identifier,
            "self": urlSelf
        },
        "self": urlCheckDevice,
        "type": "c8y_Serial"
    }

    # Build device check header. (DO NOT COMMENT)
    deviceHeaders = {
        'content-type': "application/json",
        'accept': "application/json",
    }

    # Post device to be checked to the platform.
    createDeviceResponse = HTTP.post(urlCheckDevice, json=deviceCheck, headers=deviceHeaders,
                                     auth=(username, password))

    # Print to the console the HTTP response code and text.
    print(createDeviceResponse.status_code)
    print(createDeviceResponse.text)

def createdevice(mydevice):
    # This function will define the variables needed, then post the required information to the platform in order
    # to create a device. From there it will interpret the http response to determine the UID of the device on the
    # platform. This will be saved in the info.txt file to reference at a later time.

    # define variables
    tenant = mydevice.gettenant()
    name = mydevice.getname()
    username = mydevice.getusername()
    password = mydevice.getpassword()
    urlCreateDevice = "https://" + tenant + ".iot.telstra.com/inventory/managedObjects"

    # Build device identity payload for device creation. This is a JSON payload. (DO NOT COMMENT)
    deviceIdentity = {
        "name": name,
        "type": "IoT - RPi",
        "c8y_IsDevice": {},
        "c8y_SupportedMeasurements": [
            "c8y_TemperatureMeasurement",
            "c8y_SmokeDensityMeasurement"
        ],
        "c8y_SupportedOperations": [
            "c8y_Restart"
        ],
        "c8y_Hardware": {
            "model": "Raspberry Pi B",
            "revision": "000e",
            "serialNumber": "001"
        }
    }

    # Build device creation header. (DO NOT COMMENT)
    deviceHeaders = {
        'content-type': "application/json",
        'accept': "application/json",
    }

    # Post device to be created to the platform.
    createDeviceResponse = HTTP.post(urlCreateDevice, json=deviceIdentity, headers=deviceHeaders,
                                     auth=(username, password))

    # Print to the console the HTTP response code and text.
    print(createDeviceResponse.status_code)
    print(createDeviceResponse.text)

    # Check response for success, and update device object if successful, otherwise return error
    if (createDeviceResponse.status_code == 201):
        # Save request response containing device ID.
        data = createDeviceResponse.json()

        # Update info.txt
        # Open file and read.
        mydevice.setid(data['id'])
        mydevice.setstatus('OK')
        print("Device created successfully. New ID: " + mydevice.getid())
        print("Device information updated")

    else:
        print("Unexpected Error Occurred")
        print("Status Code: " + str(createDeviceResponse.status_code))
        print("Response Text: " + createDeviceResponse.text)

def uploaddata(mydevice):

    temperature = gettemperature()
    smoke = getsmoke()

    uploadtemperature(mydevice, temperature)
    uploadsmoke(mydevice, smoke)

def gettemperature():
    temperature = random.randint(10,20)
    return temperature

def getsmoke():
    smoke = random.random()
    return smoke

def uploadtemperature(mydevice, temperature):
    urlCreateTemperatureMeasurement = "https://" + mydevice.gettenant() + ".iot.telstra.com/measurement/measurements"

    # Fetch current time
    currentTime = datetime.datetime.now()
    timeFormat = (currentTime.year, "10", currentTime.day,
                  "12", currentTime.minute, currentTime.second, currentTime.microsecond)
    dateTime = "%s-%s-%sT%s:%s:%s.%s+10:00" % timeFormat  # This will produce the Date_Time format required in JSON.

    # Build temperature measurement payload for measurement creation. This is a JSON payload. (DO NOT COMMENT)
    temperatureMeasurement = {
        "c8y_TemperatureMeasurement": {
            "Temperature": {
                "value": temperature,
                "unit": "C"}
        },
        "time": dateTime,
        "source": {
            "id": mydevice.getid()
        },
        "type": "c8y_TemperatureMeasurement"
    }

    # Build temperature creation header. (DO NOT COMMENT)
    temperatureHeader = {
        'content-type': "application/json",
        'accept': "application/json",
    }

    # Post temperature measurement to be created to the platform.
    createTemperatureMeasurementResponse = HTTP.post(urlCreateTemperatureMeasurement, json=temperatureMeasurement
                                                     , headers=temperatureHeader, auth=(mydevice.getusername(), mydevice.getpassword()))

    print(createTemperatureMeasurementResponse.text)

def uploadsmoke(mydevice,smoke):
    urlCreateSmokeMeasurement = "https://" + mydevice.gettenant() + ".iot.telstra.com/measurement/measurements"

    # Fetch current time
    currentTime = datetime.datetime.now()
    timeFormat = (currentTime.year, currentTime.month, currentTime.day,
                  currentTime.hour, currentTime.minute, currentTime.second, currentTime.microsecond)
    dateTime = "%s-%s-%sT%s:%s:%s.%s+10:00" % timeFormat  # This will produce the Date_Time format required in JSON.

    # Build temperature measurement payload for measurement creation. This is a JSON payload. (DO NOT COMMENT)
    smokeMeasurement = {
        "c8y_SmokeDensityMeasurement": {
            "Smoke": {
                "value": smoke,
                "unit": "mg/m3"}
        },
        "time": dateTime,
        "source": {
            "id": mydevice.getid()
        },
        "type": "c8y_SmokeDensityMeasurement"
    }

    # Build temperature creation header. (DO NOT COMMENT)
    smokeHeader = {
        'content-type': "application/json",
        'accept': "application/json",
    }

    # Post temperature measurement to be created to the platform.
    createSmokeMeasurementResponse = HTTP.post(urlCreateSmokeMeasurement, json=smokeMeasurement
                                                     , headers=smokeHeader, auth=(mydevice.getusername(), mydevice.getpassword()))

    print(createSmokeMeasurementResponse.text)

def uploadtemperaturetime(mydevice,temperature,dateTime):
    urlCreateTemperatureMeasurement = "https://" + mydevice.gettenant() + ".iot.telstra.com/measurement/measurements"

    # Edit time
    date, mtime = dateTime.split(" ")
    hour,minute,second = mtime.split(":")
    day,month,year = date.split("/")

    dst = isdst_now_in("Australia/Melbourne")
    if (dst):
        timezone = 11
    else:
        timezone = 10

    if (len(day)<2):
        day = "0"+day
    if (len(month)<2):
        month = "0"+month
    if (len(year)<3):
        year = "20"+year

    timeFormat = (year, month, day,
                  hour, minute, second, "00",timezone)
    dateTime = "%s-%s-%sT%s:%s:%s.%s+%s:00" % timeFormat  # This will produce the Date_Time format required in JSON.

    # Build temperature measurement payload for measurement creation. This is a JSON payload. (DO NOT COMMENT)
    temperatureMeasurement = {
        "c8y_TemperatureMeasurement": {
            "Temperature": {
                "value": temperature,
                "unit": "C"}
        },
        "time": dateTime,
        "source": {
            "id": mydevice.getid()
        },
        "type": "c8y_TemperatureMeasurement"
    }

    # Build temperature creation header. (DO NOT COMMENT)
    temperatureHeader = {
        'content-type': "application/json",
        'accept': "application/json",
    }

    # Post temperature measurement to be created to the platform.
    createTemperatureMeasurementResponse = HTTP.post(urlCreateTemperatureMeasurement, json=temperatureMeasurement
                                                     , headers=temperatureHeader,
                                                     auth=(mydevice.getusername(), mydevice.getpassword()))

    print(createTemperatureMeasurementResponse.text)

