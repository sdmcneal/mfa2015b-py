import pymongo
import datetime
from pymongo import MongoClient
from timeit import default_timer as timer

#from test import initial_data_load 

def load_test_data(db):
    new_balances = [{ "account": "Checking",
                     "amount": 10000.0,
                     "date": datetime.datetime(2015,4,1,0,0),
                     "forecast_model_id": "0",
                     "asset_type": "cash"
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

if __name__ == '__main__':
    print('main function')
    
    #assumes default local port
    client = MongoClient()
    db = client['financials']

    start = timer()
    
    load_test_data(db)
    
    end = timer()
    print('elapsed time: ',(end-start))
    
    client.close()
    