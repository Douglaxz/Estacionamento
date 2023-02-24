# importação de dependencias
from datetime import datetime, date
from flask import Flask, render_template, request, redirect, session, flash, url_for, send_from_directory,send_file
from flask_qrcode import QRcode
import time
from datetime import date, timedelta
from estacionamento import app, db
from models import tb_user,\
    tb_usertype,\
    tb_tipoveiculo,\
    tb_marcaveiculo,\
    tb_veiculo,\
    tb_preco,\
    tb_tipopagamento,\
    tb_estacionamento

from helpers import \
    frm_pesquisa, \
    frm_editar_senha,\
    frm_editar_usuario,\
    frm_visualizar_usuario, \
    frm_visualizar_tipousuario,\
    frm_editar_tipousuario,\
    frm_editar_tipoveiculo,\
    frm_visualizar_tipoveiculo,\
    frm_editar_marcaveiculo,\
    frm_visualizar_marcaveiculo,\
    frm_editar_veiculo,\
    frm_visualizar_veiculo,\
    frm_editar_preco,\
    frm_visualizar_preco,\
    frm_editar_tipopagamento,\
    frm_visualizar_tipopagamento,\
    frm_editar_estacionamento,\
    frm_visualizar_estacionamento,\
    frm_editar_estacionamento_entrada,\
    frm_editar_estacionamento_finalizar


# ITENS POR PÁGINA
from config import ROWS_PER_PAGE, CHAVE
from flask_bcrypt import generate_password_hash, Bcrypt, check_password_hash

import string
import random
import numbers

##################################################################################################################################
#GERAL
##################################################################################################################################


@app.route("/qrcode", methods=["GET"])
def get_qrcode():
    # please get /qrcode?data=<qrcode_data>
    data = request.args.get("data", "")
    return send_file(qrcode(data, mode="raw"), mimetype="image/png")

#---------------------------------------------------------------------------------------------------------------------------------
#ROTA: index
#FUNÇÃO: redirecionar para página principal
#PODE ACESSAR: todos os usuários
#---------------------------------------------------------------------------------------------------------------------------------
@app.route('/')
def index():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login'))        
    return render_template('index.html', titulo='Bem vindos')

#---------------------------------------------------------------------------------------------------------------------------------
#ROTA: logout
#FUNÇÃO: remover dados de sessão e deslogar ususários
#PODE ACESSAR: todos os usuários
#---------------------------------------------------------------------------------------------------------------------------------
@app.route('/logout', methods = ['GET', 'POST'])
def logout():
    session['usuario_logado'] = None
    flash('Logout efetuado com sucesso','success')
    return redirect(url_for('login'))

#---------------------------------------------------------------------------------------------------------------------------------
#ROTA: login
#FUNÇÃO: direcionar para formulário de login
#PODE ACESSAR: todos os usuários
#---------------------------------------------------------------------------------------------------------------------------------
@app.route('/login')
def login():
    return render_template('login.html')

#---------------------------------------------------------------------------------------------------------------------------------
#ROTA: autenticar
#FUNÇÃO: autenticar usuário
#PODE ACESSAR: todos os usuários
#---------------------------------------------------------------------------------------------------------------------------------
@app.route('/autenticar', methods = ['GET', 'POST'])
def autenticar():
    usuario = tb_user.query.filter_by(login_user=request.form['usuario']).first()
    senha = check_password_hash(usuario.password_user,request.form['senha'])
    if usuario:
        if senha:
            session['usuario_logado'] = usuario.login_user
            session['nomeusuario_logado'] = usuario.name_user
            session['tipousuario_logado'] = usuario.cod_usertype
            session['coduser_logado'] = usuario.cod_user
            flash(usuario.name_user + ' Usuário logado com sucesso','success')
            #return redirect('/')
            return redirect('/')
        else:
            flash('Verifique usuário e senha', 'danger')
            return redirect(url_for('login'))
    else:
        flash('Usuário não logado com sucesso','success')
        return redirect(url_for('login'))

##################################################################################################################################
#USUARIOS
##################################################################################################################################

#---------------------------------------------------------------------------------------------------------------------------------
#ROTA: usuario
#FUNÇÃO: tela do sistema para mostrar os usuários cadastrados
#PODE ACESSAR: usuários do tipo administrador
#---------------------------------------------------------------------------------------------------------------------------------
@app.route('/usuario', methods=['POST','GET'])
def usuario():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        flash('Sessão expirou, favor logar novamente','danger')
        return redirect(url_for('login',proxima=url_for('usuario')))        
    form = frm_pesquisa()
    page = request.args.get('page', 1, type=int)
    pesquisa = form.pesquisa.data
    if pesquisa == "":
        pesquisa = form.pesquisa_responsiva.data

    if pesquisa == "" or pesquisa == None:    
        usuarios = tb_user.query\
        .join(tb_usertype, tb_usertype.cod_usertype==tb_user.cod_usertype)\
        .add_columns(tb_user.login_user, tb_user.cod_user, tb_user.name_user, tb_user.status_user, tb_usertype.desc_usertype)\
        .order_by(tb_user.name_user)\
        .paginate(page=page, per_page=ROWS_PER_PAGE, error_out=False)
    else:
        usuarios = tb_user.query\
        .filter(tb_user.name_user.ilike(f'%{pesquisa}%'))\
        .join(tb_usertype, tb_usertype.cod_usertype==tb_user.cod_usertype)\
        .add_columns(tb_user.login_user, tb_user.cod_user, tb_user.name_user, tb_user.status_user, tb_usertype.desc_usertype)\
        .order_by(tb_user.name_user)\
        .paginate(page=page, per_page=ROWS_PER_PAGE, error_out=False)


    return render_template('usuarios.html', titulo='Usuários', usuarios=usuarios, form=form)

#---------------------------------------------------------------------------------------------------------------------------------
#ROTA: novoUsuario
#FUNÇÃO: mostrar o formulário de cadastro de usuário
#PODE ACESSAR: usuários do tipo administrador
#--------------------------------------------------------------------------------------------------------------------------------- 
@app.route('/novoUsuario')
def novoUsuario():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        flash('Sessão expirou, favor logar novamente','danger')
        return redirect(url_for('login',proxima=url_for('novoUsuario')))     
    form = frm_editar_usuario()
    return render_template('novoUsuario.html', titulo='Novo Usuário', form=form)

#---------------------------------------------------------------------------------------------------------------------------------
#ROTA: criarUsuario
#FUNÇÃO: inserir informações do usuário no banco de dados
#PODE ACESSAR: usuários do tipo administrador
#--------------------------------------------------------------------------------------------------------------------------------- 
@app.route('/criarUsuario', methods=['POST',])
def criarUsuario():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login',proxima=url_for('criarUsuario')))      
    form = frm_editar_usuario(request.form)
    if not form.validate_on_submit():
        flash('Por favor, preencha todos os dados','danger')
        return redirect(url_for('novoUsuario'))
    nome  = form.nome.data
    status = form.status.data
    login = form.login.data
    tipousuario = form.tipousuario.data
    email = form.email.data
    #criptografar senha
    senha = generate_password_hash("teste@12345").decode('utf-8')
    usuario = tb_user.query.filter_by(name_user=nome).first()
    if usuario:
        flash ('Usuário já existe','danger')
        return redirect(url_for('index')) 
    novoUsuario = tb_user(name_user=nome, status_user=status, login_user=login, cod_usertype=tipousuario, password_user=senha, email_user=email)
    db.session.add(novoUsuario)
    db.session.commit()
    flash('Usuário criado com sucesso','success')
    return redirect(url_for('usuario'))

#---------------------------------------------------------------------------------------------------------------------------------
#ROTA: criarUsuarioexterno - NÃO DISPONIVEL NESTA VERSAL
#FUNÇÃO: inserir informações do usuário no banco de dados realizam cadastro pela área externa
#PODE ACESSAR: novos usuários
#---------------------------------------------------------------------------------------------------------------------------------
@app.route('/criarUsuarioexterno', methods=['POST',])
def criarUsuarioexterno():    
    nome  = request.form['nome']
    status = 0
    email = request.form['email']
    localarroba = email.find("@")
    login = email[0:localarroba]
    tipousuario = 2
    #criptografar senha
    senha = generate_password_hash(request.form['senha']).decode('utf-8')
    usuario = tb_user.query.filter_by(name_user=nome).first()
    if usuario:
        flash ('Usuário já existe','danger')
        return redirect(url_for('login')) 
    novoUsuario = tb_user(name_user=nome, status_user=status, login_user=login, cod_usertype=tipousuario, password_user=senha, email_user=email)
    db.session.add(novoUsuario)
    db.session.commit()
    flash('Usuário criado com sucesso, favor logar com ele','success')
    return redirect(url_for('login'))  

