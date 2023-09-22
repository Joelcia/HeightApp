from os import name
from flask import Flask
from flask_mail import Mail, Message
from app import app


# configuration of mail
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'sabormnandi@gmail.com'
app.config['MAIL_PASSWORD'] = 'paXnuv-kovgi9-gywxim'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)


class Mail:

    def __init__(self,userName,userEmail,userHeight,averageHeight):
        self.name = userName
        self.email = userEmail
        self.height = userHeight
        self.averageHeight = averageHeight
        self.sender = 'sabormnandi@gmail.com'

    
    def sendMail(self):

        emailBodyHTML = "Hi "+ self.name +""",
        <br>
        <br>
        Your current height is : """ + str(round(self.height, 2)) + """cm. <br><br>
        Your average height is : """ + str(round(self.averageHeight, 2)) + """cm. <br><br><br>
        Kind Regards,<br>
        Joelcia
        """
        emailBodyTEXT = "Hi "+ self.name +""",


        Your current height is : """ + str(round(self.height, 2)) + """cm. 
        

        Your average height is : """ + str(round(self.averageHeight, 2)) + """cm. 
        


        Kind Regards,
        Joelcia
        """
        message = Message(subject="Your Height", recipients= self.email, body= emailBodyTEXT, html = emailBodyHTML,sender= self.sender )
        mail.send(message)

