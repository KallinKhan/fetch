from flask import Blueprint, request, make_response
import arrow
import json


transactions = Blueprint('transactions', __name__)

transactions_history = []
payer_balances = {}


@transactions.route('/add_transaction', methods=['POST'])
def add_transaction():
    global transactions_history
    global payer_balances
    payer = request.json['payer']
    points = request.json['points']
    timestamp = request.json['timestamp']

    #  Create balance entry for new payer (if applicable) and update balance
    if payer not in payer_balances.keys():
        payer_balances[payer] = 0
    payer_balances[payer] += points

    #  Add transaction to transaction history list and sort by timestamp
    transactions_history.append({
        'payer': payer,
        'points': points,
        'timestamp': timestamp,
        'remaining': points  # Track how many points from transaction have been "used" in spend
    })
    transactions_history.sort(key=lambda x: arrow.get(x['timestamp']).datetime)

    response = make_response({'message': 'Transaction Added.'})
    return response


@transactions.route('/spend_points', methods=['POST'])
def spend_points():
    global transactions_history
    global payer_balances
    points_to_spend = request.json['points']

    #  Check that there is enough points across payers to complete spend
    if sum(payer_balances.values()) < points_to_spend:
        response = make_response({'message': 'Not Enough Points.'})
        return response
    else:
        #  If a payer balance is negative, we do not want to take more points from that payer
        payers_to_ignore = []
        for payer in payer_balances.keys():
            if payer_balances[payer] < 0:
                payers_to_ignore.append(payer)
        points_from_payers = {}
        #  Go through transaction history and calculate how much each account contributes
        for transaction_index in range(len(transactions_history)):
            transaction = transactions_history[transaction_index]
            payer = transaction['payer']

            #  Skip payers with non-positive balances
            if payer in payers_to_ignore:
                continue

            #  Initialize dictionary entry to track how much to take from each account
            if payer not in points_from_payers.keys():
                points_from_payers[payer] = 0

            #  Check how many points are available to spend from a transaction
            transaction_remaining_points = transaction['remaining']

            #  Use the available points from the transaction, update how many points are still needed, and
            #  update the number of points taken from the account of the transaction's payer.
            #  If the number of points needed to spend is less than the number available in the transaction,
            #  only use what is needed.
            if points_to_spend > transaction_remaining_points:
                points_from_payers[payer] -= transaction_remaining_points
                points_to_spend -= transaction_remaining_points
                transactions_history[transaction_index]['remaining'] = 0
            else:
                points_from_payers[payer] -= points_to_spend
                transactions_history[transaction_index]['remaining'] -= points_to_spend
                break
        #  Update payer balances and create response object
        response_list = []
        for payer in points_from_payers.keys():
            payer_balances[payer] += points_from_payers[payer]
            response_object = {
                'payer': payer,
                'points': points_from_payers[payer]
            }
            response_list.append(response_object)

        response = make_response(json.dumps(response_list))
        return response


@transactions.route('/balance', methods=['GET'])
def balance():
    global payer_balances
    response = make_response(payer_balances)
    return response


@transactions.route('/reset', methods=['GET'])
def reset():
    global transactions_history
    global payer_balances
    transactions_history = []
    payer_balances = {}
    response = make_response(payer_balances)
    return response
