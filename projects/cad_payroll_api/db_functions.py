import psycopg2

# handling SERIAL type
# See the following example:

# INSERT INTO fruits(name) 
# VALUES('Orange');
# Code language: SQL (Structured Query Language) (sql)

# Or

# INSERT INTO fruits(id,name) 
# VALUES(DEFAULT,'Apple');

def clean_query_results(value,data_type):

    if data_type == "money":
        return float(value.replace("$","").replace(",",""))
    elif data_type == "numeric":
        return float(value)
    # so, this is redundant here, but I don't want another if statement in execute_query() to determine whether the data needs to be cleaned or not. i'd rather just throw all the data here and directly append the returned value to the list I'm creating
    else:
        return value


def execute_query(query,table_name):

    # store connection details in a txt file
    # how to securely store user + pass information?
    # how to get around SQL inject?

    conn = psycopg2.connect(host="localhost",database="cad_payroll_api",user="ivan",password="apples123",port=5432)
    cursor = conn.cursor()
    
    # get data
    cursor.execute(query)
    query_results = cursor.fetchall()
    print(query_results)
    # get column names
    column_query = "SELECT column_name,data_type FROM information_schema.columns WHERE table_schema = 'public' AND table_name = '{}';".format(table_name)
    cursor.execute(column_query)
    column_names = cursor.fetchall()
    print(column_names)
    print(column_names[0][0])
    
    # taking the followin
    # [(2023, '$3,754.00', '$3,500.00', Decimal('0.05950'))]
    # [('yr', 'smallint'), ('max_contribution', 'money'), ('exemption', 'money'), ('rate', 'numeric')]
    # and turning it into a dictionary of lists

    return_dict = {}

    for column_pos in range(len(column_names)):
        # create key-value pair with key = column  name from table
        return_dict[column_names[column_pos][0]] = []
        for row_pos in range(len(query_results)):
            return_dict[column_names[column_pos][0]].append(clean_query_results(query_results[row_pos][column_pos],column_names[column_pos][1]))

    conn.close()
    return return_dict

# might be a future where I need more specific queries. for now it's going to be pretty simple
# do I want to SELECT * if I already know year + region? any data thats only relevant to the db?
def get_cpp_data(year):
    query = "SELECT * FROM cpp_values WHERE yr = {}".format(year)
    return execute_query(query,"cpp_values")

def get_ei_query(year):
    query = "SELECT * FROM ei_values WHERE yr = {}".format(year)
    return execute_query(query,"ei_values")

def get_tax_brackets(year,region):
    query = "SELECT * FROM tax_brackets WHERE yr = {} AND region = {}".format(year,region)
    return execute_query(query,"tax_brackets")

def get_canada_employment_amount(year):
    query = "SELECT * FROM canada_employment_amount WHERE yr = {}".format(year)
    return execute_query(query,"canada_employment_amount")

def get_pay_periods(year):
    query = "SELECT * FROM pay_periods WHERE yr = {}".format(year)
    return execute_query(query,"pay_periods")

if __name__ == "__main__":
    print(execute_query("SELECT * FROM cpp_values WHERE yr = 2023;","cpp_values"))
    print(execute_query("SELECT * FROM tax_brackets WHERE region = 'Alberta';","tax_brackets"))
    print(execute_query("SELECT * FROM pay_periods WHERE yr = 2023","pay_periods"))
