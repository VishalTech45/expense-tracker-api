from flask import Flask 
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_restful import Api
from models import db
from resources.auth import UserRegistration ,UserLogin ,TokenRefresh
from resources.expense import ExpenseList,ExpenseDetail
from datetime import timedelta 
 
app = Flask(__name__)

#Config
app.config["JWT_SECRET_KEY"] = "expense-tracker-secret-key"
app.config["JWT_ACCESS_TOKEN_EXPIRES"]= timedelta(minutes=15)
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=7)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///expense_tracker.db"

# Extensions initialization 
db.init_app(app)
bcrypt =Bcrypt(app)
jwt = JWTManager(app)
api = Api(app)


#Error Handlers
@app.errorhandler(404)
def not_found(e):
    return {"message":'Resource not found'},404

@app.errorhandler(500)
def internal_error(e):
    return{"message":"Internal server error"},500

@app.errorhandler(405)
def method_not_allowed(e):
    return {"message":"Method not allowed"} ,405

#  Creating Database tables 

with app.app_context():
    db.create_all()

#Routes  
api.add_resource(UserRegistration,"/register")
api.add_resource(UserLogin , "/login")
api.add_resource(ExpenseList ,"/expenses")
api.add_resource(ExpenseDetail,"/expenses/<int:expense_id>")
api.add_resource(TokenRefresh ,"/refresh")
 

if __name__ =="__main__":
    app.run(debug=True)    