#---------------------------------------------------------------------------------------------------------------------------------
#ROTA: visualizarUsuario
#FUNÇÃO: mostrar formulário de visualização dos usuários cadastrados
#PODE ACESSAR: usuários do tipo administrador
#--------------------------------------------------------------------------------------------------------------------------------- 
@app.route('/visualizarUsuario/<int:id>')
def visualizarUsuario(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        flash('Sessão expirou, favor logar novamente','danger')
        return redirect(url_for('login',proxima=url_for('visualizarUsuario')))    
    usuario = tb_user.query.filter_by(cod_user=id).first()
    form = frm_visualizar_usuario()
    form.nome.data = usuario.name_user
    form.status.data = usuario.status_user
    form.login.data = usuario.login_user
    form.tipousuario.data = usuario.cod_usertype
    form.email.data = usuario.email_user
    return render_template('visualizarUsuario.html', titulo='Visualizar Usuário', id=id, form=form)   

#---------------------------------------------------------------------------------------------------------------------------------
#ROTA: editarUsuario
#FUNÇÃO: mostrar formulário de edição dos usuários cadastrados
#PODE ACESSAR: usuários do tipo administrador
#--------------------------------------------------------------------------------------------------------------------------------- 
@app.route('/editarUsuario/<int:id>')
def editarUsuario(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        flash('Sessão expirou, favor logar novamente','danger')
        return redirect(url_for('login',proxima=url_for('editarUsuario/<int:id>')))  
    usuario = tb_user.query.filter_by(cod_user=id).first()
    form = frm_editar_usuario()
    form.nome.data = usuario.name_user
    form.status.data = usuario.status_user
    form.login.data = usuario.login_user
    form.tipousuario.data = usuario.cod_usertype
    form.email.data = usuario.email_user
    return render_template('editarUsuario.html', titulo='Editar Usuário', id=id, form=form)    
       
#---------------------------------------------------------------------------------------------------------------------------------
#ROTA: atualizarUsuario
#FUNÇÃO: alterar as informações dos usuários no banco de dados
#PODE ACESSAR: usuários do tipo administrador
#---------------------------------------------------------------------------------------------------------------------------------
@app.route('/atualizarUsuario', methods=['POST',])
def atualizarUsuario():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        flash('Sessão expirou, favor logar novamente','danger')
        return redirect(url_for('login',proxima=url_for('atualizarUsuario')))          
    form = frm_editar_usuario(request.form)
    if not form.validate_on_submit():
        flash('Por favor, preencha todos os dados','danger')
        return redirect(url_for('atualizarUsuario'))
    id = request.form['id']
    usuario = tb_user.query.filter_by(cod_user=request.form['id']).first()
    usuario.name_user = form.nome.data
    usuario.status_user = form.status.data
    usuario.login_user = form.login.data
    usuario.cod_uertype = form.tipousuario.data
    db.session.add(usuario)
    db.session.commit()
    flash('Usuário alterado com sucesso','success')
    return redirect(url_for('visualizarUsuario', id=request.form['id']))

#---------------------------------------------------------------------------------------------------------------------------------
#ROTA: editarSenhaUsuario
#FUNÇÃO: formulário para edição da tela do usuário
#PODE ACESSAR: usuários do tipo administrador
#---------------------------------------------------------------------------------------------------------------------------------
@app.route('/editarSenhaUsuario/')
def editarSenhaUsuario():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        flash('Sessão expirou, favor logar novamente','danger')
        return redirect(url_for('login',proxima=url_for('visualizarUsuario')))    
    form = frm_editar_senha()
    return render_template('trocarsenha.html', titulo='Trocar Senha', id=id, form=form)  

#---------------------------------------------------------------------------------------------------------------------------------
#ROTA: trocarSenhaUsuario
#FUNÇÃO: alteração da senha do usuário no banco de dados
#PODE ACESSAR: usuários do tipo administrador
#---------------------------------------------------------------------------------------------------------------------------------
@app.route('/trocarSenhaUsuario', methods=['POST',])
def trocarSenhaUsuario():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        flash('Sessão expirou, favor logar novamente','danger')
        return redirect(url_for('login',proxima=url_for('atualizarUsuario')))          
    form = frm_editar_senha(request.form)
    if form.validate_on_submit():
        id = session['coduser_logado']
        usuario = tb_user.query.filter_by(cod_user=id).first()
        if form.senhaatual.data != usuario.password_user:
            flash('senha atual incorreta','danger')
            return redirect(url_for('editarSenhaUsuario'))

        if form.senhaatual.data != usuario.password_user:
            flash('senha atual incorreta','danger')
            return redirect(url_for('editarSenhaUsuario')) 

        if form.novasenha1.data != form.novasenha2.data:
            flash('novas senhas não coincidem','danger')
            return redirect(url_for('editarSenhaUsuario')) 
        usuario.password_user = generate_password_hash(form.novasenha1.data).decode('utf-8')
        db.session.add(usuario)
        db.session.commit()
        flash('senha alterada com sucesso!','success')
    else:
        flash('senha não alterada!','danger')
    return redirect(url_for('editarSenhaUsuario')) 

##################################################################################################################################
#TIPO DE USUARIOS
##################################################################################################################################

#---------------------------------------------------------------------------------------------------------------------------------
#ROTA: tipousuario
#FUNÇÃO: tela do sistema para mostrar os tipos de usuários cadastrados
#PODE ACESSAR: usuários do tipo administrador
#---------------------------------------------------------------------------------------------------------------------------------
@app.route('/tipousuario', methods=['POST','GET'])
def tipousuario():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        flash('Sessão expirou, favor logar novamente','danger')
        return redirect(url_for('login',proxima=url_for('tipousuario')))         
    page = request.args.get('page', 1, type=int)
    form = frm_pesquisa()   
    pesquisa = form.pesquisa.data
    if pesquisa == "":
        pesquisa = form.pesquisa_responsiva.data
    
    if pesquisa == "" or pesquisa == None:     
        tiposusuario = tb_usertype.query.order_by(tb_usertype.desc_usertype)\
        .paginate(page=page, per_page=ROWS_PER_PAGE , error_out=False)
    else:
        tiposusuario = tb_usertype.query.order_by(tb_usertype.desc_usertype)\
        .filter(tb_usertype.desc_usertype.ilike(f'%{pesquisa}%'))\
        .paginate(page=page, per_page=ROWS_PER_PAGE, error_out=False)        
    return render_template('tipousuarios.html', titulo='Tipo Usuário', tiposusuario=tiposusuario, form=form)

#---------------------------------------------------------------------------------------------------------------------------------
#ROTA: novoTipoUsuario
#FUNÇÃO: mostrar o formulário de cadastro de tipo de usuário
#PODE ACESSAR: usuários do tipo administrador
#---------------------------------------------------------------------------------------------------------------------------------
@app.route('/novoTipoUsuario')
def novoTipoUsuario():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        flash('Sessão expirou, favor logar novamente','danger')
        return redirect(url_for('login',proxima=url_for('novoTipoUsuario'))) 
    form = frm_editar_tipousuario()
    return render_template('novoTipoUsuario.html', titulo='Novo Tipo Usuário', form=form)

#---------------------------------------------------------------------------------------------------------------------------------
#ROTA: criarTipoUsuario
#FUNÇÃO: inserir informações do tipo de usuário no banco de dados
#PODE ACESSAR: usuários do tipo administrador
#--------------------------------------------------------------------------------------------------------------------------------- 
@app.route('/criarTipoUsuario', methods=['POST',])
def criarTipoUsuario():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        flash('Sessão expirou, favor logar novamente','danger')
        return redirect(url_for('login',proxima=url_for('criarTipoUsuario')))     
    form = frm_editar_tipousuario(request.form)
    if not form.validate_on_submit():
        flash('Por favor, preencha todos os dados','danger')
        return redirect(url_for('criarTipoUsuario'))
    desc  = form.descricao.data
    status = form.status.data
    tipousuario = tb_usertype.query.filter_by(desc_usertype=desc).first()
    if tipousuario:
        flash ('Tipo Usuário já existe','danger')
        return redirect(url_for('tipousuario')) 
    novoTipoUsuario = tb_usertype(desc_usertype=desc, status_usertype=status)
    flash('Tipo de usuário criado com sucesso!','success')
    db.session.add(novoTipoUsuario)
    db.session.commit()
    return redirect(url_for('tipousuario'))

#---------------------------------------------------------------------------------------------------------------------------------
#ROTA: visualizarTipoUsuario
#FUNÇÃO: mostrar formulário de visualização dos tipos de usuários cadastrados
#PODE ACESSAR: usuários do tipo administrador
#--------------------------------------------------------------------------------------------------------------------------------- 
@app.route('/visualizarTipoUsuario/<int:id>')
def visualizarTipoUsuario(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        flash('Sessão expirou, favor logar novamente','danger')
        return redirect(url_for('login',proxima=url_for('visualizarTipoUsuario')))  
    tipousuario = tb_usertype.query.filter_by(cod_usertype=id).first()
    form = frm_visualizar_tipousuario()
    form.descricao.data = tipousuario.desc_usertype
    form.status.data = tipousuario.status_usertype
    return render_template('visualizarTipoUsuario.html', titulo='Visualizar Tipo Usuário', id=id, form=form)   

#---------------------------------------------------------------------------------------------------------------------------------
#ROTA: editarTipoUsuario
##FUNÇÃO: mostrar formulário de edição dos tipos de usuários cadastrados
#PODE ACESSAR: usuários do tipo administrador
#---------------------------------------------------------------------------------------------------------------------------------
@app.route('/editarTipoUsuario/<int:id>')
def editarTipoUsuario(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        flash('Sessão expirou, favor logar novamente','danger')
        return redirect(url_for('login',proxima=url_for('editarTipoUsuario')))  
    tipousuario = tb_usertype.query.filter_by(cod_usertype=id).first()
    form = frm_editar_tipousuario()
    form.descricao.data = tipousuario.desc_usertype
    form.status.data = tipousuario.status_usertype
    return render_template('editarTipoUsuario.html', titulo='Editar Tipo Usuário', id=id, form=form)   

#---------------------------------------------------------------------------------------------------------------------------------
#ROTA: atualizarTipoUsuario
#FUNÇÃO: alterar as informações dos tipos de usuários no banco de dados
#PODE ACESSAR: usuários do tipo administrador
#---------------------------------------------------------------------------------------------------------------------------------
@app.route('/atualizarTipoUsuario', methods=['POST',])
def atualizarTipoUsuario():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        flash('Sessão expirou, favor logar novamente','danger')
        return redirect(url_for('login',proxima=url_for('atualizarTipoUsuario')))      
    form = frm_editar_tipousuario(request.form)
    if form.validate_on_submit():
        id = request.form['id']
        tipousuario = tb_usertype.query.filter_by(cod_usertype=request.form['id']).first()
        tipousuario.desc_usertype = form.descricao.data
        tipousuario.status_usertype = form.status.data
        db.session.add(tipousuario)
        db.session.commit()
        flash('Tipo de usuário atualizado com sucesso!','success')
    else:
        flash('Favor verificar os campos!','danger')
    return redirect(url_for('visualizarTipoUsuario', id=request.form['id']))    


##################################################################################################################################
#TIPO DE VEÍCULOS
##################################################################################################################################

#---------------------------------------------------------------------------------------------------------------------------------
#ROTA: tipoveiculo
#FUNÇÃO: tela do sistema para mostrar os tipos de veículos cadastrados
#PODE ACESSAR: usuários do tipo administrador
#---------------------------------------------------------------------------------------------------------------------------------
@app.route('/tipoveiculo', methods=['POST','GET'])
def tipoveiculo():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        flash('Sessão expirou, favor logar novamente','danger')
        return redirect(url_for('login',proxima=url_for('tipoveiculos')))         
    page = request.args.get('page', 1, type=int)
    form = frm_pesquisa()   
    pesquisa = form.pesquisa.data
    if pesquisa == "":
        pesquisa = form.pesquisa_responsiva.data
    
    if pesquisa == "" or pesquisa == None:     
        tiposveiculo = tb_tipoveiculo.query.order_by(tb_tipoveiculo.desc_tipoveiculo)\
        .paginate(page=page, per_page=ROWS_PER_PAGE , error_out=False)
    else:
        tiposveiculo = tb_tipoveiculo.query.order_by(tb_tipoveiculo.desc_tipoveiculo)\
        .filter(tb_tipoveiculo.desc_tipoveiculos.ilike(f'%{pesquisa}%'))\
        .paginate(page=page, per_page=ROWS_PER_PAGE, error_out=False)        
    return render_template('tipoveiculo.html', titulo='Tipo Veículo', tiposveiculo=tiposveiculo, form=form)

#---------------------------------------------------------------------------------------------------------------------------------
#ROTA: novoTipoVeiculo
#FUNÇÃO: mostrar o formulário de cadastro de tipo de veículo
#PODE ACESSAR: usuários do tipo administrador
#---------------------------------------------------------------------------------------------------------------------------------
@app.route('/novoTipoVeiculo')
def novoTipoVeiculo():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        flash('Sessão expirou, favor logar novamente','danger')
        return redirect(url_for('login',proxima=url_for('novoTipoVeiculo'))) 
    form = frm_editar_tipoveiculo()
    return render_template('novoTipoVeiculo.html', titulo='Novo Tipo Veiculo', form=form)

#---------------------------------------------------------------------------------------------------------------------------------
#ROTA: criarTipoVeiculo
#FUNÇÃO: inserir informações do tipo de veículos no banco de dados
#PODE ACESSAR: usuários do tipo administrador
#--------------------------------------------------------------------------------------------------------------------------------- 
@app.route('/criarTipoVeiculo', methods=['POST',])
def criarTipoVeiculo():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        flash('Sessão expirou, favor logar novamente','danger')
        return redirect(url_for('login',proxima=url_for('criarTipoVeiculo')))     
    form = frm_editar_tipoveiculo(request.form)
    if not form.validate_on_submit():
        flash('Por favor, preencha todos os dados','danger')
        return redirect(url_for('criarTipoVeiculo'))
    desc  = form.descricao.data
    status = form.status.data
    tipoveiculo = tb_tipoveiculo.query.filter_by(desc_tipoveiculo=desc).first()
    if tipoveiculo:
        flash ('Tipo Veículo já existe','danger')
        return redirect(url_for('tipoveiculo')) 
    novoTipoVeiculo = tb_tipoveiculo(desc_tipoveiculo=desc, status_tipoveiculo=status)
    flash('Tipo de novoTipoVeiculo criado com sucesso!','success')
    db.session.add(novoTipoVeiculo)
    db.session.commit()
    return redirect(url_for('tipoveiculo'))

#---------------------------------------------------------------------------------------------------------------------------------
#ROTA: visualizarTipoVeiculo
#FUNÇÃO: mostrar formulário de visualização dos tipos de veiculo cadastrados
#PODE ACESSAR: usuários do tipo administrador
#--------------------------------------------------------------------------------------------------------------------------------- 
@app.route('/visualizarTipoVeiculo/<int:id>')
def visualizarTipoVeiculo(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        flash('Sessão expirou, favor logar novamente','danger')
        return redirect(url_for('login',proxima=url_for('visualizarTipoVeiculo')))  
    tipoveiculo = tb_tipoveiculo.query.filter_by(cod_tipoveiculo=id).first()
    form = frm_visualizar_tipoveiculo()
    form.descricao.data = tipoveiculo.desc_tipoveiculo
    form.status.data = tipoveiculo.status_tipoveiculo
    return render_template('visualizarTipoVeiculo.html', titulo='Visualizar Tipo Veículo', id=id, form=form)   

#---------------------------------------------------------------------------------------------------------------------------------
#ROTA: editarTipoVeiculo
##FUNÇÃO: mostrar formulário de edição dos tipos de veículo cadastrados
#PODE ACESSAR: usuários do tipo administrador
#---------------------------------------------------------------------------------------------------------------------------------
@app.route('/editarTipoVeiculo/<int:id>')
def editarTipoVeiculo(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        flash('Sessão expirou, favor logar novamente','danger')
        return redirect(url_for('login',proxima=url_for('editarTipoVeiculo')))  
    tipoveiculo = tb_tipoveiculo.query.filter_by(cod_tipoveiculo=id).first()
    form = frm_editar_tipoveiculo()
    form.descricao.data = tipoveiculo.desc_tipoveiculo
    form.status.data = tipoveiculo.status_tipoveiculo
    return render_template('editarTipoVeiculo.html', titulo='Editar Tipo Veículo', id=id, form=form)   

#---------------------------------------------------------------------------------------------------------------------------------
#ROTA: atualizarTipoVeiculo
#FUNÇÃO: alterar as informações dos tipos de veículo no banco de dados
#PODE ACESSAR: usuários do tipo administrador
#---------------------------------------------------------------------------------------------------------------------------------
@app.route('/atualizarTipoVeiculo', methods=['POST',])
def atualizarTipoVeiculo():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        flash('Sessão expirou, favor logar novamente','danger')
        return redirect(url_for('login',proxima=url_for('atualizarTipoVeiculo')))      
    form = frm_editar_tipoveiculo(request.form)
    if form.validate_on_submit():
        id = request.form['id']
        tipoveiculo = tb_tipoveiculo.query.filter_by(cod_tipoveiculo=request.form['id']).first()
        tipoveiculo.desc_tipoveiculo = form.descricao.data
        tipoveiculo.status_tipoveiculo= form.status.data
        db.session.add(tipoveiculo)
        db.session.commit()
        flash('Tipo de veículo atualizado com sucesso!','success')
    else:
        flash('Favor verificar os campos!','danger')
    return redirect(url_for('visualizarTipoVeiculo', id=request.form['id']))    

##################################################################################################################################
#MARCA DE VEÍCULOS
##################################################################################################################################

#---------------------------------------------------------------------------------------------------------------------------------
#ROTA: marcaveiculo
#FUNÇÃO: tela do sistema para mostrar as marcas de veículos cadastrados
#PODE ACESSAR: usuários do tipo administrador
#---------------------------------------------------------------------------------------------------------------------------------
@app.route('/marcaveiculo', methods=['POST','GET'])
def marcaveiculo():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        flash('Sessão expirou, favor logar novamente','danger')
        return redirect(url_for('login',proxima=url_for('marcaveiculo')))         
    page = request.args.get('page', 1, type=int)
    form = frm_pesquisa()   
    pesquisa = form.pesquisa.data
    if pesquisa == "":
        pesquisa = form.pesquisa_responsiva.data
    
    if pesquisa == "" or pesquisa == None:     
        marcasveiculo = tb_marcaveiculo.query.order_by(tb_marcaveiculo.desc_marcaveiculo)\
        .paginate(page=page, per_page=ROWS_PER_PAGE , error_out=False)
    else:
        marcasveiculo = tb_marcaveiculo.query.order_by(tb_marcaveiculo.desc_marcaveiculo)\
        .filter(tb_marcaveiculo.desc_marcaveiculos.ilike(f'%{pesquisa}%'))\
        .paginate(page=page, per_page=ROWS_PER_PAGE, error_out=False)        
    return render_template('marcaveiculo.html', titulo='Marca Veículo', marcasveiculo=marcasveiculo, form=form)

#---------------------------------------------------------------------------------------------------------------------------------
#ROTA: novoTipoVeiculo
#FUNÇÃO: mostrar o formulário de cadastro das marcas de veículo
#PODE ACESSAR: usuários do tipo administrador
#---------------------------------------------------------------------------------------------------------------------------------
@app.route('/novoMarcaVeiculo')
def novoMarcaVeiculo():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        flash('Sessão expirou, favor logar novamente','danger')
        return redirect(url_for('login',proxima=url_for('novoMarcaVeiculo'))) 
    form = frm_editar_tipoveiculo()
    return render_template('novoMarcaVeiculo.html', titulo='Novo Marca Veiculo', form=form)

#---------------------------------------------------------------------------------------------------------------------------------
#ROTA: criarMarcaVeiculo
#FUNÇÃO: inserir informações do marcas de veículos no banco de dados
#PODE ACESSAR: usuários do tipo administrador
#--------------------------------------------------------------------------------------------------------------------------------- 
@app.route('/criarMarcaVeiculo', methods=['POST',])
def criarMarcaVeiculo():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        flash('Sessão expirou, favor logar novamente','danger')
        return redirect(url_for('login',proxima=url_for('criarMarcaVeiculo')))     
    form = frm_editar_marcaveiculo(request.form)
    if not form.validate_on_submit():
        flash('Por favor, preencha todos os dados','danger')
        return redirect(url_for('criarMarcaVeiculo'))
    desc  = form.descricao.data
    status = form.status.data
    marcaveiculo = tb_marcaveiculo.query.filter_by(desc_marcaveiculo=desc).first()
    if marcaveiculo:
        flash ('Marca Veículo já existe','danger')
        return redirect(url_for('tipoveiculo')) 
    novoMarcaVeiculo = tb_marcaveiculo(desc_marcaveiculo=desc, status_marcaveiculo=status)
    flash('Marca de veículo criado com sucesso!','success')
    db.session.add(novoMarcaVeiculo)
    db.session.commit()
    return redirect(url_for('marcaveiculo'))

#---------------------------------------------------------------------------------------------------------------------------------
#ROTA: visualizarMarcaVeiculo
#FUNÇÃO: mostrar formulário de visualização das marcas de veiculo cadastrados
#PODE ACESSAR: usuários do tipo administrador
#--------------------------------------------------------------------------------------------------------------------------------- 
@app.route('/visualizarMarcaVeiculo/<int:id>')
def visualizarMarcaVeiculo(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        flash('Sessão expirou, favor logar novamente','danger')
        return redirect(url_for('login',proxima=url_for('visualizarMarcaVeiculo')))  
    marcaveiculo = tb_marcaveiculo.query.filter_by(cod_marcaveiculo=id).first()
    form = frm_visualizar_marcaveiculo()
    form.descricao.data = marcaveiculo.desc_marcaveiculo
    form.status.data = marcaveiculo.status_marcaveiculo
    return render_template('visualizarMarcaVeiculo.html', titulo='Visualizar Marca Veículo', id=id, form=form)   

#---------------------------------------------------------------------------------------------------------------------------------
#ROTA: editarMarcaVeiculo
##FUNÇÃO: mostrar formulário de edição das marcas de veículo cadastrados
#PODE ACESSAR: usuários do tipo administrador
#---------------------------------------------------------------------------------------------------------------------------------
@app.route('/editarMarcaVeiculo/<int:id>')
def editarMarcaVeiculo(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        flash('Sessão expirou, favor logar novamente','danger')
        return redirect(url_for('login',proxima=url_for('editarMarcaVeiculo')))  
    marcaveiculo = tb_marcaveiculo.query.filter_by(cod_marcaveiculo=id).first()
    form = frm_editar_marcaveiculo()
    form.descricao.data = marcaveiculo.desc_marcaveiculo
    form.status.data = marcaveiculo.status_marcaveiculo
    return render_template('editarMarcaVeiculo.html', titulo='Editar Marca Veículo', id=id, form=form)   

#---------------------------------------------------------------------------------------------------------------------------------
#ROTA: atualizarMarcaVeiculo
#FUNÇÃO: alterar as informações das marcas de veículo no banco de dados
#PODE ACESSAR: usuários do tipo administrador
#---------------------------------------------------------------------------------------------------------------------------------
@app.route('/atualizarMarcaVeiculo', methods=['POST',])
def atualizarMarcaVeiculo():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        flash('Sessão expirou, favor logar novamente','danger')
        return redirect(url_for('login',proxima=url_for('atualizarMarcaVeiculo')))      
    form = frm_editar_marcaveiculo(request.form)
    if form.validate_on_submit():
        id = request.form['id']
        marcaveiculo = tb_marcaveiculo.query.filter_by(cod_marcaveiculo=request.form['id']).first()
        marcaveiculo.desc_marcaveiculo = form.descricao.data
        marcaveiculo.status_marcaveiculo= form.status.data
        db.session.add(marcaveiculo)
        db.session.commit()
        flash('Marca de veículo atualizado com sucesso!','success')
    else:
        flash('Favor verificar os campos!','danger')
    return redirect(url_for('visualizarMarcaVeiculo', id=request.form['id']))    


##################################################################################################################################
#VEÍCULOS
##################################################################################################################################

#---------------------------------------------------------------------------------------------------------------------------------
#ROTA: veiculo
#FUNÇÃO: tela do sistema para mostrar os veículos cadastrados
#PODE ACESSAR: usuários do tipo administrador
#---------------------------------------------------------------------------------------------------------------------------------
@app.route('/veiculo', methods=['POST','GET'])
def veiculo():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        flash('Sessão expirou, favor logar novamente','danger')
        return redirect(url_for('login',proxima=url_for('veiculo')))         
    page = request.args.get('page', 1, type=int)
    form = frm_pesquisa()   
    pesquisa = form.pesquisa.data
    if pesquisa == "":
        pesquisa = form.pesquisa_responsiva.data
    
    if pesquisa == "" or pesquisa == None:     
        veiculos = tb_veiculo.query.order_by(tb_veiculo.desc_veiculo)\
        .paginate(page=page, per_page=ROWS_PER_PAGE , error_out=False)
    else:
        veiculos = tb_veiculo.query.order_by(tb_veiculo.desc_veiculo)\
        .filter(tb_veiculo.desc_veiculos.ilike(f'%{pesquisa}%'))\
        .paginate(page=page, per_page=ROWS_PER_PAGE, error_out=False)        
    return render_template('veiculo.html', titulo='Veículo', veiculos=veiculos, form=form)

#---------------------------------------------------------------------------------------------------------------------------------
#ROTA: novoVeiculo
#FUNÇÃO: mostrar o formulário de cadastro dos veículo
#PODE ACESSAR: usuários do tipo administrador
#---------------------------------------------------------------------------------------------------------------------------------
@app.route('/novoVeiculo')
def novoVeiculo():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        flash('Sessão expirou, favor logar novamente','danger')
        return redirect(url_for('login',proxima=url_for('novoVeiculo'))) 
    form = frm_editar_veiculo()
    return render_template('novoVeiculo.html', titulo='Novo Veiculo', form=form)

#---------------------------------------------------------------------------------------------------------------------------------
#ROTA: criarVeiculo
#FUNÇÃO: inserir informações do marcas de veículos no banco de dados
#PODE ACESSAR: usuários do tipo administrador
#--------------------------------------------------------------------------------------------------------------------------------- 
@app.route('/criarVeiculo', methods=['POST',])
def criarVeiculo():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        flash('Sessão expirou, favor logar novamente','danger')
        return redirect(url_for('login',proxima=url_for('criarVeiculo')))     
    form = frm_editar_veiculo(request.form)
    if not form.validate_on_submit():
        flash('Por favor, preencha todos os dados','danger')
        return redirect(url_for('criarVeiculo'))
    desc  = form.descricao.data
    status = form.status.data
    marca = form.marcaveiculo.data
    tipo = form.tipoveiculo.data
    veiculo = tb_veiculo.query.filter_by(desc_veiculo=desc).first()
    if veiculo:
        flash ('Veículo já existe','danger')
        return redirect(url_for('veiculo')) 
    novoVeiculo = tb_veiculo(desc_veiculo=desc, status_veiculo=status,cod_marcaveiculo=marca,cod_tipoveiculo=tipo)
    flash('Veículo criado com sucesso!','success')
    db.session.add(novoVeiculo)
    db.session.commit()
    return redirect(url_for('veiculo'))

#---------------------------------------------------------------------------------------------------------------------------------
#ROTA: visualizarVeiculo
#FUNÇÃO: mostrar formulário de visualização dos veiculos cadastrados
#PODE ACESSAR: usuários do tipo administrador
#--------------------------------------------------------------------------------------------------------------------------------- 
@app.route('/visualizarVeiculo/<int:id>')
def visualizarVeiculo(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        flash('Sessão expirou, favor logar novamente','danger')
        return redirect(url_for('login',proxima=url_for('visualizarVeiculo')))  
    veiculo = tb_veiculo.query.filter_by(cod_veiculo=id).first()
    form = frm_visualizar_veiculo()
    form.descricao.data = veiculo.desc_veiculo
    form.status.data = veiculo.status_veiculo
    form.marcaveiculo.data = veiculo.cod_marcaveiculo
    form.tipoveiculo.data = veiculo.cod_tipoveiculo
    return render_template('visualizarVeiculo.html', titulo='Visualizar Veículo', id=id, form=form)   

#---------------------------------------------------------------------------------------------------------------------------------
#ROTA: editarVeiculo
##FUNÇÃO: mostrar formulário de edição dos veículo cadastrados
#PODE ACESSAR: usuários do tipo administrador
#---------------------------------------------------------------------------------------------------------------------------------
@app.route('/editarVeiculo/<int:id>')
def editarVeiculo(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        flash('Sessão expirou, favor logar novamente','danger')
        return redirect(url_for('login',proxima=url_for('editarVeiculo')))  
    veiculo = tb_veiculo.query.filter_by(cod_veiculo=id).first()
    form = frm_editar_veiculo()
    form.descricao.data = veiculo.desc_veiculo
    form.status.data = veiculo.status_veiculo
    form.marcaveiculo.data = veiculo.cod_marcaveiculo
    form.tipoveiculo.data = veiculo.cod_tipoveiculo
    return render_template('editarVeiculo.html', titulo='Editar Veículo', id=id, form=form)   

#---------------------------------------------------------------------------------------------------------------------------------
#ROTA: atualizarVeiculo
#FUNÇÃO: alterar as informações dos veículo no banco de dados
#PODE ACESSAR: usuários do tipo administrador
#---------------------------------------------------------------------------------------------------------------------------------
@app.route('/atualizarVeiculo', methods=['POST',])
def atualizarVeiculo():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        flash('Sessão expirou, favor logar novamente','danger')
        return redirect(url_for('login',proxima=url_for('atualizarVeiculo')))      
    form = frm_editar_veiculo(request.form)
    if form.validate_on_submit():
        id = request.form['id']
        veiculo = tb_veiculo.query.filter_by(cod_veiculo=request.form['id']).first()
        veiculo.desc_veiculo = form.descricao.data
        veiculo.status_veiculo= form.status.data
        veiculo.cod_marca = form.marcaveiculo.data
        veiculo.cod_tipoveiculo = form.tipoveiculo.data
        db.session.add(veiculo)
        db.session.commit()
        flash('Veículo atualizado com sucesso!','success')
    else:
        flash('Favor verificar os campos!','danger')
    return redirect(url_for('visualizarVeiculo', id=request.form['id']))   

##################################################################################################################################
#PREÇOS
##################################################################################################################################

#---------------------------------------------------------------------------------------------------------------------------------
#ROTA: precos
#FUNÇÃO: tela do sistema para mostrar os preços cadastrados
#PODE ACESSAR: usuários do tipo administrador
#---------------------------------------------------------------------------------------------------------------------------------
@app.route('/preco', methods=['POST','GET'])
def preco():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        flash('Sessão expirou, favor logar novamente','danger')
        return redirect(url_for('login',proxima=url_for('preco')))         
    page = request.args.get('page', 1, type=int)
    form = frm_pesquisa()   
    pesquisa = form.pesquisa.data
    if pesquisa == "":
        pesquisa = form.pesquisa_responsiva.data
    
    if pesquisa == "" or pesquisa == None:     
        precos = tb_preco.query.order_by(tb_preco.ordem_preco)\
        .paginate(page=page, per_page=ROWS_PER_PAGE , error_out=False)
    else:
        precos = tb_preco.query.order_by(tb_preco.ordem_preco)\
        .filter(tb_preco.desc_precoilike(f'%{pesquisa}%'))\
        .paginate(page=page, per_page=ROWS_PER_PAGE, error_out=False)        
    return render_template('preco.html', titulo='Preços', precos=precos, form=form)

#---------------------------------------------------------------------------------------------------------------------------------
#ROTA: novoPreco
#FUNÇÃO: mostrar o formulário de cadastro dos preços
#PODE ACESSAR: usuários do tipo administrador
#---------------------------------------------------------------------------------------------------------------------------------
@app.route('/novoPreco')
def novoPreco():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        flash('Sessão expirou, favor logar novamente','danger')
        return redirect(url_for('login',proxima=url_for('novoPreco'))) 
    form = frm_editar_preco()
    return render_template('novoPreco.html', titulo='Novo Preço', form=form)

#---------------------------------------------------------------------------------------------------------------------------------
#ROTA: criarPreco
#FUNÇÃO: inserir informações do preços no banco de dados
#PODE ACESSAR: usuários do tipo administrador
#--------------------------------------------------------------------------------------------------------------------------------- 
@app.route('/criarPreco', methods=['POST',])
def criarPreco():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        flash('Sessão expirou, favor logar novamente','danger')
        return redirect(url_for('login',proxima=url_for('criarPreco')))     
    form = frm_editar_preco(request.form)
    if not form.validate_on_submit():
        flash('Por favor, preencha todos os dados','danger')
        return redirect(url_for('criarPreco'))
    desc  = form.descricao.data
    status = form.status.data
    minutoinicial = form.minutoinicial.data
    minutofinal = form.minutofinal.data
    valor = form.preco.data
    ordem = form.ordem.data
    preco = tb_preco.query.filter_by(desc_preco=desc).first()
    if preco:
        flash ('Preço já existe','danger')
        return redirect(url_for('preco')) 
    novoPreco = tb_preco(desc_preco=desc, status_preco=status,minutoinicial_preco=minutoinicial,minutofinal_preco=minutofinal,valor_preco=valor,ordem_preco=ordem)
    flash('Preço criado com sucesso!','success')
    db.session.add(novoPreco)
    db.session.commit()
    return redirect(url_for('preco'))

#---------------------------------------------------------------------------------------------------------------------------------
#ROTA: visualizarPreco
#FUNÇÃO: mostrar formulário de visualização dos preços cadastrados
#PODE ACESSAR: usuários do tipo administrador
#--------------------------------------------------------------------------------------------------------------------------------- 
@app.route('/visualizarPreco/<int:id>')
def visualizarPreco(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        flash('Sessão expirou, favor logar novamente','danger')
        return redirect(url_for('login',proxima=url_for('visualizarPreco')))  
    preco = tb_preco.query.filter_by(cod_preco=id).first()
    form = frm_visualizar_preco()
    form.descricao.data = preco.desc_preco
    form.status.data = preco.status_preco
    form.minutoinicial.data = preco.minutoinicio_preco
    form.minutofinal.data = preco.minutofinal_preco
    form.preco.data = preco.valor_preco
    form.ordem.data = preco.ordem_preco
    return render_template('visualizarPreco.html', titulo='Visualizar Preço', id=id, form=form)   

#---------------------------------------------------------------------------------------------------------------------------------
#ROTA: editarPreco
##FUNÇÃO: mostrar formulário de edição dos preços cadastrados
#PODE ACESSAR: usuários do tipo administrador
#---------------------------------------------------------------------------------------------------------------------------------
@app.route('/editarPreco/<int:id>')
def editarPreco(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        flash('Sessão expirou, favor logar novamente','danger')
        return redirect(url_for('login',proxima=url_for('editarPreco')))  
    preco = tb_preco.query.filter_by(cod_preco=id).first()
    form = frm_editar_preco()
    form.descricao.data = preco.desc_preco
    form.status.data = preco.status_preco
    form.minutoinicial.data = preco.minutoinicio_preco
    form.minutofinal.data = preco.minutofinal_preco
    form.preco.data = preco.valor_preco
    form.ordem.data = preco.ordem_preco
    return render_template('editarPreco.html', titulo='Editar Preço', id=id, form=form)   

#---------------------------------------------------------------------------------------------------------------------------------
#ROTA: atualizarPreco
#FUNÇÃO: alterar as informações dos preços no banco de dados
#PODE ACESSAR: usuários do tipo administrador
#---------------------------------------------------------------------------------------------------------------------------------
@app.route('/atualizarPreco', methods=['POST',])
def atualizarPreco():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        flash('Sessão expirou, favor logar novamente','danger')
        return redirect(url_for('login',proxima=url_for('atualizarPreco')))      
    form = frm_editar_preco(request.form)
    if form.validate_on_submit():
        id = request.form['id']
        preco = tb_preco.query.filter_by(cod_preco=request.form['id']).first()
        preco.desc_preco = form.descricao.data
        preco.status_preco= form.status.data
        preco.minutoinicio_preco = form.minutoinicial.data
        preco.minutofinal_preco = form.minutofinal.data
        preco.valor_preco = form.preco.data
        preco.ordem_preco = form.ordem.data
        db.session.add(preco)
        db.session.commit()
        flash('Preco atualizado com sucesso!','success')
    else:
        flash('Favor verificar os campos!','danger')
    return redirect(url_for('visualizarPreco', id=request.form['id'])) 

##################################################################################################################################
#TIPO DE PAGAMENTOS
##################################################################################################################################

#---------------------------------------------------------------------------------------------------------------------------------
#ROTA: tipopagamento
#FUNÇÃO: tela do sistema para mostrar os tipos de pagamentos cadastrados
#PODE ACESSAR: usuários do tipo administrador
#---------------------------------------------------------------------------------------------------------------------------------
@app.route('/tipopagamento', methods=['POST','GET'])
def tipopagamento():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        flash('Sessão expirou, favor logar novamente','danger')
        return redirect(url_for('login',proxima=url_for('tipopagamento')))         
    page = request.args.get('page', 1, type=int)
    form = frm_pesquisa()   
    pesquisa = form.pesquisa.data
    if pesquisa == "":
        pesquisa = form.pesquisa_responsiva.data
    
    if pesquisa == "" or pesquisa == None:     
        tipospagamento = tb_tipopagamento.query.order_by(tb_tipopagamento.desc_tipopagamento)\
        .paginate(page=page, per_page=ROWS_PER_PAGE , error_out=False)
    else:
        tipospagamento = tb_tipopagamento.query.order_by(tb_tipopagamento.desc_tipopagamento)\
        .filter(tb_tipopagamento.desc_tipopagamento.ilike(f'%{pesquisa}%'))\
        .paginate(page=page, per_page=ROWS_PER_PAGE, error_out=False)        
    return render_template('tipopagamento.html', titulo='Tipo Pagamento', tipospagamento=tipospagamento, form=form)

#---------------------------------------------------------------------------------------------------------------------------------
#ROTA: novoTipoPagamento
#FUNÇÃO: mostrar o formulário de cadastro de tipo de pagamento
#PODE ACESSAR: usuários do tipo administrador
#---------------------------------------------------------------------------------------------------------------------------------
@app.route('/novoTipoPagamento')
def novoTipoPagamento():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        flash('Sessão expirou, favor logar novamente','danger')
        return redirect(url_for('login',proxima=url_for('novoTipoPagamento'))) 
    form = frm_editar_tipopagamento()
    return render_template('novoTipoPagamento.html', titulo='Novo Tipo Pagamento', form=form)

#---------------------------------------------------------------------------------------------------------------------------------
#ROTA: criarTipoPagamento
#FUNÇÃO: inserir informações do tipo de pagamento no banco de dados
#PODE ACESSAR: usuários do tipo administrador
#--------------------------------------------------------------------------------------------------------------------------------- 
@app.route('/criarTipoPagamento', methods=['POST',])
def criarTipoPagamento():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        flash('Sessão expirou, favor logar novamente','danger')
        return redirect(url_for('login',proxima=url_for('criarTipoPaamento')))     
    form = frm_editar_tipopagamento(request.form)
    if not form.validate_on_submit():
        flash('Por favor, preencha todos os dados','danger')
        return redirect(url_for('criarTipoPagamento'))
    desc  = form.descricao.data
    status = form.status.data
    tipopagamento = tb_tipopagamento.query.filter_by(desc_tipopagamento=desc).first()
    if tipopagamento:
        flash ('Tipo Pagamento já existe','danger')
        return redirect(url_for('tipopagamento')) 
    novoTipoPagamento = tb_tipopagamento(desc_tipopagamento=desc, status_tipopagamento=status)
    flash('Tipo de pagamento criado com sucesso!','success')
    db.session.add(novoTipoPagamento)
    db.session.commit()
    return redirect(url_for('tipopagamento'))

#---------------------------------------------------------------------------------------------------------------------------------
#ROTA: visualizarTipoPagamento
#FUNÇÃO: mostrar formulário de visualização dos tipos de pagamento cadastrados
#PODE ACESSAR: usuários do tipo administrador
#--------------------------------------------------------------------------------------------------------------------------------- 
@app.route('/visualizarTipoPagamento/<int:id>')
def visualizarTipoPagamento(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        flash('Sessão expirou, favor logar novamente','danger')
        return redirect(url_for('login',proxima=url_for('visualizarTipoPagamento')))  
    tipopagamento = tb_tipopagamento.query.filter_by(cod_tipopagamento=id).first()
    form = frm_visualizar_tipopagamento()
    form.descricao.data = tipopagamento.desc_tipopagamento
    form.status.data = tipopagamento.status_tipopagamento
    return render_template('visualizarTipoPagamento.html', titulo='Visualizar Tipo Pagamento', id=id, form=form)   

#---------------------------------------------------------------------------------------------------------------------------------
#ROTA: editarTipoUsuario
##FUNÇÃO: mostrar formulário de edição dos tipos de usuários cadastrados
#PODE ACESSAR: usuários do tipo administrador
#---------------------------------------------------------------------------------------------------------------------------------
@app.route('/editarTipoPagamento/<int:id>')
def editarTipoPagamento(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        flash('Sessão expirou, favor logar novamente','danger')
        return redirect(url_for('login',proxima=url_for('editarTipoPagamento')))  
    tipopagamento = tb_tipopagamento.query.filter_by(cod_tipopagamento=id).first()
    form = frm_editar_tipopagamento()
    form.descricao.data = tipopagamento.desc_tipopagamento
    form.status.data = tipopagamento.status_tipopagamento
    return render_template('editarTipoPagamento.html', titulo='Editar Tipo Pagamento', id=id, form=form)   

#---------------------------------------------------------------------------------------------------------------------------------
#ROTA: atualizarTipoPagamento
#FUNÇÃO: alterar as informações dos tipos de usuários no banco de dados
#PODE ACESSAR: usuários do tipo administrador
#---------------------------------------------------------------------------------------------------------------------------------
@app.route('/atualizarTipoPagamento', methods=['POST',])
def atualizarTipoPagamento():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        flash('Sessão expirou, favor logar novamente','danger')
        return redirect(url_for('login',proxima=url_for('atualizarTipoPagamento')))      
    form = frm_editar_tipopagamento(request.form)
    if form.validate_on_submit():
        id = request.form['id']
        tipopagamento = tb_tipopagamento.query.filter_by(cod_tipopagamento=request.form['id']).first()
        tipopagamento.desc_tipopagamento = form.descricao.data
        tipopagamento.status_tipopagamento = form.status.data
        db.session.add(tipopagamento)
        db.session.commit()
        flash('Tipo de pagamento atualizado com sucesso!','success')
    else:
        flash('Favor verificar os campos!','danger')
    return redirect(url_for('visualizarTipoPagamento', id=request.form['id']))  

##################################################################################################################################
#ESTACIONAMENTO
##################################################################################################################################

#---------------------------------------------------------------------------------------------------------------------------------
#ROTA: estacionamento
#FUNÇÃO: tela do sistema para mostrar os estacionamento cadastrados
#PODE ACESSAR: usuários do tipo administrador
#---------------------------------------------------------------------------------------------------------------------------------
@app.route('/estacionamento', methods=['POST','GET'])
def estacionamento():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        flash('Sessão expirou, favor logar novamente','danger')
        return redirect(url_for('login',proxima=url_for('estacionamento')))         
    page = request.args.get('page', 1, type=int)
    form = frm_pesquisa()   
    pesquisa = form.pesquisa.data
    if pesquisa == "":
        pesquisa = form.pesquisa_responsiva.data
    
    if pesquisa == "" or pesquisa == None:     
        estacionamentos = tb_estacionamento.query\
        .join(tb_veiculo, tb_estacionamento.cod_veiculo==tb_veiculo.cod_veiculo)\
        .join(tb_marcaveiculo, tb_marcaveiculo.cod_marcaveiculo==tb_veiculo.cod_marcaveiculo)\
        .add_columns(tb_estacionamento.cod_estacionamento, tb_estacionamento.placa_estacionamento, tb_veiculo.desc_veiculo, tb_marcaveiculo.desc_marcaveiculo, tb_estacionamento.entrada_estacionamento)\
        .order_by(tb_estacionamento.entrada_estacionamento.desc())\
        .filter(tb_estacionamento.valor_estacionamento == None)\
        .paginate(page=page, per_page=ROWS_PER_PAGE , error_out=False)
    else:
        estacionamentos = tb_estacionamento.query\
        .join(tb_veiculo, tb_estacionamento.cod_veiculo==tb_veiculo.cod_veiculo)\
        .join(tb_marcaveiculo, tb_marcaveiculo.cod_marcaveiculo==tb_veiculo.cod_marcaveiculo)\
        .add_columns(tb_estacionamento.cod_estacionamento, tb_estacionamento.placa_estacionamento, tb_veiculo.desc_veiculo, tb_marcaveiculo.desc_marcaveiculo, tb_estacionamento.entrada_estacionamento)\
        .order_by(tb_estacionamento.entrada_estacionamento.desc())\
        .filter(tb_estacionamento.placa_estacionamento.ilike(f'%{pesquisa}%'))\
        .filter(tb_estacionamento.valor_estacionamento == None)\
        .paginate(page=page, per_page=ROWS_PER_PAGE, error_out=False)        
    return render_template('estacionamento.html', titulo='Estacionamento', estacionamentos=estacionamentos, form=form)

#---------------------------------------------------------------------------------------------------------------------------------
#ROTA: novoEstacionamento
#FUNÇÃO: mostrar o formulário de cadastro de estacionamento
#PODE ACESSAR: usuários do tipo administrador
#---------------------------------------------------------------------------------------------------------------------------------
@app.route('/novoEstacionamento')
def novoEstacionamento():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        flash('Sessão expirou, favor logar novamente','danger')
        return redirect(url_for('login',proxima=url_for('novoEstacionamento'))) 
    form = frm_editar_estacionamento_entrada()
    form.entrada.data = datetime.now()
    return render_template('novoEstacionamento.html', titulo='Novo Estacionamento', form=form)

#---------------------------------------------------------------------------------------------------------------------------------
#ROTA: criarEstacionamento
#FUNÇÃO: inserir informações do estacionamento no banco de dados
#PODE ACESSAR: usuários do tipo administrador
#--------------------------------------------------------------------------------------------------------------------------------- 
@app.route('/criarEstacionamento', methods=['POST',])
def criarEstacionamento():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        flash('Sessão expirou, favor logar novamente','danger')
        return redirect(url_for('login',proxima=url_for('criarEstacionamento')))     
    form = frm_editar_estacionamento_entrada(request.form)
    #return str(form.entrada.data)
    if not form.validate_on_submit():
        flash('Por favor, preencha todos os dados','danger')
        return redirect(url_for('criarEstacionamento'))
    placa  = form.placa.data
    entrada = form.entrada.data
    veiculo = form.veiculo.data

    estacionamento = tb_estacionamento.query.filter_by(entrada_estacionamento=entrada).first()
    if estacionamento:
        flash ('Estacionamento já existe','danger')
        return redirect(url_for('estacionamento')) 
    novoEstacionamento = tb_estacionamento(placa_estacionamento=placa,entrada_estacionamento=entrada,cod_veiculo=veiculo)
    flash('Tipo de pagamento criado com sucesso!','success')
    db.session.add(novoEstacionamento)
    db.session.commit()
    return redirect(url_for('estacionamento'))

#---------------------------------------------------------------------------------------------------------------------------------
#ROTA: visualizarEstacionamento
#FUNÇÃO: mostrar formulário de visualização dos estacionamento cadastrados
#PODE ACESSAR: usuários do tipo administrador
#--------------------------------------------------------------------------------------------------------------------------------- 
@app.route('/visualizarEstacionamento/<int:id>')
def visualizarEstacionamento(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        flash('Sessão expirou, favor logar novamente','danger')
        return redirect(url_for('login',proxima=url_for('visualizarEstacionamento')))  
    estacionamento = tb_estacionamento.query.filter_by(cod_estacionamento=id).first()
    form = frm_visualizar_estacionamento()
    form.placa.data = estacionamento.placa_estacionamento
    form.entrada.data = estacionamento.entrada_estacionamento
    form.veiculo.data = estacionamento.cod_veiculo
    return render_template('visualizarEstacionamento.html', titulo='Visualizar Estacionamento', id=id, form=form)   

#---------------------------------------------------------------------------------------------------------------------------------
#ROTA: editarEstacionamento
##FUNÇÃO: mostrar formulário de edição dos estacionamento cadastrados
#PODE ACESSAR: usuários do tipo administrador
#---------------------------------------------------------------------------------------------------------------------------------
@app.route('/editarEstacionamento/<int:id>')
def editarEstacionamento(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        flash('Sessão expirou, favor logar novamente','danger')
        return redirect(url_for('login',proxima=url_for('editarEstacionamento')))  
    estacionamento = tb_estacionamento.query.filter_by(cod_estacionamento=id).first()
    form = frm_editar_estacionamento_entrada()
    form.placa.data = estacionamento.placa_estacionamento
    form.entrada.data = estacionamento.entrada_estacionamento
    form.veiculo.data = estacionamento.cod_veiculo
    return render_template('editarEstacionamento.html', titulo='Editar Estacionamento', id=id, form=form)   

#---------------------------------------------------------------------------------------------------------------------------------
#ROTA: atualizarEstacionamento
#FUNÇÃO: alterar as informações dos estacionamento no banco de dados
#PODE ACESSAR: usuários do tipo administrador
#---------------------------------------------------------------------------------------------------------------------------------
@app.route('/atualizarEstacionamento', methods=['POST',])
def atualizarEstacionamento():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        flash('Sessão expirou, favor logar novamente','danger')
        return redirect(url_for('login',proxima=url_for('atualizarEstacionamento')))      
    form = frm_editar_estacionamento_entrada(request.form)
    if form.validate_on_submit():
        id = request.form['id']
        estacionamento = tb_estacionamento.query.filter_by(cod_estacionamento=request.form['id']).first()
        estacionamento.placa_estacionamento = form.placa.data
        estacionamento.entrada_estacionamento = form.entrada.data
        estacionamento.cod_veiculo = form.veiculo.data

        db.session.add(estacionamento)
        db.session.commit()
        flash('Estacionamento atualizado com sucesso!','success')
    else:
        flash('Favor verificar os campos!','danger')
    return redirect(url_for('visualizarEstacionamento', id=request.form['id']))  

#---------------------------------------------------------------------------------------------------------------------------------
#ROTA: editarEstacionamento
##FUNÇÃO: mostrar formulário de edição dos estacionamento cadastrados
#PODE ACESSAR: usuários do tipo administrador
#---------------------------------------------------------------------------------------------------------------------------------
@app.route('/finalizarEstacionamento/<int:id>')
def finalizarEstacionamento(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        flash('Sessão expirou, favor logar novamente','danger')
        return redirect(url_for('login',proxima=url_for('finalizarEstacionamento')))  
    estacionamento = tb_estacionamento.query.filter_by(cod_estacionamento=id).first()
    form = frm_editar_estacionamento()
    form.placa.data = estacionamento.placa_estacionamento
    form.entrada.data = estacionamento.entrada_estacionamento
    form.saida.data = datetime.now()
    form.veiculo.data = estacionamento.cod_veiculo
    tempo = datetime.now() - estacionamento.entrada_estacionamento
    minutos = int(tempo.total_seconds()/60)
    precos = tb_preco.query.order_by(tb_preco.desc_preco)
    for preco in precos:
        if minutos >= (preco.minutoinicio_preco) and minutos <= (preco.minutofinal_preco):
            valorfinal = preco.valor_preco
    qrcodeimagem = str(estacionamento.placa_estacionamento) +"-"+ str(valorfinal)
    form.valor.data = valorfinal
    return render_template('finalizarEstacionamento.html', titulo='Finalizar Estacionamento', id=id, form=form,qrcodeimagem=qrcodeimagem)  

#---------------------------------------------------------------------------------------------------------------------------------
#ROTA: concluirEstacionamento
#FUNÇÃO: alterar as informações dos estacionamento no banco de dados
#PODE ACESSAR: usuários do tipo administrador
#---------------------------------------------------------------------------------------------------------------------------------
@app.route('/concluirEstacionamento', methods=['POST',])
def concluirEstacionamento():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        flash('Sessão expirou, favor logar novamente','danger')
        return redirect(url_for('login',proxima=url_for('concluirEstacionamento')))      
    form = frm_editar_estacionamento_finalizar(request.form)
    if form.validate_on_submit():
        id = request.form['id']
        estacionamento = tb_estacionamento.query.filter_by(cod_estacionamento=request.form['id']).first()
        estacionamento.cod_tipopagamento = form.pagamento.data
        estacionamento.saida_estacionamento = form.saida.data
        estacionamento.valor_estacionamento = form.valor.data
        
        db.session.add(estacionamento)
        db.session.commit()
        flash('Estacionamento finalizado com sucesso!','success')
    else:
        flash('Favor verificar os campos!','danger')
    return redirect(url_for('estacionamento'))  

#---------------------------------------------------------------------------------------------------------------------------------
#ROTA: estacionamentoHistorico
#FUNÇÃO: tela do sistema para mostrar os estacionamento cadastrados
#PODE ACESSAR: usuários do tipo administrador
#---------------------------------------------------------------------------------------------------------------------------------
@app.route('/estacionamentoHistorico', methods=['POST','GET'])
def estacionamentoHistorico():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        flash('Sessão expirou, favor logar novamente','danger')
        return redirect(url_for('login',proxima=url_for('estacionamentoHistorico')))         
    page = request.args.get('page', 1, type=int)
    form = frm_pesquisa()   
    pesquisa = form.pesquisa.data
    if pesquisa == "":
        pesquisa = form.pesquisa_responsiva.data
    
    if pesquisa == "" or pesquisa == None:     
        estacionamentos = tb_estacionamento.query\
        .join(tb_veiculo, tb_estacionamento.cod_veiculo==tb_veiculo.cod_veiculo)\
        .join(tb_marcaveiculo, tb_marcaveiculo.cod_marcaveiculo==tb_veiculo.cod_marcaveiculo)\
        .add_columns(tb_estacionamento.cod_estacionamento, tb_estacionamento.placa_estacionamento, tb_veiculo.desc_veiculo, tb_marcaveiculo.desc_marcaveiculo, tb_estacionamento.entrada_estacionamento)\
        .order_by(tb_estacionamento.entrada_estacionamento.desc())\
        .filter(tb_estacionamento.valor_estacionamento != None)\
        .paginate(page=page, per_page=ROWS_PER_PAGE , error_out=False)
    else:
        estacionamentos = tb_estacionamento.query\
        .join(tb_veiculo, tb_estacionamento.cod_veiculo==tb_veiculo.cod_veiculo)\
        .join(tb_marcaveiculo, tb_marcaveiculo.cod_marcaveiculo==tb_veiculo.cod_marcaveiculo)\
        .add_columns(tb_estacionamento.cod_estacionamento, tb_estacionamento.placa_estacionamento, tb_veiculo.desc_veiculo, tb_marcaveiculo.desc_marcaveiculo, tb_estacionamento.entrada_estacionamento)\
        .order_by(tb_estacionamento.entrada_estacionamento.desc())\
        .filter(tb_estacionamento.placa_estacionamento.ilike(f'%{pesquisa}%'))\
        .filter(tb_estacionamento.valor_estacionamento != None)\
        .paginate(page=page, per_page=ROWS_PER_PAGE, error_out=False)        
    return render_template('estacionamentoHistorico.html', titulo='Estacionamento Historico', estacionamentos=estacionamentos, form=form)

#---------------------------------------------------------------------------------------------------------------------------------
#ROTA: emitirTicket
#FUNÇÃO: tela do sistema para mostrar os estacionamento cadastrados
#PODE ACESSAR: usuários do tipo administrador
#---------------------------------------------------------------------------------------------------------------------------------
@app.route('/emitirTicket/<int:id>')
def emitirTicket(id):
    estacionamento = tb_estacionamento.query.filter_by(cod_estacionamento=id).first()
    placa = estacionamento.placa_estacionamento
    entrada = estacionamento.entrada_estacionamento.strftime("%d/%m/%Y %H:%M")
    veiculo = tb_veiculo.query.filter_by(cod_veiculo=estacionamento.cod_veiculo).first()
    modelo = veiculo.desc_veiculo
    marcas = tb_marcaveiculo.query.filter_by(cod_marcaveiculo=veiculo.cod_marcaveiculo).first()
    marca = marcas.desc_marcaveiculo
    qrcodeimagem = str(placa) +"|"+ str(marca) +"|"+ str(modelo) + "|"+ str(entrada)
    return render_template('ticket.html', titulo='Ticket Estacionamento', id=id, placa=placa, entrada=entrada, modelo=modelo,marca=marca,qrcodeimagem=qrcodeimagem)  
