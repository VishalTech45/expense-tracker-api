from flask_restful import Resource
from flask import request 
from  models import db , User
from flask_bcrypt import Bcrypt
from flask_jwt_extended import create_access_token , create_refresh_token ,jwt_required ,get_jwt_identity

bcrypt = Bcrypt()

class UserRegistration(Resource):
     def post(self):
          data = request.get_json()
          username = data.get("username")
          password = data.get("password")
          role= data.get("role","user") # default will be "user"

          #Validation
          if not username or not password:
               return {"message": "Username and password are  Required "} ,400
          
          # Check! username already exists  or not 
          if User.query.filter_by(username=username).first():
               return {"message":"Username already Existed"} ,400
          
          #Password hash karo aur user save karo 
          hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
          new_user = User(username = username,password = hashed_password ,role =role)
          db.session.add(new_user)
          db.session.commit()


          return {"massage":"User  Added in list"} ,201


class UserLogin(Resource):
     def post(self):
          data = request.get_json()
          username = data.get("username")
          password = data.get("password")


          # Find User
          user = User.query.filter_by(username = username).first()

          # Password verification
          if user and bcrypt.check_password_hash(user.password,password):
                access_token  = create_access_token(identity=str(user.id))
                refresh_token = create_refresh_token(identity =str(user.id))
                return {"access_token": access_token,
                        "refresh_token":refresh_token 
                          },200
          return{"message":"Invalid credentials"},401 
     

class TokenRefresh(Resource):
     @jwt_required(refresh = True)
     def post(self):
          current_user_id = get_jwt_identity()
          new_access_token = create_access_token(identity= current_user_id)
          return { "access_token": new_access_token},200      