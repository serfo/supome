import os
import bcrypt
import datetime
from flask import Flask,request,jsonify,Response,make_response,session
from model import *

SERVER_PORT=6432

app=Flask(__name__)

app.secret_key=os.urandom(24)
app.permanent_session_lifetime=datetime.timedelta(days=30)


@app.route('/dash_app',methods=['POST'])
def config():
    data=request.get_json()
    user=sem.query(User).filter(User.username==data.get('username')).first()
    res={'op':False}
    if user==None:
        res={'op':False,',remark':'username is not exist.'}
        return jsonify(res)
    if not bcrypt.checkpw(data.get('password').encode('utf-8'), user.password.encode('utf-8')):
        res={'op':False,'remark':'password error.'}
        return jsonify(res)
    config={
        'token':sem.query(Token).filter(Token.username==user.username).first(),
        'nodes':sem.query(Node).all(),
        'proxies':sem.query(Proxie).filter(Proxie.username==user.username).all()
    }
    res['config']=dict([(k,model_to_dict(v)) for k,v in config.items()])
    res['op']=True
    print('generate config success.')
    return jsonify(res)

if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0',port=SERVER_PORT,threading=True)

