from flask import Flask, jsonify, request
from flask_api import status
import payroll_formulas as pf
import logging
import data_validation as dv

app = Flask(__name__)


@app.route("/")
def home():
    data = request.get_json()
    return jsonify(data)


@app.route("/payroll/cpp_contributions")
def cpp_contributions():
    json_body = request.get_json()
    data_validation_response = dv.validate_json_cpp(json_body)
    print(type(json_body["gross_earnings"]))
    if data_validation_response != "Valid":
        return jsonify({"error_message":data_validation_response}),status.HTTP_400_BAD_REQUEST
    else:
        return jsonify({"cpp_contribution":pf.cpp_contributions(json_body["gross_earnings"],json_body["pay_frequency"],json_body["ytd_contributions"],json_body["year"])})


@app.route("/payroll/ei_premiums")
def ei_premiums():
    json_body = request.get_json()
    data_validation_response = dv.validate_json_ei(json_body)
    print(type(json_body["gross_earnings"]))
    if data_validation_response != "Valid":
        return jsonify({"error_message":data_validation_response}),status.HTTP_400_BAD_REQUEST
    else:
        return jsonify({"ei_premiums":pf.ei_premium(json_body["gross_earnings"],json_body["ytd_contributions"],json_body["year"])})    
    #return jsonify({"message":"test"})


@app.route("/payroll/payroll")
def payroll():
    return jsonify({"message":"test"})


if __name__ == "__main__":
    logging.basicConfig(filename=".\\projects\\cad_payroll_api\\logs.txt",format='%(asctime)s - %(message)s',level=logging.DEBUG)
    app.run(debug=True)
