#importações
import os
from estacionamento import app, db
from models import tb_user, tb_usertype, tb_tipoveiculo, tb_marcaveiculo,tb_preco, tb_veiculo, tb_tipopagamento
from flask_wtf import FlaskForm
from wtforms import Form, StringField, validators, SubmitField,IntegerField, SelectField,PasswordField,DateField,EmailField,BooleanField,RadioField, TextAreaField, TimeField, TelField, DateTimeLocalField,FloatField, DecimalField 

##################################################################################################################################
#PESQUISA
##################################################################################################################################

#---------------------------------------------------------------------------------------------------------------------------------
#FORMUÁRIO: pesquisa (geral)
#TIPO: edição
#TABELA: nenhuma
#---------------------------------------------------------------------------------------------------------------------------------
class frm_pesquisa(FlaskForm):
    pesquisa = StringField('Pesquisa:', [validators.Length(min=1, max=50)],render_kw={"placeholder": "digite sua pesquisa"} )
    pesquisa_responsiva = StringField('Pesquisa:', [validators.Length(min=1, max=50)],render_kw={"placeholder": "digite sua pesquisa"} )
    salvar = SubmitField('Pesquisar')

##################################################################################################################################
#USUÁRIO
##################################################################################################################################

#---------------------------------------------------------------------------------------------------------------------------------
#FORMUÁRIO: usuários
#TIPO: edição
#TABELA: tb_user
#---------------------------------------------------------------------------------------------------------------------------------
class frm_editar_usuario(FlaskForm):
    nome = StringField('Nome:', [validators.DataRequired(), validators.Length(min=1, max=50)],render_kw={"placeholder": "digite o nome do usuário"})
    status = SelectField('Situação:', coerce=int, choices=[(0,"Ativo"),(1,"Inativo")])
    login = StringField('Login:', [validators.DataRequired(), validators.Length(min=1, max=50)],render_kw={"placeholder": "digite o login do usuário"})    
    tipousuario = SelectField('Situação:', coerce=int,  choices=[(g.cod_usertype, g.desc_usertype) for g in tb_usertype.query.order_by('desc_usertype')])
    email = EmailField('Email:', [validators.DataRequired(), validators.Length(min=1, max=50)],render_kw={"placeholder": "digite o email do usuário"})
    salvar = SubmitField('Salvar')


#---------------------------------------------------------------------------------------------------------------------------------
#FORMUÁRIO: usuários
#TIPO: visualização
#TABELA: tb_user
#---------------------------------------------------------------------------------------------------------------------------------
class frm_visualizar_usuario(FlaskForm):
    nome = StringField('Nome:', [validators.DataRequired(), validators.Length(min=1, max=50)],render_kw={'readonly': True})
    status = SelectField('Situação:', coerce=int, choices=[(0,"Ativo"),(1,"Inativo")], render_kw={'readonly': True})
    login = StringField('Login:', [validators.DataRequired(), validators.Length(min=1, max=50)], render_kw={'readonly': True})
    tipousuario = SelectField('Tipo:', coerce=int, choices=[(g.cod_usertype, g.desc_usertype) for g in tb_usertype.query.order_by('desc_usertype')], render_kw={'readonly': True})
    email = EmailField('Email:', [validators.DataRequired(), validators.Length(min=1, max=50)], render_kw={'readonly': True})
    salvar = SubmitField('Editar')    

#---------------------------------------------------------------------------------------------------------------------------------
#FORMUÁRIO: trocar senha do usuário
#TIPO: edição
#TABELA: tb_user
#---------------------------------------------------------------------------------------------------------------------------------
class frm_editar_senha(FlaskForm):
    senhaatual = PasswordField('Senha Atual:', [validators.DataRequired(), validators.Length(min=1, max=50)], render_kw={"placeholder": "digite a senha atual"})
    novasenha1 = PasswordField('Nova Senha:', [validators.DataRequired(), validators.Length(min=1, max=50)], render_kw={"placeholder": "digite a nova senha"})
    novasenha2 = PasswordField('Confirme Nova Senha:', [validators.DataRequired(), validators.Length(min=1, max=50)], render_kw={"placeholder": "digite novamente a senha"})
    salvar = SubmitField('Editar')  

##################################################################################################################################
#TIPO DE USUÁRIO
##################################################################################################################################

