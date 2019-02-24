import os
import shutil
import subprocess
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
""" ==========================================
    Author/s: Luke Tan
    Date: 18-12-18
    Last Modified: 18-12-18
    TODO: - Update the global variables below this comment
          - remove the top line of the Ninjas.csv since its just the column headings
          - Update the CertificateTemplate.pdf so that it has the correct date and champions

    HOW IT WORKS: Uses latex to read in a pdf template of the certificate then a shell script to find and replace the
                  name as well as compile.
                  The python script manages the certificates and ninjas using the array index they were read in on, i tried
                  naming the certificate.pdf the ninja's name but that kinda fucked everything up cause some names are tricky.
                  Using the index is easier for validating anyway since you can see any numbers that arent there

    REQUIREMENTS: Python3.6
                  latex installed
                  Calibri font installed - this is a bit of a pain for linux systems so if you want change it in the Template.tex
                  Don't change any filenames btw i hardcoded all of them
                    - Generator.sh - for compiling the latex and doing the name replacement
                    - CertificateTemplate.pdf
                    - Template.tex

    HOW TO USE: Safest way would be to run createCerts() first then sendEmails(), so that you can verify the certificates
                sendEmails() just needs readFile() to run, it can run without createCerts()
    =========================================="""

NINJA_FILE = "Ninjas.csv"
# Index when line is split on comma into array
EMAIL_INDEX = 1
FNAME_INDEX = 2
LNAME_INDEX = 3

email = ''
password = ''
subject = ''
message = ""

""" ==========================================
    Read NINJA_FILE and capitalize any names, stores in global var ninjaArray
    =========================================="""
def readFile():
    index = 0
    with open(NINJA_FILE) as f:
        lines = f.readlines()
        for line in lines:
            lineArray = line.split(",")
            ninja = [lineArray[EMAIL_INDEX], lineArray[FNAME_INDEX].lower().capitalize(), lineArray[LNAME_INDEX].lower().capitalize()]

            #Deals with Capitalizing multi-names
            if " " in ninja[1]:
                fuck = ninja[1].split(" ")
                if len(fuck[1]) > 1 :
                    ninja[1] = fuck[0] + " " +  fuck[1].capitalize()
            if " " in ninja[2]:
                fuck = ninja[2].split(" ")
                if len(fuck[1]) > 1 :
                    ninja[2] = fuck[0] + " " +  fuck[1].capitalize()


            ninjaArray.append(ninja)
            index = index + 1

""" ==========================================
    Creates and stores certificates in Certs directory, name of cert is array index.pdf
    The script to put names on the template is Generator.sh and it uses lualatex
    Creates tmp dir and cleans it up at end of function
    Deletes Certs and tmp directory of they exist before starting, so don't need to worry about cleaning up every time
    =========================================="""
def createCerts():
    certsDir = os.getcwd() + "/Certs"
    tmpDir = os.getcwd() + "/tmp"

    # Delete Certs and tmp directory
    if os.path.isdir(certsDir):
        shutil.rmtree(certsDir)
    if os.path.isdir(tmpDir):
        shutil.rmtree(tmpDir)

    os.mkdir(certsDir)
    os.mkdir(tmpDir)

    #Copy Certificate template into tmp folder
    shutil.copyfile(os.getcwd() + "/CertificateTemplate.pdf", os.getcwd() + "/tmp/CertificateTemplate.pdf")

    scriptPath = os.getcwd() + "/Generator.sh"
    index = 0
    for ninja in ninjaArray:
        subprocess.call([scriptPath, ninja[FNAME_INDEX], ninja[LNAME_INDEX],str(index)])
        index = index + 1

    shutil.rmtree(tmpDir)

""" ==========================================
    Sends the emails, never bothered with error handling so use a test_email before doing the real thing
    =========================================="""
def sendEmails():

    #TODO: test_email = ''

    #set up SMTP connection
    smtpObj = smtplib.SMTP('smtp.gmail.com', 587)
    smtpObj.starttls()

    smtpObj.login(email, password)

    index = 0
    for ninja in ninjaArray:

        file_location = os.getcwd() + '/Certs/' + str(index) + '.pdf'
        index = index + 1

        msg = MIMEMultipart()
        msg['From'] = email
        msg['Subject'] = subject
        msg['To'] = ninja[EMAIL_INDEX]
        #msg['To'] = test_email

        #The magic don't worry about this stuff
        msg.attach(MIMEText(message,'plain'))
        filename = os.path.basename(file_location)
        attatchment = open(file_location, "rb")
        part = MIMEBase('application', 'octet-stream')
        part.set_payload((attatchment).read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', "attatchment; filename= %s" % filename)
        msg.attach(part)
        text = msg.as_string()


        retVal = smtpObj.sendmail(email, ninja[EMAIL_INDEX], text)
        #retVal = smtpObj.sendmail(email, test_email, text)

        #Apparantly the return of .sendmail() is a dictionary containing all the failed emails, couldn't be bothered checking
        if len(retVal) > 0:
            print("idk wtf went wrong" + ':' + ninja[EMAIL_INDEX])


    smtpObj.quit()

# ====================================== MAIN ======================================
ninjaArray = []

readFile()

#Update "constants" index
EMAIL_INDEX = 0
FNAME_INDEX = 1
LNAME_INDEX = 2

createCerts()

#sendEmails()




