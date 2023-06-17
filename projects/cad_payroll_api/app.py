from flask import Flask, jsonify, request
from flask_api import status
import payroll_formulas as pf
import logging

app = Flask(__name__)

@app.route("/")
def home():
    data = request.get_json()
    # print(data["test"])
    return jsonify(data)

# you have all the pieces for this. build it out fully
@app.route("/payroll/cpp_contributions")
def cpp_contributions():
    json_body = request.get_json()
    print(json_body)
    print(type(json_body["test"]))
    print(type(json_body["test2"]))
    print(type(json_body["test3"]))
    #return jsonify({"message":"test"})
    return jsonify({"error_message":"too many records"}),status.HTTP_400_BAD_REQUEST
    # print(request.json)
    # print(request.json["hello"])
    # cpp = pf.cpp_contributions(0,0.0595,3500,3700,52,request.json["hello"])
    # return jsonify({"message":cpp})

@app.route("/payroll/ei_premiums")
def ei_premiums():
    return jsonify({"message":"test"})

@app.route("/payroll/payroll")
def payroll():
    return jsonify({"message":"test"})

if __name__ == "__main__":
    logging.basicConfig(filename=".\\projects\\cad_payroll_api\\logs.txt",format='%(asctime)s - %(message)s',level=logging.DEBUG)
    app.run(debug=True)
