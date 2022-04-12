import os
import json
import pandas as pd

# create a function to extract the data from the json file
def get_json(folder_name):
    all_data = []
    for file in os.listdir(os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', folder_name))):
        if file.endswith(".json"):
            try:
                with open(os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', folder_name,file))) as json_file:
                    data = json.load(json_file)
                    all_data.append(data)
            except:
                print("An exception occurred")
    return pd.json_normalize(all_data)


def main():
    # get the data from the json file
    accounts = get_json('data/accounts/')
    cards = get_json('data/cards/')
    savings_accounts = get_json('data/savings_accounts/')

    # print result for question no. 1
    print('### Question no 1###')
    print('\n', accounts)
    print('\n', cards)
    print('\n', savings_accounts)

    # change timestamp to readable format
    accounts['ts_accounts'] = pd.to_datetime(accounts['ts'], unit='ms')
    cards['ts_cards'] = pd.to_datetime(cards['ts'], unit='ms')
    savings_accounts['ts_savings_accounts'] = pd.to_datetime(
        savings_accounts['ts'], unit='ms')

    # generating card id and savings account id for join table
    accounts['data.account_id'] = accounts['id'].apply(lambda x: x[0:2])
    cards['data.card_id'] = cards['id'].apply(lambda x: x[0:2])
    savings_accounts['data.savings_account_id'] = savings_accounts['id'].apply(
        lambda x: x[0:3])

    # merging account table, card table, and savings account table
    mer1 = accounts.merge(cards, left_on='set.card_id',
                          right_on='data.card_id', how='left')
    mer2 = mer1.merge(savings_accounts, left_on='set.savings_account_id',
                      right_on='data.savings_account_id', how='left')

    # create a new column for the merging all timestamp
    mer2['all_ts'] = None
    mer2["all_ts"].fillna(mer2["ts_cards"], inplace=True)
    mer2["all_ts"].fillna(mer2["ts_savings_accounts"], inplace=True)
    mer2["all_ts"].fillna(mer2["ts_accounts"], inplace=True)

    # sort the dataframe by the timestamp
    mer2.sort_values(by=['all_ts'], inplace=True)

    # print result for question no. 2
    print('\n\n\n### Question no 2###')
    print('\n', mer2)

    # filter the data to get non empty data in credit_used on cards table and balance on savings account table
    filt = (mer2['set.credit_used'].notnull() & mer2['set.credit_used'] > 0) | (
        mer2['set.balance'].notnull() & mer2['set.balance'] > 0)
    col_res = ['all_ts', 'set.credit_used', 'set.balance']
    res = mer2.loc[filt, col_res]

    # print result for question no. 3
    print('\n\n\n### Question no 3###')
    print('\n', res)
    print('\n', 'Total Transactions:', len(res))
    for i in range(0, len(res)):
        val = ''
        if res.iat[i, 1] > 0:
            val = 'credit used ' + str(res.iat[i, 1])
        elif res.iat[i, 2] > 0:
            val = 'balance added ' + str(res.iat[i, 2])
        print('Transaction No.' + str(i+1) + ' on ' +
              str(res.iat[i, 0]) + ' is ' + val)


if __name__ == '__main__':
    main()
