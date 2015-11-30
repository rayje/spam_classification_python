# Spam Classification
A spam classification prototype

Requirements
------------
This prototype requires Python 3

Install
-----------

To install these libraries run the following command

Create a virtual environment using `virtualenv`
```
$ virtualenv -p python3 venv
$ source venv/bin/activate
```

Install libraries listed in requirements.txt
```
$ pip install -r requirements.txt
```

Download data
```
$ mkdir .data
$ ./getdata.sh
```
The above script will download a large set of email from the following sources:
- http://www.aueb.gr/users/ion/data/enron-spam/
- https://spamassassin.apache.org/publiccorpus/
