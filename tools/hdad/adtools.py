import subprocess

def getinfo(user):

    p = subprocess.Popen(["powershell.exe", "Get-ADUser '%s' -Properties * | Select DisplayName, Title, "
    "Department, departmentNumber, CN, DistinguishedName, EmailAddress, EmployeeNumber, Enabled, Created, "
    "LastLogonDate, logonCount, OfficePhone, PasswordExpired, PasswordLastSet, AccountExpirationDate" % (user)], stdout=subprocess.PIPE)

    info = p.communicate()
    y = str(info).split("\\r\\n")
    return "----- INFO -----\n" + "\n".join(y[2:-4]) + "\n"

def getgroups(user):
    p = subprocess.Popen(["powershell.exe", "Get-ADPrincipalGroupMembership '%s' | select name" % (user)], stdout=subprocess.PIPE)
    info = p.communicate()
    y = str(info).split("\\r\\n")
    return "----- GROUPS -----\n" + "\n".join(y[3:-3]) + "\n"


def unlock(user):
    p = subprocess.Popen(["powershell.exe", "Unlock-ADAccount -Identity '%s'" % (user)], stdout=subprocess.PIPE)
    return "Unlocked user's AD account"

def unexpire(user):
    p = subprocess.Popen(["powershell.exe", "Clear-ADAccountExpiration -Identity '%s'" % (user)], stdout=subprocess.PIPE)
    return "Unexpired user's AD account"

def getinfo_json(user):
        p = subprocess.Popen(["powershell.exe", "Get-ADUser '%s' -Properties * | Select DisplayName, Title, "
        "Department, departmentNumber, CN, DistinguishedName, EmailAddress, EmployeeNumber, Enabled, Created, "
        "LastLogonDate, logonCount, OfficePhone, PasswordExpired, PasswordLastSet, AccountExpirationDate "
        "| ConvertTo-Json" % (user)], stdout=subprocess.PIPE)

        info = p.communicate()
        return str(info)
        # y = str(info).split("\\r\\n")
        # return "----- INFO -----\n" + "\n".join(y[2:-4]) + "\n"