#---------------------------------------------------------------------------------------------------------------------------------
#FORMUÁRIO: tipo de usuário
#TIPO: edição
#TABELA: tb_usertype
#---------------------------------------------------------------------------------------------------------------------------------
class frm_editar_tipousuario(FlaskForm):
    descricao = StringField('Descrição:', [validators.DataRequired(), validators.Length(min=1, max=50)], render_kw={"placeholder": "digite a descrição do tipo de usuário"})
    status = SelectField('Situação:', coerce=int, choices=[(0, 'Ativo'),(1, 'Inativo')])
    salvar = SubmitField('Salvar')    

#---------------------------------------------------------------------------------------------------------------------------------
#FORMUÁRIO: tipo de usuário
#TIPO: visualização
#TABELA: tb_usertype
#---------------------------------------------------------------------------------------------------------------------------------
class frm_visualizar_tipousuario(FlaskForm):
    descricao = StringField('Descrição:', [validators.DataRequired(), validators.Length(min=1, max=50)], render_kw={'readonly': True})
    status = SelectField('Situação:', coerce=int, choices=[(0, 'Ativo'),(1, 'Inativo')], render_kw={'readonly': True})
    salvar = SubmitField('Salvar')    

##################################################################################################################################
#TIPO DE VEÍCULO
##################################################################################################################################

#---------------------------------------------------------------------------------------------------------------------------------
#FORMUÁRIO: tipo de veículo
#TIPO: edição
#TABELA: tb_tipoveiculo
#---------------------------------------------------------------------------------------------------------------------------------
class frm_editar_tipoveiculo(FlaskForm):
    descricao = StringField('Descrição:', [validators.DataRequired(), validators.Length(min=1, max=50)], render_kw={"placeholder": "digite a descrição do tipo de veículo"})
    status = SelectField('Situação:', coerce=int, choices=[(0, 'Ativo'),(1, 'Inativo')])
    salvar = SubmitField('Salvar')    

#---------------------------------------------------------------------------------------------------------------------------------
#FORMUÁRIO: tipo de usuário
#TIPO: visualização
#TABELA: tb_tipoveiculo
#---------------------------------------------------------------------------------------------------------------------------------
class frm_visualizar_tipoveiculo(FlaskForm):
    descricao = StringField('Descrição:', [validators.DataRequired(), validators.Length(min=1, max=50)], render_kw={'readonly': True})
    status = SelectField('Situação:', coerce=int, choices=[(0, 'Ativo'),(1, 'Inativo')], render_kw={'readonly': True})
    salvar = SubmitField('Salvar')   
    
##################################################################################################################################
#MARCA DE VEÍCULO
##################################################################################################################################

#---------------------------------------------------------------------------------------------------------------------------------
#FORMUÁRIO: marca de veículo
#TIPO: edição
#TABELA: tb_marcaveiculo
#---------------------------------------------------------------------------------------------------------------------------------
class frm_editar_marcaveiculo(FlaskForm):
    descricao = StringField('Descrição:', [validators.DataRequired(), validators.Length(min=1, max=50)], render_kw={"placeholder": "digite a descrição do tipo de veículo"})
    status = SelectField('Situação:', coerce=int, choices=[(0, 'Ativo'),(1, 'Inativo')])
    salvar = SubmitField('Salvar')    

#---------------------------------------------------------------------------------------------------------------------------------
#FORMUÁRIO: marca de usuário
#TIPO: visualização
#TABELA: tb_marcaveiculo
#---------------------------------------------------------------------------------------------------------------------------------
class frm_visualizar_marcaveiculo(FlaskForm):
    descricao = StringField('Descrição:', [validators.DataRequired(), validators.Length(min=1, max=50)], render_kw={'readonly': True})
    status = SelectField('Situação:', coerce=int, choices=[(0, 'Ativo'),(1, 'Inativo')], render_kw={'readonly': True})
    salvar = SubmitField('Salvar')   
    
##################################################################################################################################
#VEÍCULO
##################################################################################################################################

#---------------------------------------------------------------------------------------------------------------------------------
#FORMUÁRIO: veículo
#TIPO: edição
#TABELA: tb_veiculo
#---------------------------------------------------------------------------------------------------------------------------------
class frm_editar_veiculo(FlaskForm):
    descricao = StringField('Descrição:', [validators.DataRequired(), validators.Length(min=1, max=50)], render_kw={"placeholder": "digite a descrição do tipo de veículo"})
    status = SelectField('Situação:', coerce=int, choices=[(0, 'Ativo'),(1, 'Inativo')])
    marcaveiculo = SelectField('Marca:', coerce=int, choices=[(g.cod_marcaveiculo, g.desc_marcaveiculo) for g in tb_marcaveiculo.query.order_by('desc_marcaveiculo')])
    tipoveiculo = SelectField('Tipo:', coerce=int, choices=[(g.cod_tipoveiculo, g.desc_tipoveiculo) for g in tb_tipoveiculo.query.order_by('desc_tipoveiculo')])
    salvar = SubmitField('Salvar')    

