# Log Parser Application
Python 3 application that counts errors in logs file.

## Basic Usage

### Local Python Library Execution
You can execute only the library locally and provide a logs file to be parsed:
```
cd app
pip3 install -r requirements.txt
python3 parser.py log.txt
```
Theres a testing log file [here](app/log.txt).

### Run API locally
API can be run locally by installing the Flask library.
```
cd app
pip3 install -r requirements.txt
python3 api.py
```
API instructions can be found on its home page.

### Run Dockerized
Application can be run as a container too. Perform the following commands on the root directory to do so:
```
docker build -t log-parser .
docker run -p 5001:5000 -d log-parser
```
Now, you can access the API on [http://localhost:5001](http://localhost:5001).
