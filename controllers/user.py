from flask import Blueprint, jsonify, render_template, request, redirect
from connectors.mysql_connector import engine
from models.user import User
from sqlalchemy.orm import sessionmaker
from flask_login import login_user, login_required, logout_user, current_user
from utils.api_response import api_response
from sqlalchemy import func
from flask_jwt_extended import create_access_token

users_routes = Blueprint('users_routes',__name__)

@users_routes.route("/register", methods=['GET'])
def users_register():
    return render_template("user/register.html")

@users_routes.route("/login", methods=['GET'])
def users_login():
    return render_template("user/login.html")

@users_routes.route("/register", methods=['POST'])
def do_registration():

    username = request.form['username']
    email = request.form['email']
    password = request.form['password']
    
    print(f"Username: {username}, Email: {email}, Password Hash: {password}")
    NewUser = User(username=username, email=email)
    NewUser.set_password(password)

    connection = engine.connect()
    Session = sessionmaker(connection)
    session = Session()

    session.begin()
    try:
        session.add(NewUser)
        session.commit()
    except Exception as e:
        print(f"Error during registration: {e}")
        session.rollback()
        return { "message": "Failed to Register" }
    
    return api_response(
            status_code=201,
            message= "New user data has been successfully added",
            data={
                "id": NewUser.id,
                "username": NewUser.username,
                "email": NewUser.email
            }
        )  

@users_routes.route("/login", methods=['POST'])
def do_user_login():
    
    connection = engine.connect()
    Session = sessionmaker(connection)
    session = Session()

    try:
        users = session.query(User).filter(User.email==request.form['email']).first()

        if users == None:
            return {"message" : "Email not registered"}
        

        if not users.check_password(request.form['password']):
            return {"message" : "Password Salah"}

        login_user(users, remember=False)

        return {"message" : "Login berhasil"}

    except Exception as e:
        return { "message" : "Login Failed"}


@users_routes.route("/login", methods=['GET'])
@login_required
def users_home():
    response_data = dict()
    connection = engine.connect()
    Session = sessionmaker(connection)
    session = Session()
    try:
        user_query = session.query(User)


        if request.args.get('query') != None:
            search_query = request.args.get('query')
            user_query = user_query.filter(User.username.like(f'%{search_query}%'))

        users = user_query.all()
        response_data['user'] = [user.serialize(full=False) for user in users]


        return jsonify(response_data)

    except Exception as e:
        return api_response(
            status_code=500,
            message=str(e),
            data={}
        )
    finally:
        session.close()

@users_routes.route("/login/<int:user_id>", methods=['GET'])
@login_required
def get_user_by_id(user_id):
    connection = engine.connect()
    Session = sessionmaker(connection)
    session = Session()
    try:
        user = session.query(User).filter(User.id==user_id).first()
        if user:
            return jsonify(user.serialize(full=True))
        else:
            return jsonify({
                'message': 'User is not registered yet'
            }), 404
        
    except Exception as e:
        return api_response(
            status_code=500,
            message=str(e),
            data={}
        )
    
    finally:
        session.close()

@users_routes.route("/login/<int:user_id>", methods=['GET'])
@login_required
def update_user_by_id(user_id):
    connection = engine.connect()
    Session = sessionmaker(connection)
    session = Session()
    session.begin()

    try:
        user_to_update = session.query(User).filter(User.id == user_id).first()

        if not user_to_update:
            return api_response(
                status_code=404,
                message="User not found",
                data={}
            )

        user_to_update.username = request.form.get('username', user_to_update.username)
        user_to_update.email = request.form.get('email', user_to_update.email)
        new_password = request.form.get('password')
        if new_password:
            user_to_update.set_password(new_password)
        user_to_update.updated_at = func.now()

        session.commit()
        
        return api_response(
            status_code=201,
            message="User data has been updated successfully",
            data={
                "username": user_to_update.username,
                "email": user_to_update.email,
                "password": new_password
            }
        )    
    except Exception as e:
        session.rollback()
        return api_response(
            status_code=500,
            message=str(e),
            data={}
        )
    
    finally:
        session.close()
    
@users_routes.route("/logout", methods=['GET'])
def do_user_logout():
    logout_user()
    return redirect('/login')

@users_routes.route("/banking", methods=['GET'])
def user_banking():
    return render_template("user/banking.html", current_user=current_user)



@users_routes.route("/update_username", methods=['POST'])
def update_username():
    if current_user.is_authenticated:
        new_username = request.form['new_username']
        current_user.username = new_username
        connection = engine.connect()
        Session = sessionmaker(bind=connection)
        session = Session()

        try:
            session.merge(current_user)  
            session.commit()
        except Exception as e:
            session.rollback()
            print(f"Error updating username: {e}")
            return {"message": "Error updating username"}

        session.close()  
        return redirect('/banking')
    else:
        return {"message": "Unauthorized"}

@users_routes.route("/update_email", methods=['POST'])
def update_email():
    if current_user.is_authenticated:
        new_email = request.form['new_email']
        current_user.email = new_email
        connection = engine.connect()
        Session = sessionmaker(bind=connection)
        session = Session()

        try:
            session.merge(current_user)  
            session.commit()
        except Exception as e:
            session.rollback()
            print(f"Error updating email: {e}")
            return {"message": "Error updating email"}

        session.close()  
        return redirect('/banking')
    else:
        return {"message": "Unauthorized"}
    
@users_routes.route("/login/<int:user_id>", methods=['PUT'])
def update_user(user_id):
    connection = engine.connect()
    Session = sessionmaker(connection)
    session = Session()
    session.begin()

    try:
        user_to_update = session.query(User).filter(User.id == user_id).first()

        if not user_to_update:
            return api_response(
                status_code=404,
                message="User not found",
                data={}
            )

        user_to_update.username = request.form.get('username', user_to_update.username)
        user_to_update.email = request.form.get('email', user_to_update.email)
        new_password = request.form.get('password')
        if new_password:
            user_to_update.set_password(new_password)
        user_to_update.updated_at = func.now()

        session.commit()
        
        return api_response(
            status_code=201,
            message="User data has been updated successfully",
            data={
                "username": user_to_update.username,
                "email": user_to_update.email,
                "password": new_password
            }
        )    
    except Exception as e:
        session.rollback()
        return api_response(
            status_code=500,
            message=str(e),
            data={}
        )
    
    finally:
        session.close()


# Pakai authentikasi token "JWT Manager"

@users_routes.route("/loginjwt", methods=['GET'])
def user_login_jwt():
    return render_template("users/login_jwt.html")

@users_routes.route("/logoutjwt", methods=['GET'])
def do_user_logout_jwt():
    logout_user()
    return redirect('/')

@users_routes.route("/loginjwt", methods=['POST'])
def do_user_login_jwt():
    connection = engine.connect()
    Session = sessionmaker(bind=connection)
    session = Session()

    try:
        user = session.query(User).filter(User.email==request.form['email']).first()

        if user == None:
            return jsonify ({"message": "Email not registered"}), 404
        
        if not user.check_password(request.form['password']):
            return jsonify ({"message": "Password wrong"}), 401
        
        user_id = user.id
        username = user.username

        access_token = create_access_token(identity=user.email)
        return jsonify({"access_token": access_token, "user_id": user_id, "username": username}), 200
        
    except Exception as e:
        print(e) 


        return jsonify({"message": "Login has not been successful"}), 500
    
    finally:
        session.close()