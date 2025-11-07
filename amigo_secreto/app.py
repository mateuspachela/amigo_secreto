import random
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS # Importante para plataformas como o Render

# --- Configuração do Amigo Secreto ---

# 1. Lista de participantes
participants = [
    "Pedro", "Italo", "Enzo", "Luiza", "Japa", "Pachela", 
    "Fernanda", "Luigi", "Juliana", "Gabi prado", "joao Caprio", 
    "vicentin", "duda p"
]

def create_assignments(names):
    """
    Sorteia os pares de amigo secreto, garantindo
    que ninguém tire a si mesmo.
    """
    receivers = names[:]  # Cria uma cópia da lista
    assignments = {}
    
    # Continua embaralhando até que não haja auto-atribuições
    while True:
        random.shuffle(receivers)
        
        # Verifica se alguém tirou a si mesmo
        valid = True
        for i in range(len(names)):
            if names[i] == receivers[i]:
                valid = False
                break
        
        # Se a combinação for válida, sai do loop
        if valid:
            break
            
    # Cria o dicionário final de "quem tirou quem"
    assignments = {giver: receiver for giver, receiver in zip(names, receivers)}
    return assignments

# --- Fim da Configuração ---


# Cria a aplicação Flask
app = Flask(__name__)
# Habilita o CORS (necessário para o frontend e backend conversarem)
CORS(app)

# Sorteia os amigos UMA VEZ quando o servidor inicia
# O resultado ficará na memória
secret_santa_map = create_assignments(participants)

# Para depuração (você pode ver isso nos logs do Render)
print("--- SORTEIO REALIZADO ---")
print(secret_santa_map)
print("--------------------------")


# Rota 1: Servir a página principal (Frontend)
@app.route('/')
def index():
    """
    Carrega o arquivo index.html e passa a lista de 
    participantes para o dropdown.
    """
    return render_template('index.html', participants=participants)


# Rota 2: A "API" que revela o amigo secreto
@app.route('/get-assignment')
def get_assignment():
    """
    Recebe um nome (ex: ?name=Pedro) e retorna
    quem essa pessoa tirou em JSON.
    """
    name = request.args.get('name')
    
    if name in secret_santa_map:
        friend = secret_santa_map[name]
        # Retorna o resultado como JSON
        return jsonify({'secret_friend': friend})
    elif name:
        return jsonify({'error': 'Nome não encontrado na lista.'}), 404
    else:
        return jsonify({'error': 'Nome não fornecido.'}), 400

# Necessário para rodar no Render (ele usará um servidor Gunicorn)
if __name__ == '__main__':
    # '0.0.0.0' torna o servidor acessível na rede
    # O Render fornecerá sua própria PORTA
    app.run(host='0.0.0.0', port=5000)