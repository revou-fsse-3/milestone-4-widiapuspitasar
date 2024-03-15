from flask import Blueprint, render_template, request, redirect, jsonify
from connectors.mysql_connector import engine
from models.account import Account
from sqlalchemy.orm import sessionmaker
from flask_login import current_user, login_required
from utils.api_response import api_response
from sqlalchemy import func

accounts_routes = Blueprint('accounts_routes', __name__)

@accounts_routes.route("/accounts", methods=['POST'])
def create_account():
    try:
        account_type = request.form['account_type']
        account_number = request.form['account_number']
        balance = request.form['balance']

        if not account_type or not account_number or not balance:
            raise ValueError("Data tidak lengkap")
        
        new_account = Account(user_id = current_user.id, account_type=account_type, account_number=account_number, balance=balance)

        connection = engine.connect()
        Session = sessionmaker(connection)
        session = Session()

        session.begin()
        session.add(new_account)
        session.commit()

        return api_response(
            status_code=201,
            message="The creation of new account data has been entered successfully",
            data={
                "id": new_account.id,
                "user_id": new_account.user_id,
                "account_type": new_account.account_type,
                "account_number": new_account.account_number,
                "balance": new_account.balance
            }
        )
        
    
    except Exception as e:
        return api_response(
            status_code=500,
            message=str(e),
            data={}
        )
    finally:
        session.close()
    

@accounts_routes.route("/accounts", methods=['GET'])
@login_required
def accounts_home():
    response_data = dict()
    connection = engine.connect()
    Session = sessionmaker(connection)
    session = Session()
    try:
        account_query = session.query(Account)

        if request.args.get('query') != None:
            search_query = request.args.get('query')
            account_query = account_query.filter(Account.account_type.like(f'%{search_query}%'))

        accounts = account_query.all()
        response_data['accounts'] = [account.serialize(full=False) for account in accounts]

        return jsonify(response_data)

    except Exception as e:
        return api_response(
            status_code=500,
            message=str(e),
            data={}
        )
    finally:
        session.close()

@accounts_routes.route("/accounts/<int:account_id>", methods=['GET'])
@login_required
def accounts_byid(account_id):
    connection = engine.connect()
    Session = sessionmaker(connection)
    session = Session()
    try:
        account = session.query(Account).filter(Account.id==account_id).first()

        if account:
            return jsonify(account.serialize(full=True))
        else:
            return jsonify({
                'message': 'The account has not been registered in the system'
            }), 404
        
    except Exception as e:
        return api_response(
            status_code=500,
            message=str(e),
            data={}
        )
    
    finally:
        session.close()

@accounts_routes.route("/accounts/<int:account_id>", methods=['PUT'])
@login_required
def update_account(account_id):
    connection = engine.connect()
    Session = sessionmaker(connection)
    session = Session()
    session.begin()

    try:
        update_account = session.query(Account).filter(Account.id == account_id).first()

        update_account.account_type = request.form.get('account_type', update_account.account_type)
        update_account.account_number = request.form.get('account_number', update_account.account_number)
        update_account.balance = request.form.get('balance', update_account.balance)
        update_account.updated_at = func.now()

        session.commit()
            
        return api_response(
            status_code=201,
            message="Account data updated successfully",
            data={
                    "account_type": update_account.account_type,
                    "account_number": update_account.account_number,
                    "balance": update_account.balance,
                    "updated_at": update_account.updated_at
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

@accounts_routes.route("/accounts/<int:id>", methods=['DELETE'])
@login_required
def delete_account(id):
    connection = engine.connect()
    Session = sessionmaker(connection)
    session = Session()

    try:
        account_delete = session.query(Account).filter(Account.id == id).first()
                        
        session.delete(account_delete)
        session.commit()
        return api_response(
                status_code=200,
                message="Account data has been successfully deleted",
                data={
                "id": account_delete.id,
                "user_id": account_delete.user_id,
                "account_type": account_delete.account_type,
                "account_number": account_delete.account_number,
                "balance": account_delete.balance
                }
            )          
    
    except Exception as e:
        session.rollback()
        return jsonify({"error": str(e)}), 500
    
    finally:
        session.close()