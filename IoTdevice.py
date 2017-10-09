class IoTdevice:

    def __init__(self):
        print("Fetching Device Variables...")


        try:
            infotxt = open("info.txt", "r")
        except IOError:
            print("ERROR: Could not open info.txt -- " + IOError)

        info = infotxt.readlines()
        infotxt.close()

        for line in info:
            setting = line[0:2]
            #print(setting)
            if setting == 'SN':
                serialNumber = line[10:]
                self.serialNumber = serialNumber.strip()
            elif setting == 'St':
                status = line[10:]
                self.status = status.strip()
            elif setting == 'Te':
                tenant = line[10:]
                self.tenant = tenant.strip()
            elif setting == 'Us':
                username = line[10:]
                self.username = username.strip()
            elif setting == 'Pa':
                password = line[10:]
                self.password = password.strip()
            elif setting == 'Na':
                name = line[10:]
                self.name = name.strip()
            elif setting == 'ID':
                identifier = line[10:]
                self.identifier = identifier.strip()
            else:
                print("Unexpected line in info.txt: " + line)

        print("Fetched!")

        # Write the file to disk.
        sysinfo = open('info.txt', 'w')
        sysinfo.writelines(info)
        sysinfo.close()
        print("The System has been Initialized")




    # GETTERS
    def getserialnumber(self):
        return self.serialNumber

    def getstatus(self):
        return self.status

    def gettenant(self):
        return self.tenant

    def getusername(self):
        return self.username

    def getpassword(self):
        return self.password

    def getname(self):
        return self.name

    def getid(self):
        return self.identifier

    # SETTERS
    def setserialnumber(self, value):
        success = False
        try:
            _infotxt = open("info.txt", "r")
        except IOError:
            print("ERROR: Could not open info.txt -- " + IOError)

        if (not _infotxt.closed):
            _info = _infotxt.readlines()
            _infotxt.close()

        try:
            _infotxt = open("info.txt", "w")
        except IOError:
            print("ERROR: Could not open info.txt -- " + IOError)

        if (not _infotxt.closed):
            self.serialNumber = value
            _info[0] = "SN:        "+value+"\n"
            _infotxt.writelines(_info)
            _infotxt.close()
            success = True

        return success


    def setstatus(self, value):
        success = False
        try:
            _infotxt = open("info.txt", "r")
        except IOError:
            print("ERROR: Could not open info.txt -- " + IOError)

        if (not _infotxt.closed):
            _info = _infotxt.readlines()
            _infotxt.close()

        try:
            _infotxt = open("info.txt", "w")
        except IOError:
            print("ERROR: Could not open info.txt -- " + IOError)

        if (not _infotxt.closed):
            self.status = value
            _info[1] = "Status:    " + value+"\n"
            _infotxt.writelines(_info)
            _infotxt.close()
            success = True

        return success

    def settenant(self, value):
        success = False
        try:
            _infotxt = open("info.txt", "r")
        except IOError:
            print("ERROR: Could not open info.txt -- " + IOError)

        if (not _infotxt.closed):
            _info = _infotxt.readlines()
            _infotxt.close()

        try:
            _infotxt = open("info.txt", "w")
        except IOError:
            print("ERROR: Could not open info.txt -- " + IOError)

        if (not _infotxt.closed):
            self.tenant = value
            _info[2] = "Tenant:    " + value+"\n"
            _infotxt.writelines(_info)
            _infotxt.close()
            success = True

        return success

    def setusername(self, value):
        success = False

        try:
            _infotxt = open("info.txt", "r")
        except IOError:
            print("ERROR: Could not open info.txt -- " + IOError)

        if (not _infotxt.closed):
            _info = _infotxt.readlines()
            _infotxt.close()

        try:
            _infotxt = open("info.txt", "w")
        except IOError:
            print("ERROR: Could not open info.txt -- " + IOError)

        if (not _infotxt.closed):
            self.username = value
            _info[3] = "Username:  " + value +"\n"
            _infotxt.writelines(_info)
            _infotxt.close()
            success = True

        return success

    def setpassword(self, value):
        success = False
        try:
            _infotxt = open("info.txt", "r")
        except IOError:
            print("ERROR: Could not open info.txt -- " + IOError)

        if (not _infotxt.closed):
            _info = _infotxt.readlines()
            _infotxt.close()

        try:
            _infotxt = open("info.txt", "w")
        except IOError:
            print("ERROR: Could not open info.txt -- " + IOError)

        if (not _infotxt.closed):
            self.password = value
            _info[4] = "Password:  " + value+"\n"
            _infotxt.writelines(_info)
            _infotxt.close()
            success = True

        return success

    def setname(self, value):
        success = False
        try:
            _infotxt = open("info.txt", "r")
        except IOError:
            print("ERROR: Could not open info.txt -- " + IOError)

        if (not _infotxt.closed):
            _info = _infotxt.readlines()
            _infotxt.close()

        try:
            _infotxt = open("info.txt", "w")
        except IOError:
            print("ERROR: Could not open info.txt -- " + IOError)

        if (not _infotxt.closed):
            self.name = value
            _info[5] = "Name:      " + value+"\n"
            _infotxt.writelines(_info)
            _infotxt.close()
            success = True

        return success

    def setid(self, value):
        success = False
        try:
            _infotxt = open("info.txt", "r")
        except IOError:
            print("ERROR: Could not open info.txt -- " + IOError)

        if (not _infotxt.closed):
            _info = _infotxt.readlines()
            _infotxt.close()

        try:
            _infotxt = open("info.txt", "w")
        except IOError:
            print("ERROR: Could not open info.txt -- " + IOError)

        if (not _infotxt.closed):
            self.identifier = value
            _info[6] = "ID:        " + value+"\n"
            _infotxt.writelines(_info)
            _infotxt.close()
            success = True

        return success

