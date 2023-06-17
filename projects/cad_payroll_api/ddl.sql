CREATE TABLE cpp_values (
    yr SMALLINT PRIMARY KEY,
    max_contribution MONEY NOT NULL,
    exemption MONEY NOT NULL,
    rate NUMERIC(6,5) NOT NULL
);

CREATE TABLE ei_values (
    yr SMALLINT PRIMARY KEY,
    max_contribution MONEY NOT NULL,
    rate NUMERIC(6,5) NOT NULL
);

CREATE TABLE tax_brackets (
    yr SMALLINT NOT NULL,
    region VARCHAR(30) NOT NULL,
    bracket_num NUMERIC(2) NOT NULL,
    low MONEY NOT NULL,
    high MONEY NOT NULL,
    rate NUMERIC(6,5) NOT NULL,
    constant MONEY NOT NULL,
    PRIMARY KEY (yr,region,bracket_num)
);

CREATE TABLE canada_employment_amount (
    yr SMALLINT PRIMARY KEY,
    amount MONEY NOT NULL
);

CREATE TABLE pay_periods (
    yr SMALLINT NOT NULL,
    full_name VARCHAR(30) NOT NULL,
    num_pay_periods NUMERIC(3) NOT NULL,
    PRIMARY KEY (yr,full_name)
);

CREATE TABLE company (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    address_1 VARCHAR(50) NOT NULL,
    address_2 VARCHAR(50),
    city VARCHAR(50) NOT NULL,
    postal_code VARCHAR(6) NOT NULL,
    province VARCHAR(30) NOT NULL
);

CREATE TABLE employee (
    id NUMERIC(15) PRIMARY KEY,
    company_id NUMERIC NOT NULL,
    fname VARCHAR(30) NOT NULL,
    lname VARCHAR(30) NOT NULL,
    title VARCHAR(50) NOT NULL,
    salary_pp MONEY NOT NULL,
    pay_frequency VARCHAR(30) NOT NULL,
    fed_personal_amount MONEY NOT NULL,
    prov_personal_amount MONEY NOT NULL,
    address_1 VARCHAR(50) NOT NULL,
    address_2 VARCHAR(50),
    city VARCHAR(50) NOT NULL,
    postal_code VARCHAR(6) NOT NULL,
    province VARCHAR(30) NOT NULL,
);

CREATE TABLE payroll_codes (
    id VARCHAR(7) PRIMARY KEY,
    type VARCHAR(30) NOT NULL,
    name VARCHAR(50) NOT NULL
);

CREATE TABLE payroll_logs (
    run_date DATE NOT NULL,
    employee_id NUMERIC(15) NOT NULL,
    company_id INTEGER NOT NULL,
    pay_period NUMERIC(3) NOT NULL,
    payroll_code VARCHAR(7) NOT NULL,
    amount MONEY NOT NULL,
    PRIMARY KEY (run_date,employee_id,company_id,pay_period),
    FOREIGN KEY (employee_id) REFERENCES employee (id),
    FOREIGN KEY (company_id) REFERENCES company (id),
    FOREIGN KEY (payroll_code) REFERENCES payroll_codes (id)
);

CREATE TABLE payroll_schedule (
    company_id NUMERIC NOT NULL,
    pp_start DATE NOT NULL,
    pp_end DATE NOT NULL,
    pay_date DATE NOT NULL,
    off_cycle DATE NOT NULL
);