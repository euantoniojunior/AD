from flask import Flask, jsonify
from ldap3 import Server, Connection, ALL

# Configurações do servidor AD e do Flask
AD_SERVER = 'dc.dominio.local'  # Substituir pelo FQDN ou IP do controlador de domínio (exemplo: dc01.exemplo.local)
AD_USER = 'usuario@dominio.local'  # Substituir pelo usuário de autenticação no AD (exemplo: admin@exemplo.local)
AD_PASSWORD = 'senha'  # Substituir pela senha do usuário de autenticação no AD
AD_BASE_DN = 'DC=dominio,DC=local'  # Substituir pela base DN do domínio (exemplo: DC=exemplo,DC=local)

app = Flask(__name__)

@app.route('/ad_data')
def get_ad_data():
    try:
        # Conectando ao servidor AD
        server = Server(AD_SERVER, get_info=ALL)
        conn = Connection(server, AD_USER, AD_PASSWORD, auto_bind=True)

        # Consultar usuários
        conn.search(AD_BASE_DN, '(objectClass=user)', attributes=['cn'])
        users_count = len(conn.entries)

        # Consultar computadores
        conn.search(AD_BASE_DN, '(objectClass=computer)', attributes=['cn'])
        computers_count = len(conn.entries)

        # Fechar a conexão
        conn.unbind()

        # Retornar os resultados como JSON
        return jsonify({'usuarios': users_count, 'computadores': computers_count})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
