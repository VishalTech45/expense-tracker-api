from flask_restful import Resource
from flask import request
from flask_jwt_extended import jwt_required , get_jwt_identity
from models  import db, Expense ,User
import os 
from werkzeug.utils import secure_filename
 

class ExpenseList(Resource):

    @jwt_required()
    def get(self):
        #JWT se current user ka id nikalo
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)

        if current_user.role == "admin":
            expenses = Expense.query.all()
        else :
            expenses = Expense.query.filter_by(user_id=current_user_id).all()   
 


        result = []
        for expense in expenses:
             result.append({
                 "id":expense.id,
                 "title":expense.title,
                 "amount":expense.amount,
                 "category":expense.category,
                 "date" : str(expense.date)
             })

        return{"expenses":result} ,200



    @jwt_required()
    def post(self):
        #JWT se current user ka id nikalo
        current_user_id = get_jwt_identity()

        title = request.form.get("title")
        amount = request.form.get("amount")
        category = request.form.get("category") 
        

        #Validation
        if not title or not amount or not category:
            return{"message":"title ,amount and category are required"} ,400
        receipt_path = None 

        if "receipt" in request.files:
            file = request.files["receipt"]
            filename = secure_filename(file.filename)
            upload_folder = "uploads"
            os.makedirs(upload_folder , exist_ok = True)
            file.save(os.path.join(upload_folder,filename))
            receipt_path = filename 


        new_expense = Expense(
            title = title,
            amount = amount,
            category = category,
            user_id = current_user_id ,
            receipt = receipt_path
        )  

        db.session.add(new_expense)
        db.session.commit()

        return {"message" : "Expense   Added !"} ,201
    

class ExpenseDetail(Resource):

    @jwt_required()
    def put(self,expense_id):
        current_user_id = get_jwt_identity()

        # Find Expense 
        expense = Expense.query.filter_by(id=expense_id , user_id = current_user_id).first()


        if not expense:
            return {"message": "Expense not Found !"},404

        data = request.get_json()
        #Jo bhi bheja hai update karo , nahi bheja toh purana rakho

        expense.title = data.get("title",expense.title)
        expense.amount = data.get("amount",expense.amount)
        expense.category = data.get("category",expense.category)


        db.session.commit()
        return {"message":"Expense  Updated "},200

    @jwt_required()
    def delete(self,expense_id):
         current_user_id = get_jwt_identity()

         expense = Expense.query.filter_by(id = expense_id ,user_id= current_user_id).first()

         if not expense:
              return {"message":"Expense  didn't found"},400
         
         db.session.delete(expense)
         db.session.commit()
         return{"message":"Expense deleted"} ,200
         
        
