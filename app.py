from flask import Flask
from flask_restful import Api
from resources.emp import Emp

app=Flask(__name__)
app.config['PROPAGATE_EXCEPTIONS']=True
app.config['PREFERRED_URL_SCHEME']='https'
api=Api(app)

api.add_resource(Emp,'/emp')

if __name__ == "__main__":
    app.run()
