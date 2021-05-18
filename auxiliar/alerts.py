
import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
# ================================================================= #
def sendMessage(email, cameraName, qtyPeople):

  # --------------------------------------------------------------- #
  EMAIL_ADDRESS = 'facemaskdetectorservice@gmail.com'
  EMAIL_PWD = 'FMDS@001'
  # --------------------------------------------------------------- #
  mailBox = smtplib.SMTP(host='smtp.gmail.com', port=587)
  mailBox.starttls()
  mailBox.login(EMAIL_ADDRESS, EMAIL_PWD)
  # --------------------------------------------------------------- #
  msg = MIMEMultipart()
  # --------------------------------------------------------------- #
  msg['From'] = EMAIL_ADDRESS
  msg['To'] = email
  msg['Subject'] = 'ALERT: People without mask are detected!'
  # --------------------------------------------------------------- #
  emailDateTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
  message = createMessage(emailDateTime, cameraName, qtyPeople)
  # --------------------------------------------------------------- #
  msg.attach(MIMEText(message, 'html'))
  mailBox.send_message(msg)
  del msg
  mailBox.quit()
  # --------------------------------------------------------------- #

# ================================================================= #
def createMessage(emailDateTime, cameraName, qtyPeople):

  message = """\
              <html>
                <body>
                  <style>
                    table, th, td {
                      border: 1px solid black;
                      border-collapse: collapse;
                    }
                    table {
                      width: 100%;
                      font-size: 15px;
                      font-family: Calibri;
                    }
                    th, td {
                      padding: 10px;
                    }
                    th {
                      color: white;
                      background-color: #005EB8;
                    }
                    .firstTitle {
                      font-size: 20px;
                      font-family: Calibri;
                      font-weight: bold;
                    }
                    .basicText {
                      font-size: 15px;
                      font-family: Calibri;
                    }
                  </style>
                  <div class="firstTitle">Face Mask Detector - Alert</div>
                  <br>
                  <br>
                  <div class="basicText"><b>Execution Date:</b> """ + str(emailDateTime) + """ </div>
                  <br>
                  <div class="basicText">""" + str(qtyPeople) + """ people was identified without mask on camera """ + cameraName + """.</div>
                  <br>
                  <br>
                </body>
              </html>
          """

  return message

# ================================================================= #