from utils import funcs
from utils.models import FilePaths, History, LP, Transaction, Waterfall, WaterfallConfig
import pandas as pd
import sys


if len(sys.argv) > 1 and sys.argv[1] == "--example":
    file_paths = FilePaths(is_dev = True)
    print("", 40 * "*", "\n", "Loading example data", "\n", 40 * "*", "\n")
else:
    file_paths = FilePaths(is_dev = False)

history: History = History()

config: WaterfallConfig = WaterfallConfig(
    preferred_return = 8.0 / 100.0,
    catch_up = 100.0 / 100.0,
    carried_interest = 20.0 / 100.0
)


def process_commitments():
    commitments_frame: pd.DataFrame = funcs.load_dataframe(file_paths.commitments)
    for _, row in commitments_frame.iterrows():
        lp: LP = LP(row)
        history.add_lp(lp)


def process_transactions():
    transactions_frame: pd.DataFrame = funcs.load_dataframe(file_paths.transactions)
    # transactions['clean_transaction_amount'] = transactions['transaction_amount'].apply(utils.clean_currency).astype('float')
    # filtered_df = transactions[transactions['contribution_or_distribution'] == 'distribution']
    # result = filtered_df.groupby('commitment_id')['clean_transaction_amount'].sum()
    for _, row in transactions_frame.iterrows():
        trnx: Transaction = Transaction(row)
        history.add_transaction(trnx)


def main():

    process_commitments()
    process_transactions()

    try:
        commitment_id = int(input("Enter Commitment ID: "))
    except:
        print("Commitment ID needs to be an integer")
        exit()

    lp: LP = history.get_lp(commitment_id)
    if lp is None:
        print("No Limited Partner found, try again!")
        exit()

    waterfall: Waterfall = Waterfall(lp, config)
    waterfall.calculate()


if __name__ == "__main__":
    main()

