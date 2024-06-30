import pandas as pd
from . import funcs
from datetime import datetime
from tabulate import tabulate


class FilePaths(object):

    def __init__(self, is_dev: bool):
        self.prefix = 'test_' if is_dev else ''
        self.commitments = f"./data/{self.prefix}commitments.csv"
        self.transactions = f"./data/{self.prefix}transactions.csv"


class Transaction(object):

    def __init__(self, data: pd.Series):
        self.transaction_date: datetime = funcs.str_2_date(data.transaction_date)
        self.transaction_amount: float = funcs.clean_currency(data.transaction_amount)
        self._type: str = data.contribution_or_distribution
        self.commitment_id: int = data.commitment_id

    @staticmethod
    def get_as_cols():
        # return [ "Transaction Date", "Transaction Amount", "Contribution or Distribution", "Commitment ID" ]
        return [ "Transaction Date", "Transaction Amount" ]

    def get_vals(self):
        # return [ funcs.date_obj_2_str(self.transaction_date), funcs.num_2_currency('$', self.transaction_amount), self._type, self.commitment_id ]
        return [ funcs.date_obj_2_str(self.transaction_date), funcs.num_2_currency('$', self.transaction_amount) ]


class LP(object):
    def __init__(self, data: pd.Series):
        self.entity_name: str = data.entity_name
        self.commitment_amount: float = funcs.clean_currency(data.commitment_amount)
        self._id: int = data.id
        self.distributions: list[Transaction] = []
        self.contributions: list[Transaction] = []


class History(object):

    def __init__(self):
        self.lps: dict[int, LP] = {}


    def add_lp(self, lp: LP) -> bool:
        self.lps[lp._id] = lp
        return True


    def get_lp(self, _id: int) -> "LP | None":
        lp: "LP | None" = self.lps.get(_id)
        return lp


    # def get_lp_prop(self, _id: int, prop: str) -> "LP | None":
    #     lp: "LP | None" = self.lps.get(_id)
    #     if lp:
    #         return lp.getattr(prop)


    def add_transaction(self, transaction: Transaction) -> bool:

        if transaction.commitment_id not in self.lps:
            return False

        if transaction._type == "contribution":
            self.lps[transaction.commitment_id].contributions.append(transaction)
        elif transaction._type == "distribution":
            self.lps[transaction.commitment_id].distributions.append(transaction)

        return True
    

class WaterfallConfig(object):
    def __init__(self, preferred_return: float, catch_up: float, carried_interest: float):
        self.preferred_return: float = preferred_return
        self.catch_up: float = catch_up
        self.carried_interest: float = carried_interest


class ResultProperties(object):
    def __init__(self):
        self.starting_tier_capital: float = 0
        self.lp_allocation: float = 0
        self.gp_allocation: float = 0
        self.total_tier_distribution: float = 0
        self.remaining_capital_for_next_tier: float = 0

    @staticmethod
    def get_as_cols():
        return [ "Tier Name", "Starting Tier Capital", "LP Allocation", "GP Allocation", "Total Tier Distribution", "Remaining Capital for Next Tier" ]


class Results(object):
    def __init__(self):
        self.return_on_capital: ResultProperties = ResultProperties()
        self.preferred_return: ResultProperties = ResultProperties()
        self.catch_up: ResultProperties = ResultProperties()
        self.final_split: ResultProperties = ResultProperties()


