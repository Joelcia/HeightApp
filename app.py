import sys
from flask import Flask, config, render_template, url_for, send_from_directory,request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from flask_cors import CORS, cross_origin
#from model import db,User,Height
from flask_migrate import Migrate
from validate_email import validate_email
#from mail import mail
from os import name
from flask import Flask
from flask_mail import Mail, Message

#create the Flask instance called app by passing the static files
app = Flask(__name__, static_folder='heightApp/build', static_url_path='')
#initialise flask cors to enable cross-orgin requests in case the api and frontend files are in different servers
CORS(app)
#Access posgresql database
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://mlhdyrvlxqgsat:ec4b79f64daf0795e5fe3503e92aad73666910795155bf9313f30ca14ece3514@ec2-52-19-96-181.eu-west-1.compute.amazonaws.com/d48hkjkid4muhg'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app) #initialise database
migrate = Migrate(app, db)

# configuration of mail
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'sabormnandi@gmail.com'
app.config['MAIL_PASSWORD'] = 'paXnuv-kovgi9-gywxim'
app.config['MAIL_DEFAULT_SENDER']='sabormnandi@gmail.com'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)



#create user models
class User(db.Model):
    __tablename__ = 'user'
 
    userid = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
 
    def __init__(self,name,email):
        self.name = name
        self.email = email
 
    def __repr__(self):
        return f"{self.name}:{self.email}"

#create user models
class Height(db.Model):
    __tablename__ = 'height'
 
    id = db.Column(db.Integer, primary_key = True)
    userid = db.Column(db.Integer, db.ForeignKey('user.userid'))
    height = db.Column(db.Float, nullable=False)
 
    def __init__(self,userid,height):
        self.userid = userid
        self.height = height
 
    def __repr__(self):
        return f"{self.userid}:{self.height}"

#create mail class
class Mail:

    def __init__(self,userName,userEmail,userHeight,averageHeight):
        self.name = userName
        self.email = userEmail
        self.height = userHeight
        self.averageHeight = averageHeight
        self.sender = 'sabormnandi@gmail.com'

    
    def sendMail(self):

        emailBodyTEXT = "Hi "+ self.name +""",


    Your height is : """ + str(round(self.height, 2)) + """cm. 
        

    The average user height is : """ + str(round(self.averageHeight, 2)) + """cm. 
        


    Kind Regards,
    Joelcia
        """
        #message = Message(subject= "Your Height", recipients = [self.email], body= emailBodyTEXT, html = emailBodyHTML,sender= self.sender)
        message = Message("Your Height", recipients = [self.email], sender= self.sender)
        message.body = emailBodyTEXT
        mail.send(message)


#add Post request method listener on the api url to send user input data and map to api and send to DB
@app.route('/api', methods = ['POST'])
@cross_origin() #to allow for cross-origin requests in case the api and frontend files are in different servers
def create_user_height():
    
    invalidInputs = []
    newName = ''
    newEmail = ''
    newHeight = ''

    data = request.get_json() #request data on post method call
    
    ##validate name
    if(data['name'].strip() == '' or len(data['name']) > 100):
        invalidInputs.append('name')
    else:
        newName = data['name'].strip()

     ##validate height
    try:
        if(not int(data['height']) or int(data['height']) <= 0):
            invalidInputs.append('height')
        else:
            newHeight = int(data['height'])
    except ValueError:
        invalidInputs.append('height')

    ##validate email
    if(not validate_email(data['email']) == True or len(data['email']) > 50):
        invalidInputs.append('email')
    else:
        newEmail = data['email'].strip()
    
    
    if(len(invalidInputs) > 0):
        return jsonify({'status':'failed','invalid':invalidInputs})
    else:
        try: 
            #check if email exist
            if db.session.query(User).filter(User.email == newEmail).count() == 0:
                #send name and email to the user DB
                userToSave = User(email=newEmail, name=newName)
                db.session.add(userToSave)
                db.session.commit()

                #send height and matching userid to the heights DB
                heightToSave = Height(userid=userToSave.userid,height=int(newHeight))
                db.session.add(heightToSave)
                db.session.commit()
            
            #update height for repeated email
            elif db.session.query(User).filter(User.email == newEmail).count() == 1:
                userIdToUpdate = User.query.filter_by(email = newEmail).first() #return row at repeated email
                userIdToUpdate.name = newName #update name
                db.session.commit()

                foundUserid = userIdToUpdate.userid #saved userid of repeated email
                heightToUpdate = Height.query.get(foundUserid) #find corresponding height entry
                heightToUpdate.height = int(newHeight) #update height
                db.session.commit()
                #print(heightToUpdate.height, file=sys.stderr)

            #get average user heights
            avgUserHeight = db.session.query(func.avg(Height.height).label('average')).filter(Height.userid==User.userid).first()

            #send email to user with their height and average height
            emailToSend = Mail(userName = newName,userEmail = newEmail, userHeight = newHeight,averageHeight = avgUserHeight.average)
            emailToSend.sendMail()
            #msg = Message('hey there', recipients = [newEmail])
            #mail.send(msg)

            return jsonify({'status':'success'})
            
        except Exception as e:
	        print(str(e))
        
    return jsonify({'status':'failed'})

    #return data #return render_template('file.js')


#serve (display) the react app on the homepage url
@app.route('/')
@cross_origin()
def serve():
    return send_from_directory(app.static_folder, 'index.html')
    #return (app.static_folder, 'index.html')

#run app and debug
if __name__ == "__main__":
    app.run(debug=True)