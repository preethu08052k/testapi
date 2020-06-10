from flask import Flask
from flask_restful import Api
from waitress import serve
from resources.emp import Emp

app=Flask(__name__)
app.config['PROPAGATE_EXCEPTIONS']=True
app.config['PREFERRED_URL_SCHEME']='https'
api=Api(app)

api.add_resource(Emp,'/emp')

serve(app,host='127.0.0.1',port=5000,url_scheme='https')
