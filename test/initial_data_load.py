import datetime

def load_test_data(db):
    new_balances = [{ "account": "Checking",
                     "amount": 10000.0,
                     "date": datetime(2015,4,1,0,0),
                     "forecast_model_id": "0",
                     "asset_type": "cash"
    }]
    
    new_ledger_entries = [{ "account": "Checking",
                           "user_id": 100,
                           "amount": -3000.0,
                           "date": datetime(2015,4,1,0,0),
                           "description": "Test Entry 1",
                           "forecast_model_id": "999" },
        { "account": "Checking",
         "user_id": 100,
         "amount": -5000.0,
         "date": datetime(2015,4,3,0,0),
         "description": "Test Entry 1",
         "forecast_model_id": "999" }]
    
    result = db.ledgers.insert_many(new_ledger_entries)
    