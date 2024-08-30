from flask import Flask, jsonify, request
from config import config
from flask_mysqldb import MySQL  

app = Flask(__name__) 

con = MySQL(app)  

@app.route('/users',methods = ['GET'])
def index(): 
    try:    
        cursor = con.connection.cursor()
        sql = 'SELECT * FROM user' 
        cursor.execute(sql)
        datum = cursor.fetchall() 
        list_of_user  = []
        for user in datum:
            user_entity = {'user_id': user[0],'user_first_name':user[1],
            'user_last_name':user[2] , 'user_name':user[3] , 
            'user_password':user[4] , 'user_role':user[5] 
            }
            list_of_user.append(user_entity)

        return jsonify({'user':list_of_user})#,'error_message':'liste des utilisateurs'
    except Exception as ex:
        return jsonify({'error_casching':'cet utilisateur n\existe pas'})

@app.route('/users/<user_id>',methods= ['GET'])
def get_single_user(user_id):
    try:    
        cursor = con.connection.cursor()
        sql = "SELECT * FROM user WHERE user_id = '{0}'" .format(user_id) 
        cursor.execute(sql)
        datum = cursor.fetchone()  
        if datum != None:
            user_entity = {'user_id':datum[0],'user_first_name':datum[1],
            'user_last_name':datum[2] , 'user_name':datum[3] , 
            'user_password':datum[4] , 'user_role':datum[5] 
            }
            return jsonify({'user':user_entity,'error_message':"user est présent"}) 
        else:
            return jsonify({'error_message':'cet utilisateur n\'existe pas'}) 
    except:
          return jsonify({'error_casching':'une erreur s\'est produite'})

@app.route('/users',methods = ['POST'])
def register_user():
    try:
        cursor = con.connection.cursor()
        sql = """
        INSERT INTO user (user_id, user_first_name, user_last_name, user_name, user_password, user_role)
        VALUES('{0}', '{1}', '{2}','{3}','{4}','{5}')
        """.format(request.json['user_id'], request.json['user_first_name'], request.json['user_last_name'],
        request.json['user_name'], request.json['user_password'], request.json['user_role'],)
        cursor.execute(sql)
        con.connection.commit()
        return jsonify({'error_message':'enregistrez avec succès'}) 
    except:
        return jsonify({'error_casching':'une erreur s\'est produite durant la sauvegarde'})

@app.route('/users/<user_id>',methods = ['PUT']) 
def update_user(user_id):
    cursor = con.connection.cursor()
    try:
        cursor = con.connection.cursor()
        sql = """
        UPDATE user SET user_first_name = '{1}',user_last_name = '{2}',user_name = '{3}',
        user_password = '{4}',user_role = '{5}'""".format(request.json['user_first_name'], request.json['user_last_name'],
        request.json['user_name'], request.json['user_password'], request.json['user_role'],user_id)
        cursor.execute(sql)
        con.connection.commit()
        return jsonify({'error_message':'modifier avec succès'}) 
    except:
        return jsonify({'error_casching':'une erreur s\'est produite dlors de la modification'})


@app.route('/users/<user_id>',methods = ['DELETE']) 
def delete_user(user_id):
    try:
        cursor = con.connection.cursor()
        sql = "DELETE FROM user WHERE user_id = '{0}'".format(user_id)
        cursor.execute(sql)
        con.connection.commit()
        return jsonify({'error_message':'supprimé avec succès'}) 
    except:
        return jsonify({'error_casching':'une erreur s\'est produite lors de la suppression'})
        
def page_no_found(error):
    return '<h1>La page recherché n\'existe pas</h1>'

if __name__=='__main__':
    app.config.from_object(config['development'])
    app.register_error_handler(404, page_no_found) 
    app.run(host ='0.0.0.0', port = 3000)