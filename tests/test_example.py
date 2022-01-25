import json


#  Test to execute the calls outlined in the example
def test_sequence_and_spend(client):
    #  Resetting transaction in memory
    client.get('/reset')
    #  Add transactions
    transaction_one = { "payer": "DANNON", "points": 1000, "timestamp": "2020-11-02T14:00:00Z" }
    response_one = client.post('/add_transaction', content_type='application/json', data=json.dumps(transaction_one))
    assert b'{"message":"Transaction Added."}\n' == response_one.data

    transaction_two = { "payer": "UNILEVER", "points": 200, "timestamp": "2020-10-31T11:00:00Z" }
    response_two = client.post('/add_transaction', content_type='application/json', data=json.dumps(transaction_two))
    assert b'{"message":"Transaction Added."}\n' == response_two.data

    transaction_three = { "payer": "DANNON", "points": -200, "timestamp": "2020-10-31T15:00:00Z" }
    response_three = client.post('/add_transaction', content_type='application/json', data=json.dumps(transaction_three))
    assert b'{"message":"Transaction Added."}\n' == response_three.data

    transaction_four = { "payer": "MILLER COORS", "points": 10000, "timestamp": "2020-11-01T14:00:00Z" }
    response_four = client.post('/add_transaction', content_type='application/json', data=json.dumps(transaction_four))
    assert b'{"message":"Transaction Added."}\n' == response_four.data

    transaction_five = { "payer": "DANNON", "points": 300, "timestamp": "2020-10-31T10:00:00Z" }
    response_five = client.post('/add_transaction', content_type='application/json', data=json.dumps(transaction_five))
    assert b'{"message":"Transaction Added."}\n' == response_five.data

    #  Spend points
    spend_points = { "points": 5000 }
    response_spend = client.post('/spend_points', content_type='application/json', data=json.dumps(spend_points))
    response_spend_object = json.loads(response_spend.data)
    expected_spend_response = [
        {"payer": "DANNON", "points": -100},
        {"payer": "UNILEVER", "points": -200},
        {"payer": "MILLER COORS", "points": -4700}
    ]
    assert len(response_spend_object) == len(expected_spend_response)
    assert expected_spend_response[0] in response_spend_object
    assert expected_spend_response[1] in response_spend_object
    assert expected_spend_response[2] in response_spend_object

    #  Check balance
    response_balance = client.get('/balance')
    response_balance_object = json.loads(response_balance.data)
    expected_balance_response = {
        "DANNON": 1000,
        "UNILEVER": 0,
        "MILLER COORS": 5300
    }
    assert expected_balance_response['DANNON'] == response_balance_object['DANNON']
    assert expected_balance_response['UNILEVER'] == response_balance_object['UNILEVER']
    assert expected_balance_response['MILLER COORS'] == response_balance_object['MILLER COORS']

