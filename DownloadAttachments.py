import imaplib
import email
import glob
import os
import time
import operator

def connect(server, username, password):
    # Connect to gmail server, login
    m = imaplib.IMAP4_SSL(server)
    m.login(username, password)
    m.select("INBOX")  # here you a can choose a mail box like INBOX instead
    # use m.list() to get all the mailboxes

    return m

def fetchunreademails(m):
    # This function opens a connection to the gmail server, returns connection and unread emails from inbox
    print("Fetching emails...") # https://stackoverflow.com/questions/10182499/how-do-i-download-only-unread-attachments-from-a-specific-gmail-label

    # Filter through emails to find desired emails
    resp, items = m.search(None, 'UNSEEN') # you could filter using the IMAP rules here (check http://www.example-code.com/csharp/imap-search-critera.asp)
    items = items[0].split()                # getting the mails id

    print("Emails fetched")
    return items

def fetchattachments(m,items,detach_dir):
    # Loop through desired emails to determine if they have attachments and download them to detach_dir if present
    print("Fetching attachments...")

    filearray = [] # output array of filenames

    for emailid in items:
        isdata = False
        resp, data = m.fetch(emailid, "(RFC822)") # fetching the mail, "`(RFC822)`" means "get the whole stuff", but you can ask for headers only, etc
        email_body = data[0][1] # getting the mail content

        mail = email.message_from_bytes(email_body) # parsing the mail content to get a mail object

        #Check if any attachments at all
        if mail.get_content_maintype() != 'multipart':
            continue

        print("["+mail["From"]+"] : " + mail["Subject"])

        # Skip if email is not "Multipar Logged Data"
        if "Multipar Logged Data" not in mail["Subject"]:
            continue

        # we use walk to create a generator so we can iterate on the parts and forget about the recursive headach
        for part in mail.walk():
            # multipart are just containers, so we skip them
            if part.get_content_maintype() == 'multipart':
                continue

            # is this part an attachment ?
            if part.get('Content-Disposition') is None:
                continue

            filename = part.get_filename()
            counter = 1

            # if there is no filename, we create one with a counter to avoid duplicates
            if not filename:
                filename = 'part-%03d%s' % (counter, 'bin')
                counter += 1

            # skip if not a data file
            if "MP_unit_Log_Data" not in filename:
                continue

            att_path = os.path.join(detach_dir, filename)

            #Check if its already there
            if not os.path.isfile(att_path) :
                # finally write the stuff
                print("Saving File")
                isdata = True
                filearray.append(filename)
                print(filearray)
                fp = open(att_path, 'wb')
                fp.write(part.get_payload(decode=True))
                fp.close()

    return filearray


def datafileedit(input_dir,output_dir):
    # This function opens the lates .csv in the detach_dir folder, opens it, and edits the file so only data is left, then saves it as latest_data.csv
    print("Editing data file...")

    ## Sort download dir by creation date and take top .csv's
    list_of_files = glob.glob(input_dir+'*.csv') # * means all if need specific format then *.csv

    list_of_ct = []
    for file in list_of_files:
        list_of_ct.append((os.path.getctime(file)))

    # combine file names & creation time, sort by creation time, take two newest files
    list_of_tuples = zip(list_of_files,list_of_ct)
    list_of_tuples = (list(list_of_tuples))
    sorted_list = (sorted(list_of_tuples, key=operator.itemgetter(1), reverse=True))

    first_file = sorted_list[0]
    second_file = sorted_list[1]


    latest_file_name = max(list_of_files, key=os.path.getctime)
    #print(latest_file_name)

    # Open latest.csv and read in file - assuming its data file - need to adjust to support the alarms file too
    latest_file = open(latest_file_name,'r')
    data = latest_file.readlines()
    latest_file.close()

    # Retrieve only the data into data_only array
    data_only = []
    data_start = 200

    for index,line in enumerate(data):
        text = line[0:4]

        if text == 'Date':
            data_start = index
        if index>data_start:
            data_only.append(line)

    # save the data into new .csv in output_dir
    trimmed_data_file_name = output_dir+"\\latest_data.csv"
    trimmed_data_file = open(trimmed_data_file_name,'w')
    trimmed_data_file.writelines(data_only)
    trimmed_data_file.close()

    return trimmed_data_file_name

    print("Finished edit!")


def getlatestCCID(input_dir):
    # This function opens the lates .csv in the detach_dir folder, opens it, and edits the file so only data is left, then saves it as latest_data.csv
    print("Getting CCID...")

    ## Sort download dir by creation date and take top .csv's
    list_of_files = glob.glob(input_dir + '*.csv')  # * means all if need specific format then *.csv
    latest_file_name = max(list_of_files, key=os.path.getctime)
    print(latest_file_name)

    # Open latest.csv and read in file - assuming its data file - need to adjust to support the alarms file too
    latest_file = open(latest_file_name, 'r')
    data = latest_file.readlines()
    latest_file.close()

    # Retrieve the CCID
    CCID = 'default'
    for index, line in enumerate(data):
        text = line[0:4]

        if text == 'CCID':
            CCID = line[6,:]
            print('CCID Retrieved: '+CCID)

    return CCID

    print("Finished CCID fetch")

def alarmfileedit():
    ## same as above but gets alarm file
    return


def getCCID(dir,filename):
    # Open latest.csv and read in file - assuming its data file - need to adjust to support the alarms file too
    file = open(dir+filename, 'r')
    data = file.readlines()
    file.close()

    # Retrieve the CCID
    CCID = 'default'
    for index, line in enumerate(data):
        text = line[0:4]

        if text == 'CCID':
            CCID = line[6:]
            CCID = CCID.strip()
            print('CCID Retrieved: ' + CCID)

    return CCID

def trimdatafile(input_dir,output_dir,filename):
    # This function opens the .csv in the input_dir folder, opens it, and edits the file so only data is left, then saves it in the output folder
    print("Editing data file...")

    latest_file = open(input_dir+filename, 'r')
    data = latest_file.readlines()
    latest_file.close()

    # Retrieve only the data into data_only array
    data_only = []
    data_start = 200

    for index, line in enumerate(data):
        text = line[0:4]

        if text == 'Date':
            data_start = index
        if index > data_start:
            data_only.append(line)

    # save the data into new .csv in output_dir
    trimmed_data_file_name = output_dir + "\\" + filename
    trimmed_data_file = open(trimmed_data_file_name, 'w')
    trimmed_data_file.writelines(data_only)
    trimmed_data_file.close()

    return trimmed_data_file_name

    print("Finished edit!")

def close(m):
    m.close()

