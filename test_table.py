from flask import Flask
from flask_cors import CORS
from flask import request
from flask import jsonify
import requests
import gc
import json
from flask import Flask, render_template, flash, request
import pandas as pd
from pymongo import MongoClient


connection = MongoClient()
connection = MongoClient('localhost', 27017)
db = connection.test_database
collection = db.test_collection
print(collection)
for post in collection.find({}):
        print(post)