#---------------------------------------------------------------------------------------------------------------------------------
#FORMUÁRIO: veículo
#TIPO: visualização
#TABELA: tb_veiculo
#---------------------------------------------------------------------------------------------------------------------------------
class frm_visualizar_veiculo(FlaskForm):
    descricao = StringField('Descrição:', [validators.DataRequired(), validators.Length(min=1, max=50)], render_kw={'readonly': True})
    status = SelectField('Situação:', coerce=int, choices=[(0, 'Ativo'),(1, 'Inativo')], render_kw={'readonly': True})
    marcaveiculo = SelectField('Marca:', coerce=int, choices=[(g.cod_marcaveiculo, g.desc_marcaveiculo) for g in tb_marcaveiculo.query.order_by('desc_marcaveiculo')], render_kw={'readonly': True})
    tipoveiculo = SelectField('Tipo:', coerce=int, choices=[(g.cod_tipoveiculo, g.desc_tipoveiculo) for g in tb_tipoveiculo.query.order_by('desc_tipoveiculo')], render_kw={'readonly': True})
    salvar = SubmitField('Salvar')   

##################################################################################################################################
#PREÇOS
##################################################################################################################################

#---------------------------------------------------------------------------------------------------------------------------------
#FORMUÁRIO: preço
#TIPO: edição
#TABELA: tb_preco
#---------------------------------------------------------------------------------------------------------------------------------
class frm_editar_preco(FlaskForm):
    descricao = StringField('Descrição:', [validators.DataRequired(), validators.Length(min=1, max=50)], render_kw={"placeholder": "digite a descrição do preço"})
    status = SelectField('Situação:', coerce=int, choices=[(0, 'Ativo'),(1, 'Inativo')])
    minutoinicial = DecimalField ('Minuto Inicial:', [validators.DataRequired()], render_kw={"placeholder": "digite o minuto inicial"})
    minutofinal = DecimalField ('Minuto Final:', [validators.DataRequired()], render_kw={"placeholder": "digite o minuto final"})
    preco = DecimalField ('Valor R$:', [validators.DataRequired()], render_kw={"placeholder": "digite o valor"})
    ordem = DecimalField ('Ordem:', [validators.DataRequired()], render_kw={"placeholder": "digite a ordem de exibição"})
    salvar = SubmitField('Salvar')    

#---------------------------------------------------------------------------------------------------------------------------------
#FORMUÁRIO: preço
#TIPO: visualização
#TABELA: tb_preco
#---------------------------------------------------------------------------------------------------------------------------------
class frm_visualizar_preco(FlaskForm):
    descricao = StringField('Descrição:', [validators.DataRequired(), validators.Length(min=1, max=50)], render_kw={'readonly': True})
    status = SelectField('Situação:', coerce=int, choices=[(0, 'Ativo'),(1, 'Inativo')], render_kw={'readonly': True})
    minutoinicial = DecimalField ('Minuto Inicial:', [validators.DataRequired()],render_kw={'readonly': True})
    minutofinal = DecimalField ('Minuto Final:', [validators.DataRequired()],render_kw={'readonly': True})
    preco = DecimalField ('Valor R$:', [validators.DataRequired()],render_kw={'readonly': True})
    ordem = DecimalField ('Ordem:', [validators.DataRequired()],render_kw={'readonly': True})
    salvar = SubmitField('Salvar')  

##################################################################################################################################
#TIPO DE PAGAMENTO
##################################################################################################################################

#---------------------------------------------------------------------------------------------------------------------------------
#FORMUÁRIO: tipo de pagamento
#TIPO: edição
#TABELA: tb_pagamento
#---------------------------------------------------------------------------------------------------------------------------------
class frm_editar_tipopagamento(FlaskForm):
    descricao = StringField('Descrição:', [validators.DataRequired(), validators.Length(min=1, max=50)], render_kw={"placeholder": "digite a descrição do tipo de usuário"})
    status = SelectField('Situação:', coerce=int, choices=[(0, 'Ativo'),(1, 'Inativo')])
    salvar = SubmitField('Salvar')    

#---------------------------------------------------------------------------------------------------------------------------------
#FORMUÁRIO: tipo de pagamento
#TIPO: visualização
#TABELA: tb_pagamento
#---------------------------------------------------------------------------------------------------------------------------------
class frm_visualizar_tipopagamento(FlaskForm):
    descricao = StringField('Descrição:', [validators.DataRequired(), validators.Length(min=1, max=50)], render_kw={'readonly': True})
    status = SelectField('Situação:', coerce=int, choices=[(0, 'Ativo'),(1, 'Inativo')], render_kw={'readonly': True})
    salvar = SubmitField('Salvar')    

