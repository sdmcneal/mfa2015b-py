import pymongo
import datetime
from pymongo import MongoClient
from bson import SON
from timeit import default_timer as timer

#from test import initial_data_load 

def load_test_data(db):
    new_balances = [{ "account": "Checking",
                     "balance": 10000.0,
                     "date": datetime.datetime(2015,4,1,0,0),
                     "forecast_model_id": "0",
                     "asset_type": "cash"
    },
        { "account": "401k",
                     "balance": 100000.0,
                     "date": datetime.datetime(2015,3,15,0,0),
                     "forecast_model_id": "0",
                     "asset_type": "equity"
    }]
    
    new_ledger_entries = [{ "account": "Checking",
                           "user_id": 100,
                           "amount": -3000.0,
                           "date": datetime.datetime(2015,4,1,0,0),
                           "description": "Test Entry 1",
                           "forecast_model_id": "999Py" },
        { "account": "Checking",
         "user_id": 100,
         "amount": -5000.0,
         "date": datetime.datetime(2015,4,3,0,0),
         "description": "Test Entry 2",
         "forecast_model_id": "999Py" }]
    
    db.balances.insert_many(new_balances)
    result = db.ledgers.insert_many(new_ledger_entries)
    print(result)
    
def get_last_balance(db):
    print('getting last balances')
    pipe = [
        {"$sort": { "date": 1} },
        { "$group": { "_id": "$account", "lastBalanceDate": { "$last": "$date"},
        "lastBalance": { "$last": "$balance" }}}
        ]
    result = db.balances.aggregate(pipeline=pipe)
    
    
    effective_date = datetime.datetime(2015,5,15,0,0)
    account_names = [];
    effective_balances = [];
    balance_details = [];
    
    i=0
    for doc in result:
        print(doc)
        account_name = doc['_id']
        account_names.append(account_name)
        working_balance = doc['lastBalance']
        effective_balances.append(working_balance)
        
        working_details = 'Starting balance of ' + str(working_balance) + ' on ' + str(doc['lastBalanceDate'])
        balance_details.append(working_details)
        
        query = { "account" : account_name,
                 "forecast_model_id": {"$in": [ "0", "1", "999Py"] },
                    "$and": [ { "date": { "$gt": doc['lastBalanceDate']}}, {"date": { "$lte": effective_date}}]}
        account_results = db.ledgers.find(query)
        for transaction in account_results:
            working_balance = working_balance + transaction['amount']
            working_details = working_details + ' + ' + str(transaction['amount']) + ' on ' + str(transaction['date'])
            effective_balances[-1] = working_balance
            balance_details[-1] = working_details
        
        print('account: ' + account_name + ' balance: ' + str(working_balance) + ' details: ' + working_details)
        
    print('got em ',result)

if __name__ == '__main__':
    print('main function')
    
    #assumes default local port
    client = MongoClient()
    db = client['financials']

    start = timer()
    
    load_test_data(db)
    get_last_balance(db)
    
    end = timer()
    print('elapsed time: ',(end-start))
    
    client.close()
    
    