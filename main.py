import DownloadAttachments
import cumulocityfunctions as cf
import IoTdevice as iot
from time import sleep

# Define Variables
detach_dir = 'C:\\Users\\d725261\\Downloads\\emailattachments'  # location of downloaded attachments
input_dir = detach_dir+'\\'
output_dir = "C:\\Users\\d725261\\Downloads\\trimmed"

server = 'imap.gmail.com'
username = 'diesel.telstra@gmail.com'
password = 'telstra123'

# Create iot device object
diesel = iot.IoTdevice()
CCID = " "

# finished flag to go to sleep
naptime = False

# register&create device if needed
if (diesel.getstatus() != 'OK'):

    # register and create the device on the platform
    cf.registerdevice(diesel)
    cf.createdevice(diesel)
    print("Device exists")

# Always running

while True:

    # Begin loop searching for new emails
    # While there are no new emails, i.e. empty list, connect to the email server and retrieve unread emails
    # Wait a minute before rechecking
    emails = []
    print("Checking Inbox...")
    while not emails:
        # Connect to inbox
        mailbox = DownloadAttachments.connect(server,username,password)

        #Check for unread emails
        emails = DownloadAttachments.fetchunreademails(mailbox)

        if not emails:
            print("\t\t\tNO NEW EMAILS")
            sleep(60)       # sleep 1 minutes



    # If a new email is found, download the data log attachments for those emails
    print("********* New Email Found ************")
    filelist = DownloadAttachments.fetchattachments(mailbox, emails, detach_dir)

    for filename in filelist:
        # If successfully downloaded a data attachment, open and read it, upload measurements
        if (filename==" "):
            print("ERROR:")
            print("No unseen emails with correct attachment")
        else:
            # trim data - remove excess from data file
            file = DownloadAttachments.trimdatafile(input_dir, output_dir, filename)
            # upload measurements
            # load file, for each line, post data
            data_file = open(file)
            data = data_file.readlines()
            for line in data:
                data_array = line.split(',')
                cf.uploadtemperaturetime(diesel, float(data_array[1].strip()), data_array[0])
                sleep(1) # slow down
            naptime = True


    #close mailbox when done
    #DownloadAttachments.close(mailbox)

    #If successful, sleep until next email and restart
    if (naptime):
        print("Nap Time!")
        sleep(14100) # sleep for 3h55m
        naptime = False



