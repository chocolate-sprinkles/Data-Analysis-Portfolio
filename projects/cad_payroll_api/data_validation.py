def validate_json(user_data,keys):
    # user_data is the json provided by the API
    # keys are all the values required by the json
    # validate_json doesn't know what function requires the data afterwards
    # idea is that the validations are based on the keys you're looking for rather the scenario. 
    # ex. ytd_contributions is used for a numebr of functions, but how you validate it is the same for all functions
    pass

def validate_json_cpp(user_data):
    
    if len(user_data.keys()) > 4:
        return "Too many arguments"
    elif "gross_earnings" not in user_data.keys():
        return "gross_earnings missing"
    elif "year" not in user_data.keys():
        return "year missing"
    elif "ytd_contributions" not in user_data.keys():
        return "ytd_contributions missing"
    elif "pay_frequency" not in user_data.keys():
        return "pay_frequency is missing"
    elif not (isinstance(user_data["gross_earnings"],int) or isinstance(user_data["gross_earnings"],float)):
        print(type(user_data["gross_earnings"]))
        return "gross_earnings is not a numeric value"
    elif not isinstance(user_data["year"],int):
        return "year is not an integer value"
    elif not (isinstance(user_data["ytd_contributions"],int) or isinstance(user_data["ytd_contributions"],float)):
        return "ytd_contributions is not a numeric value"
    elif not isinstance(user_data["pay_frequency"],str):
        return "pay_frequency must be a string value"
    elif user_data["gross_earnings"] < 0:
        return "gross_earnings cannot be negative"
    # need to update this one. you can only ask for cpp stuff in the current year? or for any other year that the system has data for?
    elif user_data["year"] != 2023:
        return "year must be 2023"
    elif user_data["ytd_contributions"] < 0:
        return "ytd_contributions cannot be negative"
    elif user_data["pay_frequency"] not in ["Weekly","Bi-Weekly","Semi-Monthly","Monthly"]:
        return "pay_frequency is not one of 'Weekly','Bi-Weekly','Semi-Monthly','Monthly'"
    else:
        return "Valid"

def validate_json_ei(user_data):
    if len(user_data) > 3:
        return "Too many arguments"
    elif "gross_earnings" not in user_data.keys():
        return "gross_earnings is missing"
    elif "year" not in user_data.keys():
        return "year is missing"
    elif "ytd_contributions" not in user_data.keys():
        return "ytd_contributions missing"
    elif not (isinstance(user_data["gross_earnings"],int) or isinstance(user_data["gross_earnings"],float)):
        print(type(user_data["gross_earnings"]))
        return "gross_earnings is not a numeric value"
    elif not isinstance(user_data["year"],int):
        return "year is not an integer value"
    elif not (isinstance(user_data["ytd_contributions"],int) or isinstance(user_data["ytd_contributions"],float)):
        return "ytd_contributions is not a numeric value"
    elif user_data["gross_earnings"] < 0:
        return "gross_earnings cannot be negative"
    # need to update this one. you can only ask for cpp stuff in the current year? or for any other year that the system has data for?
    elif user_data["year"] != 2023:
        return "year must be 2023"
    elif user_data["ytd_contributions"] < 0:
        return "ytd_contributions cannot be negative"
    else:
        return "Valid"
    
