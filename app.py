from flask import Flask, render_template, request, jsonify, redirect, url_for
import json
import os
import uuid

app = Flask(__name__)


def carregar_usuarios():
    try:
        if os.path.exists('usuarios.json'):
            with open('usuarios.json', 'r', encoding='utf-8') as arquivo:
                return json.load(arquivo)
        else:
            return []
    except:
        return []



def deletar_usuario(id):
    usuarios = carregar_usuarios()
    usuarios_filtrados = [usuario for usuario in usuarios if usuario.get("id") != id]

    if len(usuarios) == len(usuarios_filtrados):
        return False
    
    try:
        with open("usuarios.json", "w", encoding="utf-8") as arquivo:
            json.dump(usuarios_filtrados, arquivo, indent=4)
        return True
    except:
        return False


def salvar_usuario(usuario):
    usuarios = carregar_usuarios()
    try:
        usuarios.append(usuario)
        with open('usuarios.json', 'w', encoding='utf-8') as arquivo:
            json.dump(usuarios, arquivo, indent=4, ensure_ascii=False)
        return True
    except:
        return False


@app.route("/")
def home():
    return render_template("formulário.html")


@app.route("/cadastro-usuario", methods=["POST"])
def cadastrar_usuario():
    nome = request.form.get("nome")
    cpf = request.form.get("cpf")
    email = request.form.get("email")
    idade = request.form.get("idade")
    senha = request.form.get("senha")

    usuario = {
        "id": str(uuid.uuid4()),
        "nome": nome,
        "cpf": cpf,
        "email": email,
        "idade": idade,
        "senha": senha
    }
    
    status = salvar_usuario(usuario)

    if status:
        return render_template("cadastro_realizado.html", usuario=usuario["nome"])
    else:
        return "Não foi possível realizar o cadastro!"


@app.route("/usuarios/json")
def listar_usuarios_json():
    usuarios_json = carregar_usuarios()
    return jsonify(usuarios_json)


@app.route("/usuarios/html")
def listar_usuarios_html():
    usuarios_tabela = carregar_usuarios()
    return render_template("usuarios_tabela.html", usuarios=usuarios_tabela)


@app.route("/usuarios/completo")
def usuarios_completo():
    usuarios = carregar_usuarios()  
    usuarios_json = json.dumps(usuarios, indent=4, ensure_ascii=False)
    return render_template("usuarios_com_json_e_tabela.html", usuarios=usuarios, usuarios_json=usuarios_json)


@app.route("/usuarios/<id>", methods=["DELETE"])
def excluir_usuario(id):
    sucesso = deletar_usuario(id)

    if sucesso:
        return jsonify({"mensagem": f"Usuário deletado com sucesso"}), 200
    else:
        return jsonify({"erro": f"Usuário não encontrado"}), 404


@app.route("/usuarios/", methods=["PUT"])
def atualizar_usuario():
    usuario_edit = request.get_json()
    usuario_edit = dict(usuario_edit)
    usuarios = carregar_usuarios()

    for usuario in usuarios:
        if usuario.get("id") == usuario_edit.get("id"):
            usuario.update(usuario_edit)
            break
    
    try:
        with open("usuarios.json", "w", encoding="utf-8") as arquivo:
            json.dump(usuarios, arquivo, indent=4)

        return jsonify({"mensagem": "Usuário atualizado com sucesso!"}), 200
    except:
        return jsonify({"mensagem": "Não foi possível salvar as modificações!"}), 404

if __name__ == '__main__':
    app.run(debug=True)
