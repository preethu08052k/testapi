from flask_restful import Resource,reqparse
from werkzeug.security import safe_str_cmp
from flask_jwt_extended import create_access_token,jwt_required
from db import query

class Emp(Resource):
    @jwt_required
    def get(self):
        parser=reqparse.RequestParser()
        parser.add_argument('empno',type=int,required=True,help="empno cannot be left blank!")
        data=parser.parse_args()
        try:
            return query(f"""SELECT * FROM testapi.emp WHERE empno={data['empno']}""")
        except:
            return {"message":"There was an error connecting to emp table."},500

    @jwt_required
    def post(self):
        parser=reqparse.RequestParser()
        parser.add_argument('empno',type=int,required=True,help="empno cannot be left blank!")
        parser.add_argument('ename',type=str,required=True,help="empname cannot be left blank!")
        parser.add_argument('job',type=str,required=True,help="job cannot be left blank!")
        parser.add_argument('mgr',type=int,required=True,help="mgr cannot be left blank!")
        parser.add_argument('hiredate',type=str,required=True,help="hiredate cannot be left blank!")
        parser.add_argument('sal',type=str,required=True,help="sal cannot be left blank!")
        parser.add_argument('comm',type=str)
        parser.add_argument('deptno',type=int,required=True,help="deptno cannot be left blank!")
        parser.add_argument('pass',type=str,required=True,help="password cannot be left blank!")
        data=parser.parse_args()
        try:
            x=query(f"""SELECT * FROM testapi.emp WHERE empno={data['empno']}""",return_json=False)
            if len(x)>0: return {"message":"An emp with that empno already exists."},400
        except:
            return {"message":"There was an error inserting into emp table."},500
        if data['comm']!=None:
            try:
                query(f"""INSERT INTO testapi.emp VALUES({data['empno']},
                                                        '{data['ename']}',
                                                        '{data['job']}',
                                                        {data['mgr']},
                                                        '{data['hiredate']}',
                                                        '{data['sal']}',
                                                        '{data['comm']}',
                                                        {data['deptno']},
                                                        '{data['pass']}')""")
            except:
                return {"message":"There was an error inserting into emp table."},500
            return {"message":"Successfully Inserted."},201
        else:
            try:
                query(f"""INSERT INTO testapi.emp (empno,ename,job,mgr,hiredate,sal,deptno,pass)
                                                    VALUES({data['empno']},
                                                        '{data['ename']}',
                                                        '{data['job']}',
                                                        {data['mgr']},
                                                        '{data['hiredate']}',
                                                        '{data['sal']}',
                                                        {data['deptno']},
                                                        '{data['pass']}')""")
            except:
                return {"message":"There was an error inserting into emp table."},500
            return {"message":"Successfully Inserted."},201

class User():
    def __init__(self,empno,ename,password):
        self.empno=empno
        self.ename=ename
        self.password=password

    @classmethod
    def getUserByEname(cls,ename):
        result=query(f"""SELECT empno,ename,pass FROM emp WHERE ename='{ename}'""",return_json=False)
        if len(result)>0: return User(result[0]['empno'],result[0]['ename'],result[0]['pass'])
        return None

    @classmethod
    def getUserByempno(cls,empno):
        result=query(f"""SELECT empno,ename,pass FROM emp WHERE empno='{empno}'""",return_json=False)
        if len(result)>0: return User(result[0]['empno'],result[0]['ename'],result[0]['pass'])
        return None

class EmpLogin(Resource):
    def post(self):
        parser=reqparse.RequestParser()
        parser.add_argument('ename',type=str,required=True,help="empname cannot be left blank!")
        parser.add_argument('pass',type=str,required=True,help="password cannot be left blank!")
        data=parser.parse_args()
        user=User.getUserByEname(data['ename'])
        if user and safe_str_cmp(user.password,data['pass']):
            access_token=create_access_token(identity=user.empno,expires_delta=False)
            return {'access_token':access_token},200
        return {"message":"Invalid Credentials!"}, 401
