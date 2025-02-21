from flask import Flask, render_template
from ldap3 import Server, Connection, ALL

app = Flask(__name__)

LDAP_SERVER = 'ldap://seu-servidor'
LDAP_USER = 'seu-usuario@dominio.com'
LDAP_PASSWORD = 'sua-senha'
BASE_DN = 'DC=dominio,DC=com'

@app.route('/')
def index():
    server = Server(LDAP_SERVER, get_info=ALL)
    conn = Connection(server, LDAP_USER, LDAP_PASSWORD, auto_bind=True)
    conn.search(BASE_DN, '(objectClass=person)', attributes=['cn', 'mail'])
    users = conn.entries
    return render_template('index.html', users=users)

if __name__ == '__main__':
    app.run(debug=True)
