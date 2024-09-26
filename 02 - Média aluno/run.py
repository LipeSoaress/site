import os
from flask import Flask, render_template, request, redirect

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")
    
@app.route("/validar_notas", methods=['POST'])
def validar_notas():
    nome_aluno = request.form["nome_aluno"]
    notas_1 = float(request.form["nota1_aluno"])
    notas_2 = float(request.form["nota2_aluno"])
    notas_3 = float(request.form["nota3_aluno"])

    media = (notas_1 + notas_2 + notas_3) / 3

    if media >= 7:
        status = "Aprovado"
    elif media >= 3:
        status = "Recuperação"
    else:
        status = "Reprovado"
    
    caminho_arquivo = 'models/notas.txt'

    with open(caminho_arquivo, 'a') as arquivo:
        arquivo.write(f"{nome_aluno};{notas_1};{notas_2};{notas_3};{media};{status}\n")

    return redirect("/")

@app.route("/consulta")
def consulta_notas():
    notas = []
    caminho_arquivo = 'models/notas.txt'

    with open(caminho_arquivo, 'r') as arquivo:
        for linha in arquivo:
            item = linha.strip().split(';')
            if len(item) == 6:  # Verifica se a linha contém 5 elementos
                notas.append({
                    'nome': item[0],
                    'nota1': item[1],
                    'nota2': item[2],
                    'nota3': item[3],
                    'media': item[4],
                    'status': item[5]
                })
    return render_template("consulta_notas.html", prod=notas)

@app.route("/excluir_notas", methods=['GET'])
def excluir_notas():
    linha_para_excluir = int(request.args.get('linha')) 
    caminho_arquivo = 'models/notas.txt'
    
    with open(caminho_arquivo, 'r') as arquivo:
        linhas = arquivo.readlines()
    
    del linhas[linha_para_excluir]  

    with open(caminho_arquivo, 'w') as arquivo:
        arquivo.writelines(linhas)

    return redirect("/consulta") 

app.run(host='127.0.0.1', port=80, debug=True)