##################################################################################################################################
#ESTACIONAMENTO
##################################################################################################################################


#---------------------------------------------------------------------------------------------------------------------------------
#FORMUÁRIO: estacionamento
#TIPO: edição
#TABELA: tb_estacionamento
#---------------------------------------------------------------------------------------------------------------------------------
class frm_editar_estacionamento_entrada(FlaskForm):
    placa = StringField('Placa:', [validators.DataRequired(), validators.Length(min=1, max=50)], render_kw={"placeholder": "digite a placa"})
    entrada = DateTimeLocalField('Entrada:', [validators.DataRequired()], format='%Y-%m-%dT%H:%M')
    veiculo = SelectField('Veiculo:', coerce=int, choices=[(g.cod_veiculo, g.desc_veiculo) for g in tb_veiculo.query.order_by('desc_veiculo')])
    salvar = SubmitField('Salvar')  


#---------------------------------------------------------------------------------------------------------------------------------
#FORMUÁRIO: estacionamento
#TIPO: edição
#TABELA: tb_estacionamento
#---------------------------------------------------------------------------------------------------------------------------------
class frm_editar_estacionamento(FlaskForm):
    placa = StringField('Placa:', [validators.DataRequired(), validators.Length(min=1, max=50)], render_kw={'readonly': True})
    entrada = DateTimeLocalField('Entrada:', [validators.DataRequired()], render_kw={'readonly': True})
    saida = DateTimeLocalField('Saída:', format='%Y-%m-%dT%H:%M', render_kw={'readonly': True})
    valor = DecimalField ('Valor R$:',render_kw={'readonly': True})
    veiculo = SelectField('Veiculo:', coerce=int, choices=[(g.cod_veiculo, g.desc_veiculo) for g in tb_veiculo.query.order_by('desc_veiculo')], render_kw={'readonly': True})
    pagamento = SelectField('Pagamento:', coerce=int, choices=[(g.cod_tipopagamento, g.desc_tipopagamento) for g in tb_tipopagamento.query.order_by('desc_tipopagamento')])
    salvar = SubmitField('Salvar')    

#---------------------------------------------------------------------------------------------------------------------------------
#FORMUÁRIO: estacionamento
#TIPO: visualização
#TABELA: tb_estacionamento
#---------------------------------------------------------------------------------------------------------------------------------
class frm_visualizar_estacionamento(FlaskForm):
    placa = StringField('Descrição:', [validators.DataRequired(), validators.Length(min=1, max=7)], render_kw={'readonly': True})
    status = SelectField('Situação:', coerce=int, choices=[(0, 'Ativo'),(1, 'Inativo')], render_kw={'readonly': True})
    entrada = DateTimeLocalField('Entrada:', [validators.DataRequired()], format='%Y-%m-%dT%H:%M', render_kw={'readonly': True})
    saida = DateTimeLocalField('Saída:', format='%Y-%m-%dT%H:%M', render_kw={'readonly': True})
    valor = DecimalField ('Valor R$:', [validators.DataRequired()],render_kw={'readonly': True})
    veiculo = SelectField('Veiculo:', coerce=int, choices=[(g.cod_veiculo, g.desc_veiculo) for g in tb_veiculo.query.order_by('desc_veiculo')], render_kw={'readonly': True})
    pagamento = SelectField('Pagamento:', coerce=int, choices=[(g.cod_tipopagamento, g.desc_tipopagamento) for g in tb_tipopagamento.query.order_by('desc_tipopagamento')], render_kw={'readonly': True})
    salvar = SubmitField('Salvar')  

#---------------------------------------------------------------------------------------------------------------------------------
#FORMUÁRIO: estacionamento
#TIPO: edição
#TABELA: tb_estacionamento
#---------------------------------------------------------------------------------------------------------------------------------
class frm_editar_estacionamento_finalizar(FlaskForm):
    pagamento = SelectField('Pagamento:', coerce=int, choices=[(g.cod_tipopagamento, g.desc_tipopagamento) for g in tb_tipopagamento.query.order_by('desc_tipopagamento')])
    saida = DateTimeLocalField('Saída:', format='%Y-%m-%dT%H:%M', render_kw={'readonly': True})
    valor = DecimalField ('Valor R$:', [validators.DataRequired()],render_kw={'readonly': True})
