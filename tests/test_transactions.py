import json


#  Test to execute the calls outlined in the example
def test_add_transaction(client):
    #  Resetting transaction in memory
    client.get('/reset')

    #  Add transaction
    transaction = { "payer": "DANNON", "points": 500, "timestamp": "2020-11-02T12:00:00Z" }
    response_one = client.post('/add_transaction', content_type='application/json', data=json.dumps(transaction))
    assert b'{"message":"Transaction Added."}\n' == response_one.data

    #  Check balance
    response_balance = client.get('/balance')
    response_balance_object = json.loads(response_balance.data)
    expected_balance_response = {
        "DANNON": 500,
    }
    assert expected_balance_response['DANNON'] == response_balance_object['DANNON']


def test_spend_points(client):
    #  Resetting transaction in memory
    client.get('/reset')

    #  Add transactions
    transaction = { "payer": "DANNON", "points": 1000, "timestamp": "2020-11-02T14:00:00Z" }
    response_one = client.post('/add_transaction', content_type='application/json', data=json.dumps(transaction))
    assert b'{"message":"Transaction Added."}\n' == response_one.data

    #  Spend points
    spend_points = { "points": 200 }
    response_spend = client.post('/spend_points', content_type='application/json', data=json.dumps(spend_points))
    response_spend_object = json.loads(response_spend.data)
    expected_spend_response = [
        {"payer": "DANNON", "points": -200},
    ]
    assert len(response_spend_object) == len(expected_spend_response)
    assert expected_spend_response[0] in response_spend_object


def test_check_balance(client):
    #  Resetting transaction in memory
    client.get('/reset')

    #  Add transactions
    transaction = { "payer": "UNILEVER", "points": 3000, "timestamp": "2020-11-02T14:00:00Z" }
    response_one = client.post('/add_transaction', content_type='application/json', data=json.dumps(transaction))
    assert b'{"message":"Transaction Added."}\n' == response_one.data

    #  Check Balance
    response_balance = client.get('/balance')
    response_balance_object = json.loads(response_balance.data)
    expected_balance_response = {
        "UNILEVER": 3000
    }
    assert expected_balance_response['UNILEVER'] == response_balance_object['UNILEVER']


def test_spend_oldest(client):
    #  Resetting transaction in memory
    client.get('/reset')

    #  Add transactions
    transaction = { "payer": "DANNON", "points": 1000, "timestamp": "2020-11-02T14:00:00Z" }
    response_one = client.post('/add_transaction', content_type='application/json', data=json.dumps(transaction))
    assert b'{"message":"Transaction Added."}\n' == response_one.data

    transaction = { "payer": "UNILEVER", "points": 1000, "timestamp": "2020-10-01T14:00:00Z" }
    response_two = client.post('/add_transaction', content_type='application/json', data=json.dumps(transaction))
    assert b'{"message":"Transaction Added."}\n' == response_two.data

    #  Spend points
    spend_points = { "points": 200 }
    response_spend = client.post('/spend_points', content_type='application/json', data=json.dumps(spend_points))
    response_spend_object = json.loads(response_spend.data)
    expected_spend_response = [
        {"payer": "UNILEVER", "points": -200},
    ]
    assert len(response_spend_object) == len(expected_spend_response)
    assert expected_spend_response[0] in response_spend_object


def test_not_enough_points(client):
    #  Resetting transaction in memory
    client.get('/reset')

    #  Add transactions
    transaction = { "payer": "DANNON", "points": 1000, "timestamp": "2020-11-02T14:00:00Z" }
    response_one = client.post('/add_transaction', content_type='application/json', data=json.dumps(transaction))
    assert b'{"message":"Transaction Added."}\n' == response_one.data

    #  Spend points
    spend_points = { "points": 2000 }
    response_spend = client.post('/spend_points', content_type='application/json', data=json.dumps(spend_points))
    assert b'{"message":"Not Enough Points."}\n' == response_spend.data