class Waterfall(object):
    
    def __init__(self, lp: LP, config: WaterfallConfig):

        self.lp: LP = lp
        self.config: WaterfallConfig = config

        self.total_distribution: float = sum(d.transaction_amount for d in lp.distributions)
        self.starting_tier_capital: float = self.total_distribution
        self.total_contributed: float = sum(c.transaction_amount for c in lp.contributions)
        self.last_distribution_date: datetime = lp.distributions[-1].transaction_date

        self.results: Results = Results()


    # def get_tablular_struct(self, props: ResultProperties, name: str) -> list[str]:
    def get_tablular_struct(self, props: ResultProperties, name: str):
        return [
            name,
            funcs.num_2_currency('$', props.starting_tier_capital),
            funcs.num_2_currency('$', props.lp_allocation),
            funcs.num_2_currency('$', props.gp_allocation),
            funcs.num_2_currency('$', props.total_tier_distribution),
            funcs.num_2_currency('$', props.remaining_capital_for_next_tier)
        ]


    def calc_return_on_capital(self):

        final_contribution: float = min(self.total_contributed, self.lp.commitment_amount)

        self.results.return_on_capital.starting_tier_capital = self.starting_tier_capital

        if self.starting_tier_capital > final_contribution:
            self.starting_tier_capital = self.starting_tier_capital - final_contribution
            ans: float = final_contribution
        
        else:
            ans: float = self.starting_tier_capital
            self.starting_tier_capital = 0

        self.results.return_on_capital.lp_allocation = ans
        self.results.return_on_capital.gp_allocation = 0
        self.results.return_on_capital.total_tier_distribution = ans
        self.results.return_on_capital.remaining_capital_for_next_tier = self.starting_tier_capital

        return self.get_tablular_struct(self.results.return_on_capital, "Return on Capital")


    def calc_preferred_return(self):

        self.results.preferred_return.starting_tier_capital = self.starting_tier_capital

        ans: float = 0
        for contribution in self.lp.contributions:
            num_days = funcs.diff_dates(contribution.transaction_date, self.last_distribution_date)
            ans += funcs.preferred_return_formula(contribution.transaction_amount, self.config.preferred_return, num_days)
        
        ans -= self.total_contributed

        if self.starting_tier_capital > ans:
            self.starting_tier_capital = self.starting_tier_capital - ans        
        else:
            ans = self.starting_tier_capital
            self.starting_tier_capital = 0

        self.results.preferred_return.lp_allocation = ans
        self.results.preferred_return.gp_allocation = 0
        self.results.preferred_return.total_tier_distribution = ans
        self.results.preferred_return.remaining_capital_for_next_tier = self.starting_tier_capital

        return self.get_tablular_struct(self.results.preferred_return, "Preferred Return")


    def calc_catch_up(self):

        self.results.catch_up.starting_tier_capital = self.starting_tier_capital

        ans: float = funcs.catch_up_formula(self.config.carried_interest, self.results.preferred_return.lp_allocation, self.config.catch_up)
        
        if self.starting_tier_capital > ans:
            self.starting_tier_capital = self.starting_tier_capital - ans
        else:
            ans = self.starting_tier_capital
            self.starting_tier_capital = 0

        self.results.catch_up.lp_allocation = 0
        self.results.catch_up.gp_allocation = ans
        self.results.catch_up.total_tier_distribution = ans
        self.results.catch_up.remaining_capital_for_next_tier = self.starting_tier_capital

        return self.get_tablular_struct(self.results.catch_up, "Catch Up")


    def calc_final_split(self):

        self.results.final_split.starting_tier_capital = self.starting_tier_capital

        gp_ans: float = self.config.carried_interest * self.results.final_split.starting_tier_capital
        lp_ans: float = self.results.final_split.starting_tier_capital - gp_ans
        remaining_capital_for_next_tier = self.results.final_split.starting_tier_capital - ( gp_ans + lp_ans )
        
        self.results.final_split.lp_allocation = lp_ans
        self.results.final_split.gp_allocation = gp_ans
        self.results.final_split.total_tier_distribution = lp_ans + gp_ans
        self.results.final_split.remaining_capital_for_next_tier = remaining_capital_for_next_tier

        return self.get_tablular_struct(self.results.final_split, "Final Split")


    def calculate(self):

        roc: list[str] = self.calc_return_on_capital()
        pr: list[str] = self.calc_preferred_return()
        cu: list[str] = self.calc_catch_up()
        fs: list[str] = self.calc_final_split()
        result: list[list[str]] = [ roc, pr, cu, fs ]

        print('\n', 40 * '=', '\n')

        print("Name:", self.lp.entity_name)
        print("Commitment Amount:", funcs.num_2_currency('$', self.lp.commitment_amount))
        print('\n', 40 * '=', '\n')

        print("Contributions:")
        print(
            tabulate(
                [i.get_vals() for i in self.lp.contributions],
                headers = Transaction.get_as_cols(),
                tablefmt = "rounded_grid"
            )
        )
        print('\n', 40 * '=', '\n')

        print("Total Distribution:", self.total_distribution, '\n')
        print("Distributions:")
        print(
            tabulate(
                [i.get_vals() for i in self.lp.distributions],
                headers = Transaction.get_as_cols(),
                tablefmt = "rounded_grid"
            )
        )
        print('\n', 40 * '=', '\n')

        print("Last distrubtion was on:", funcs.date_obj_2_str(self.last_distribution_date))
        print('\n', 40 * '=', '\n')
        print("The following table represents the calculations for final distribution")

        print(
            tabulate(
                result,
                headers = ResultProperties.get_as_cols(),
                tablefmt = "rounded_grid"
            )
        )

        return result

