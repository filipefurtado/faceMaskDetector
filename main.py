from tkinter import *
from tkinter import messagebox
from source import detect_mask_video
from db_config import Database
import os
import re
# ================================================================= #
global root
global keyID
# ================================================================= #
keyID = "698dc19d489c4e4db73e28a713eab07b"
# ================================================================= #
def disable_event():
  pass
# ================================================================= #
def openFaceDetection():
  global root
  userData = getUserData()
  detect_mask_video.startFaceDetection(root, userData)
  root.deiconify()
# ================================================================= #
def optionsWindow():

  userData = getUserData()

  options = Toplevel()
  options.title("Options")
  options.geometry("400x400")
  options.configure(background='#feffcc')
  options.protocol("WM_DELETE_WINDOW", disable_event)
  # --------------------------------------------------------------- #
  title = Label(options, text="Options", font=("Courier", 26))
  title.place(relx=0.5, rely=0.15, anchor = 'center')
  title.configure(background='#feffcc')
  # --------------------------------------------------------------- #
  CameraNameLabel = Label(options, text="Camera Name", font=("Courier", 14))
  CameraNameLabel.place(relx=0.20, rely=0.35, anchor = 'center')
  CameraNameLabel.configure(background='#feffcc')
  CameraName = Entry(options)
  CameraName.place(width=200, relx=0.70, rely=0.35, anchor = 'center')

  if userData != {}:
    CameraName.insert(0, userData['cameraName'])
  # --------------------------------------------------------------- #
  EmailAlertLabel = Label(options, text="Email", font=("Courier", 14))
  EmailAlertLabel.place(relx=0.20, rely=0.45, anchor = 'center')
  EmailAlertLabel.configure(background='#feffcc')
  EmailAlert = Entry(options)
  EmailAlert.place(width=200, relx=0.70, rely=0.45, anchor = 'center')

  if userData != {}:
    EmailAlert.insert(0, userData['emailUser'])
  # --------------------------------------------------------------- #
  AlertTimeLabel = Label(options, text="Send alert every", font=("Courier", 14))
  AlertTimeLabel.place(relx=0.20, rely=0.55, anchor = 'center')
  AlertTimeLabel.configure(background='#feffcc')
  AlertTimeOption = StringVar(options)

  if userData != {}:
    if userData['alertTime'] == 1:
      AlertTimeOption.set("5 minutes")
    elif userData['alertTime'] == 2:
      AlertTimeOption.set("10 minutes")
    elif userData['alertTime'] == 3:
      AlertTimeOption.set("15 minutes")
    elif userData['alertTime'] == 4:
      AlertTimeOption.set("30 minutes")
    elif userData['alertTime'] == 5:
      AlertTimeOption.set("50 minutes")
  else:
    AlertTimeOption.set("5 minutes")
    
  AlertTime = OptionMenu(options, AlertTimeOption, "5 minutes", "10 minutes", "15 minutes", "30 minutes", "60 minutes")
  AlertTime.place(width=200, relx=0.70, rely=0.55, anchor = 'center')
  AlertTime.configure(background='#feffcc')
  # --------------------------------------------------------------- #
  ActivateAlertLabel = Label(options, text="Activate Alert", font=("Courier", 14))
  ActivateAlertLabel.place(relx=0.20, rely=0.65, anchor = 'center')
  ActivateAlertLabel.configure(background='#feffcc')
  ActivateAlertOption = IntVar()

  if userData != {}:
    ActivateAlertOption.set(int(userData['alertStatus']))
  else:
    ActivateAlertOption.set(0)

  ActivateAlert = Checkbutton(options, variable=ActivateAlertOption, onvalue=1, offvalue=0)
  ActivateAlert.place(relx=0.70, rely=0.65, anchor = 'center')
  ActivateAlert.configure(background='#feffcc')
  # --------------------------------------------------------------- #
  saveButton = Button(options, text='Save', borderwidth=0, command=lambda: saveData(CameraName, EmailAlert, AlertTimeOption, ActivateAlertOption))
  saveButton.place(relx=0.4, rely=0.85, anchor = 'center')
  # --------------------------------------------------------------- #
  backButton = Button(options, text='Back', borderwidth=0, command=options.destroy)
  backButton.place(relx=0.6, rely=0.85, anchor = 'center')
