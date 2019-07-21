# test_aubergine

## coin change problem

To run coin change problem just run python coin_change.py

where Input An amount to make change for: 4

An array of integers representing available denominations: [1, 2, 3, 4]

## run django task

First create virtuenv of python with version 3.6
For that run following command but make sure you have virtualenv is installed on your system

$ virtualenv venv --python=python3.6

Then install all requirements using following command

$ pip install -r requirements.txt

Make sure you have installed Postgres in your system.
Then create "testproject db" in postgres. And create its user and password as "testuser" and "password" respectively.

After all setup run project using following command

$ python manage.py runserver