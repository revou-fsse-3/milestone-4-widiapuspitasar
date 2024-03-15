from flask import Blueprint, request, jsonify
from models.transaction import Transaction
from utils.api_response import api_response
from connectors.mysql_connector import engine
from flask_login import login_required
from sqlalchemy.orm import sessionmaker

transaction_routes = Blueprint('transaction_routes', __name__)

@transaction_routes.route('/transaction/deposit', methods=['POST'])
@login_required
def create_transaction_deposit():
    connection = engine.connect()
    Session = sessionmaker(connection)
    session = Session()

    try:
        from_account_id = request.form.get('from_account_id')
        to_account_id = request.form.get('to_account_id')
        amount = request.form.get('amount')

        if not to_account_id or not amount:
            raise ValueError("Mohon untuk mengisi 'to_account_id' dan 'amount'")
        
        new_deposit_transaction = Transaction(
            from_account_id=from_account_id,  
            to_account_id=to_account_id,
            amount=amount,
            type='deposit',
            description='pengiriman dana'
        )

        session.add(new_deposit_transaction)
        session.commit()

        return api_response(
            status_code=201,
            message="Pembuatan data transaksi deposit berhasil diinput",
            data={
                "id": new_deposit_transaction.id,
                "from_account_id": new_deposit_transaction.from_account_id,
                "to_account_id": new_deposit_transaction.to_account_id,
                "amount": new_deposit_transaction.amount,
                "type": new_deposit_transaction.type,
                "description": new_deposit_transaction.description,
                "created_at": new_deposit_transaction.created_at
            }
        )  
    
    except Exception as e:
        return jsonify({
            'error': 'Gagal membuat transaksi deposit',
            'message': str(e)
        }), 500
    
    finally:
        session.close()

@transaction_routes.route('/transaction/withdrawal', methods=['POST'])
@login_required
def create_transaction_withdrawal():
    connection = engine.connect()
    Session = sessionmaker(connection)
    session = Session()

    try:
        from_account_id = request.form.get('from_account_id')
        to_account_id = request.form.get('to_account_id')
        amount = request.form.get('amount')

        if not to_account_id or not amount:
            raise ValueError("Mohon untuk mengisi 'to_account_id' dan 'amount'")
        
        new_withdrawal_transaction = Transaction(
            from_account_id=from_account_id,  
            to_account_id=to_account_id,
            amount=amount,
            type='withdrawal',
            description='Pengembalian Dana'
        )

        session.add(new_withdrawal_transaction)
        session.commit()

        return api_response(
            status_code=201,
            message="Pembuatan data transaksi withdrawal berhasil diinput",
            data={
                "id": new_withdrawal_transaction.id,
                "from_account_id": new_withdrawal_transaction.from_account_id,
                "to_account_id": new_withdrawal_transaction.to_account_id,
                "amount": new_withdrawal_transaction.amount,
                "type": new_withdrawal_transaction.type,
                "description": new_withdrawal_transaction.description,
                "created_at": new_withdrawal_transaction.created_at
            }
        )  
    
    except Exception as e:
        return jsonify({
            'error': 'Gagal membuat transaksi withdrawal',
            'message': str(e)
        }), 500
    
    finally:
        session.close()

@transaction_routes.route('/transaction/transfer', methods=['POST'])
@login_required
def create_transaction_transfer():
    connection = engine.connect()
    Session = sessionmaker(connection)
    session = Session()

    try:
        from_account_id = request.form.get('from_account_id')
        to_account_id = request.form.get('to_account_id')
        amount = request.form.get('amount')

        if not to_account_id or not amount:
            raise ValueError("Mohon untuk mengisi 'to_account_id' dan 'amount'")
        
        new_transfer_transaction = Transaction(
            from_account_id=from_account_id,  
            to_account_id=to_account_id,
            amount=amount,
            type='transfer',
            description='Transfer Dana'
        )

        session.add(new_transfer_transaction)
        session.commit()

        return api_response(
            status_code=201,
            message="Pembuatan data transaksi withdrawal berhasil diinput",
            data={
                "id": new_transfer_transaction.id,
                "from_account_id": new_transfer_transaction.from_account_id,
                "to_account_id": new_transfer_transaction.to_account_id,
                "amount": new_transfer_transaction.amount,
                "type": new_transfer_transaction.type,
                "description": new_transfer_transaction.description,
                "created_at": new_transfer_transaction.created_at
            }
        )  
    
    except Exception as e:
        return jsonify({
            'error': 'Gagal membuat transaksi transfer',
            'message': str(e)
        }), 500
    
    finally:
        session.close()

@transaction_routes.route('/transaction', methods=['GET'])
@login_required
def transactions_home():
    response_data = dict()
    connection = engine.connect()
    Session = sessionmaker(connection)
    session = Session()
    try:
        transaction_query = session.query(Transaction)


        if request.args.get('query') != None:
            search_query = request.args.get('query')
            transaction_query = transaction_query.filter(Transaction.from_account_id.like(f'%{search_query}%'))

        transaction = transaction_query.all()
        response_data['transaction'] = [transaction.serialize(full=False) for transaction in transaction]


        return jsonify(response_data)

    except Exception as e:
        return api_response(
            status_code=500,
            message=str(e),
            data={}
        )
    finally:
        session.close()

@transaction_routes.route('/transaction/<int:transaction_id>', methods=['GET'])
@login_required
def get_transaction_by_id(transaction_id):
    connection = engine.connect()
    Session = sessionmaker(connection)
    session = Session()
    try:
        transaction = session.query(Transaction).filter(Transaction.id==transaction_id).first()
        if transaction:
            return jsonify(transaction.serialize(full=True))
        else:
            return jsonify({
                'message': 'Account belum terdaftar di sistem'
            }), 404
        
    except Exception as e:
        return api_response(
            status_code=500,
            message=str(e),
            data={}
        )
    
    finally:
        session.close()