# ================================================================= #
def mainWindow():
  global root
  
  root = Tk()
  heightScreen = root.winfo_screenwidth()
  widthScreen = root.winfo_screenheight()

  root.title("Face Mask Detector - Version 1.0")
  root.geometry(str(heightScreen) + 'x' + str(widthScreen))
  root.configure(background='#feffcc')
  root.protocol("WM_DELETE_WINDOW", disable_event)

  background_image=PhotoImage(file=os.path.join(os.path.dirname(__file__), 'images', "imageBackground.png"))
  background_label=Label(root, image=background_image)
  background_label.place(x=0, y=0, relwidth=1.6, relheight=1)
  background_label.configure(background='#feffcc')

  title = Label(root, text="Face Mask Detector", font=("Courier", 44))
  title.place(relx = 0.5, rely = 0.2, anchor = 'center')
  title.configure(background='#feffcc')

  startButtonImage = PhotoImage(file=os.path.join(os.path.dirname(__file__), 'images', 'openMaskDetector_md.png'))
  startButton = Button(root, text='Open Mask Detector', image=startButtonImage, borderwidth=0, command=openFaceDetection)
  startButton.place(relx=0.20, rely=0.50, anchor='center')

  startLabel = Label(root, text="Open Mask Detector", font=("Courier", 16))
  startLabel.place(relx = 0.20, rely = 0.75, anchor = 'center')
  startLabel.configure(background='#feffcc')

  optionsButtonImage = PhotoImage(file=os.path.join(os.path.dirname(__file__), 'images', 'settings_md.png'))
  optionsButton = Button(root, text='Options', image=optionsButtonImage, borderwidth=0, command=optionsWindow)
  optionsButton.place(relx=0.45, rely=0.50, anchor = 'center')

  optionsLabel = Label(root, text="Options", font=("Courier", 16))
  optionsLabel.place(relx = 0.45, rely = 0.75, anchor = 'center')
  optionsLabel.configure(background='#feffcc')

  exitButtonImage = PhotoImage(file=os.path.join(os.path.dirname(__file__), 'images', 'exit_md.png'))
  exitButton = Button(root, text='Exit', image=exitButtonImage, borderwidth=0, command=root.destroy)
  exitButton.place(relx=0.80, rely=0.825, anchor = 'center')

  exitLabel = Label(root, text="Exit", font=("Courier", 16))
  exitLabel.place(relx = 0.80, rely = 0.925, anchor = 'center')
  exitLabel.configure(background='#feffcc')

  root.mainloop()

# ================================================================= #
def checkKeyID():
  global keyID

  sSQL = """SELECT STATUS FROM USER_KEYS WHERE USER_KEY=%s"""

  try:
    db = Database().connection
    cursor = db.cursor()
    cursor.execute(sSQL, (keyID, ))
    statusKey = cursor.fetchall()[0][0]
    cursor.close()
    db.close()
  except Exception:
    return False

  return statusKey

# ================================================================= #
def validateEmail(email):

  # --------------------------------------------------------------- #
  regex = '^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$'
  # --------------------------------------------------------------- #
  if(re.search(regex, email)):
    return True
  else:
    return False
  # --------------------------------------------------------------- #

# ================================================================= #
def getUserData():

  global keyID

  sSQL = """SELECT CAMERA_NAME, EMAIL_USER, ALERT_TIME, ALERT_STATUS 
            FROM USER_CONFIG
            WHERE FK_KEY_ID=(SELECT ID FROM USER_KEYS WHERE USER_KEY=%s)"""

  try:
    db = Database().connection
    cursor = db.cursor()
    cursor.execute(sSQL, (keyID,))
    optionsData = cursor.fetchall()
    cursor.close()
    db.close()

    userData = {}
    userData['cameraName'] = optionsData[0][0]
    userData['emailUser'] = optionsData[0][1]
    userData['alertTime'] = optionsData[0][2]
    userData['alertStatus'] = optionsData[0][3]

    return userData

  except Exception:
    return {}

# ================================================================= #
def saveData(CameraName, EmailAlert, AlertTime, ActivateAlert):

  global keyID

  alertTimeOptions = {'5 minutes':1, '10 minutes':2, '15 minutes':3, '30 minutes':4, '60 minutes':5}

  cameraName = CameraName.get()
  email = EmailAlert.get()
  alertTime = alertTimeOptions[AlertTime.get()]
  activateAlert = ActivateAlert.get()

  if validateEmail(email) == False:
    messagebox.showerror(title="Email invalid", message="Please inform a valid email before continue!")
    return False

  if cameraName == '':
    messagebox.showerror(title="Camera Name invalid", message="Please inform a camera name before continue!")
    return False

  sSQL = """INSERT INTO USER_CONFIG (FK_KEY_ID, CAMERA_NAME, EMAIL_USER, ALERT_TIME, ALERT_STATUS)
            VALUES ((SELECT ID FROM USER_KEYS WHERE USER_KEY=%s), %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE CAMERA_NAME=%s, EMAIL_USER=%s, ALERT_TIME=%s, ALERT_STATUS=%s"""

  try:
    db = Database().connection
    cursor = db.cursor()
    cursor.execute(sSQL, (keyID, cameraName, email, alertTime, activateAlert, cameraName, email, alertTime, activateAlert))
    db.commit()
    cursor.close()
    db.close()
  except Exception:
    messagebox.showerror(title="Error", message="Something goes wrong. Please try again!")
    return False

  messagebox.showinfo(title="Success", message="Data saved!")
  return True

# ================================================================= #
def main():

  if checkKeyID():
    mainWindow()
  else:
    messagebox.showerror(title="Key ID invalid", message="The Key ID registered is invalid.")

# ================================================================= #
main()