# ---------------------------------------------------------------------------------------------------------------------
# ERROR LOGS PARSER API
# This a Flask REST API that works as an interface for executing the parser.py.
# Usage:
# /parselogs
#     GET - Provide logs_url param with url to your logs file.
#     POST - Provide your logs file in raw text as logs_file param.
# ---------------------------------------------------------------------------------------------------------------------

import flask
import requests
import parser
from flask import request, jsonify

app = flask.Flask(__name__)
app.config["DEBUG"] = True

# This method displays API usage to the user
@app.route('/', methods=['GET'])
def home():
    return (
        "<h1>Error Logs Parser API</h1>"
        "<h2>Usage:</h2>"
        "<p>Access <a href=/parselogs>parselogs</a>.</p>"
        "<p>GET - Provide <b>logs_url</b> param with url to your logs file.</p>"
        "<p>POST - Provide your logs file in raw text as <b>logs_file</b> param.</p>"
    )

# Process either the GET or POST methods
@app.route('/parselogs', methods=['GET', 'POST'])
def parse_logs():
    logs = ""
    report = ""

    # Get method sends a request to load the log file from the provided url
    if request.method == 'GET':
        if 'logs_url' in request.args:
            url = str(request.args['logs_url'])
        else:
            return "Error: No logs_url field provided. Please specify a logs_url."
        
        try:
            logs = requests.get(url).content.decode("utf-8")
            report = logs
        except ValueError as e: 
            print(e)
        except requests.exceptions.RequestException as e:
            print(e)

    # Post method reads on temp memory the provided file
    if request.method == 'POST':
        if 'logs_file' in request.files:
            logs = request.files['logs_file'].read().decode('utf-8')
        else:
            return "POST Error: No logs_file field provided. Please specify a logs_file."
    
    errors = parser.parse_errors(logs.splitlines())
    count = parser.count_errors(errors)
    report = parser.max_errors(count)
    report = report.replace("\n", "<p></p>")
        
    return f"<p>{report}</p>"

app.run(debug=True,host='0.0.0.0')