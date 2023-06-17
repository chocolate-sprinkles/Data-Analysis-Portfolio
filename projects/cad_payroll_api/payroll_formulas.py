import logging 
import db_functions as db

# Tasks
# 1. create flask app file with a request to run payroll
# 2. add logging functionality to formulas
# 3. add data validation for html request 
# 4. create steps for refactoring, code style, naming conventions, etc.
# 5. setup local postreg database and create tables for data 

# File Thoughts
# 1. fix order of parameters
# 2. standardize parameter names
# 3. tax bracket data, max contribution/premium, cpp exemption, cpp/ei rates, pay periods, canada_employment amount should all be stored in a database

# Function Thoughts
# 1. Can't refactor function any further
# 2. Will need to look into order of parameters
# 3. add type hinting for parameters and also for output
# 4. update comments once parameter names and order is finalized
def cpp_contributions_old(ytd_contributions, rate, exemption, contribution_max, pay_periods, gross_income):
    # ytd_contributions - cpp contributions from the beginning of the year to today
    # rate - cpp contribution rate
    # contribution_max - maximum contribution amount for the taxation year
    # pay_periods - number of pay periods for the employee whose cpp is being calculated
    # gross_income - income before taxations or any deductions for a pay period

    current_cpp_contribution = ((gross_income * pay_periods) - exemption) / pay_periods * rate

    if current_cpp_contribution < 0:
        logging.info("payroll_formulas.cpp_contributions() produced a reuslt of {}".format(0))
        return 0
    elif ytd_contributions >= contribution_max:
        logging.info("payroll_formulas.cpp_contributions() produced a reuslt of {}".format(0))
        return 0
    elif current_cpp_contribution + ytd_contributions > contribution_max:
        logging.info("payroll_formulas.cpp_contributions() produced a reuslt of {}".format(contribution_max - ytd_contributions))
        return contribution_max - ytd_contributions
    else:
        logging.info("payroll_formulas.cpp_contributions() produced a reuslt of {}".format(current_cpp_contribution))
        return current_cpp_contribution
    
def cpp_contributions(gross_income,pay_frequency,ytd_contributions,year):
    
    # load values
    cpp_data =db.get_cpp_data(year)
    pay_period_data = db.get_pay_periods(year)

    # transform pay_frqeuency to numeric value
    


def ei_premium(ytd_contributions, rate, gross_income, contribution_max):

    current_ei_premum = gross_income * rate

    if ytd_contributions >= contribution_max:
        return 0
    elif current_ei_premum + ytd_contributions > contribution_max:
        return contribution_max - ytd_contributions
    else:
        return current_ei_premum


def federal_tax(gross_income, pay_periods):

    annual_taxable_income = gross_income * pay_periods

    # theres a constant K that is added to the tables. what is it used for again?
    if annual_taxable_income < 53359:
        return annual_taxable_income * 0.15
    elif annual_taxable_income < 106717:
        return 53359 * 0.15 + (annual_taxable_income - 53359.01) * 0.205
    elif annual_taxable_income < 165430:
        return 53359 * 0.15 + (106717 - 53359.01) * 0.205 + (annual_taxable_income - 106717.01) * 0.26
    elif annual_taxable_income < 235675:
        return 53359 * 0.15 + (106717 - 53359.01) * 0.205 + (165430-106717.01) * 0.26 + (annual_taxable_income - 165430.01) * 0.29
    else:
        return 53359 * 0.15 + (106717 - 53359.01) * 0.205 + (165430-106717.01) * 0.26 + (235675 - 165430.01) * 0.29 + (annual_taxable_income - 235675.01) * 0.33


def federal_tax_credits(pay_periods, cpp_contribution, ei_premiums, canada_employment_amount, basic_personal_amount, cpp_contribution_max, ei_premium_max, tax_rate_min):

    cpp_credits = min(cpp_contribution_max, cpp_contribution * pay_periods)
    ei_credits = min(ei_premium_max, ei_premiums * pay_periods)

    tax_credits = (basic_personal_amount + cpp_credits + ei_credits + canada_employment_amount) * tax_rate_min

    return tax_credits


def alberta_tax(gross_income, pay_periods):

    annual_taxable_income = gross_income * pay_periods

    # theres a constant K that is added to the tables. what is it used for again?
    if annual_taxable_income < 142292:
        return annual_taxable_income * 0.1
    elif annual_taxable_income < 170751:
        return 142292 * 0.1 + (annual_taxable_income - 142292) * 0.12
    elif annual_taxable_income < 227668:
        return 142292 * 0.1 + (170751 - 142292) * 0.12 + (annual_taxable_income - 170751) * 0.13
    elif annual_taxable_income < 341502:
        return 142292 * 0.1 + (170751 - 142292) * 0.12 + (227668 - 170751) * 0.13 + (annual_taxable_income - 227668) * 0.14
    else:
        return 142292 * 0.1 + (170751 - 142292) * 0.12 + (227668 - 170751) * 0.13 + (341502 - 227668) * 0.14 + (annual_taxable_income - 341502) * 0.15


def alberta_tax_credits(pay_periods, cpp_contribution, ei_premiums, basic_personal_amount, cpp_contribution_max, ei_premium_max, tax_rate_min):

    cpp_credits = min(cpp_contribution_max, cpp_contribution * pay_periods)
    ei_credits = min(ei_premium_max, ei_premiums * pay_periods)

    tax_credits = (basic_personal_amount + cpp_credits + ei_credits) * tax_rate_min

    return tax_credits

# test function to see how you run the entire payroll process
def alberta_payroll(gross_income,pay_periods,cpp_rate,ei_premium,cpp_max_contribution,ei_max_premium,ytd_cpp_contributions,ytd_ei_premiums,cpp_exemption,canada_employment_amount,fed_tax_rate_min,provincial_tax_rate_min):
    pass

def process_payroll():
    pass
