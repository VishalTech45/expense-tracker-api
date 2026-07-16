from flask_sqlalchemy import SQLAlchemy
from datetime import  datetime ,timezone , timedelta

db =SQLAlchemy() #  db is object  jo database se baat  karta hai . pahle empty banaya hai 

class User(db.Model): # db.model -  yeh class ek database table represent karti hai 
     #db.column - table ka ek column hai  ,primary_key - har user ka unique ID, automatically increment hota hai (1,2,3...)
     id = db.Column(db.Integer ,primary_key = True) 
     username = db.Column(db.String(100) , unique  = True ,nullable = False ) #unique= True - do users ka same username nahi ho sakta  
     password = db.Column(db.String(200),nullable = False ) # nullable = False - yeh field empty nahi ho sakti , required hai 
     role = db.Column(db.String(50) ,nullable=False,default="user")
     email = db.Column(db.String(100), unique=True, nullable=False)
     

    # One-to-Many relationship: ek user ke paas multiple expenses ho sakti hain
    # backref='owner' → expense.owner se us expense ka User object mil jaayega
    # lazy=True → expenses tab hi fetch honge jab user.expenses call karenge
     expenses = db.relationship('Expense', backref='owner',lazy=True)


IST = timezone(timedelta(hours=5 ,minutes=30))

class Expense(db.Model):
      id = db.Column(db.Integer , primary_key = True) 
      title = db.Column(db.String(100), nullable = False )
      amount = db.Column(db.Float , nullable = False)
      category = db.Column(db.String(50),nullable = False)
      receipt =  db.Column(db.String(200) , nullable = True)
      date = db.Column(db.DateTime , default=lambda:datetime.now(IST))  

      # ForeignKey : Store KArta hai hai ki yeh expense kis user ka hai 
      user_id = db.Column(db.Integer, db.ForeignKey('user.id'),nullable=False)


