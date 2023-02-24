from estacionamento import db

#---------------------------------------------------------------------------------------------------------------------------------
#TABELA: USUÁRIOS
#ORIGEM: BANCO DE DADOS
#---------------------------------------------------------------------------------------------------------------------------------
class tb_user(db.Model):
    cod_user = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name_user = db.Column(db.String(50), nullable=False)
    password_user = db.Column(db.String(50), nullable=False)
    status_user = db.Column(db.Integer, nullable=False)
    login_user = db.Column(db.String(50), nullable=False)
    cod_usertype = db.Column(db.Integer, nullable=False)
    email_user = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return '<Name %r>' % self.name

#---------------------------------------------------------------------------------------------------------------------------------
#TABELA: TIPO USUÁRIOS
#ORIGEM: BANCO DE DADOS
#---------------------------------------------------------------------------------------------------------------------------------
class tb_usertype(db.Model):
    cod_usertype = db.Column(db.Integer, primary_key=True, autoincrement=True)
    desc_usertype = db.Column(db.String(50), nullable=False)
    status_usertype = db.Column(db.Integer, nullable=False)
    def __repr__(self):
        return '<Name %r>' % self.name    
 
#---------------------------------------------------------------------------------------------------------------------------------
#TABELA: TIPO VEÍCULO
#ORIGEM: BANCO DE DADOS
#---------------------------------------------------------------------------------------------------------------------------------
class tb_tipoveiculo(db.Model):
    cod_tipoveiculo = db.Column(db.Integer, primary_key=True, autoincrement=True)
    desc_tipoveiculo = db.Column(db.String(50), nullable=False)
    status_tipoveiculo = db.Column(db.Integer, nullable=False)
    def __repr__(self):
        return '<Name %r>' % self.name  


#---------------------------------------------------------------------------------------------------------------------------------
#TABELA: MARCA VEÍCULO
#ORIGEM: BANCO DE DADOS
#---------------------------------------------------------------------------------------------------------------------------------
class tb_marcaveiculo(db.Model):
    cod_marcaveiculo = db.Column(db.Integer, primary_key=True, autoincrement=True)
    desc_marcaveiculo = db.Column(db.String(50), nullable=False)
    status_marcaveiculo = db.Column(db.Integer, nullable=False)
    def __repr__(self):
        return '<Name %r>' % self.name  

#---------------------------------------------------------------------------------------------------------------------------------
#TABELA: VEÍCULO
#ORIGEM: BANCO DE DADOS
#---------------------------------------------------------------------------------------------------------------------------------
class tb_veiculo(db.Model):
    cod_veiculo = db.Column(db.Integer, primary_key=True, autoincrement=True)
    desc_veiculo = db.Column(db.String(50), nullable=False)
    status_veiculo = db.Column(db.Integer, nullable=False)
    cod_tipoveiculo = db.Column(db.Integer, nullable=False)
    cod_marcaveiculo = db.Column(db.Integer, nullable=False)
    def __repr__(self):
        return '<Name %r>' % self.name          

#---------------------------------------------------------------------------------------------------------------------------------
#TABELA: PREÇOS
#ORIGEM: BANCO DE DADOS
#---------------------------------------------------------------------------------------------------------------------------------
class tb_preco(db.Model):
    cod_preco = db.Column(db.Integer, primary_key=True, autoincrement=True)
    desc_preco = db.Column(db.String(50), nullable=False)
    status_preco = db.Column(db.Integer, nullable=False)
    horas_preco = db.Column(db.Float, nullable=False)
    valor_preco = db.Column(db.Float, nullable=False)
    def __repr__(self):
        return '<Name %r>' % self.name     


#---------------------------------------------------------------------------------------------------------------------------------
#TABELA: TIPO PAGAMENTO
#ORIGEM: BANCO DE DADOS
#---------------------------------------------------------------------------------------------------------------------------------
class tb_tipopagamento(db.Model):
    cod_tipopagamento = db.Column(db.Integer, primary_key=True, autoincrement=True)
    desc_tipopagamento = db.Column(db.String(50), nullable=False)
    status_tipopagamento = db.Column(db.Integer, nullable=False)
    def __repr__(self):
        return '<Name %r>' % self.name 

#---------------------------------------------------------------------------------------------------------------------------------
#TABELA: ESTACIONAMENTO
#ORIGEM: BANCO DE DADOS
#---------------------------------------------------------------------------------------------------------------------------------
class tb_estacionamento(db.Model):
    cod_estacionamento = db.Column(db.Integer, primary_key=True, autoincrement=True)
    placa_estacionamento = db.Column(db.String(50), nullable=False)
    status_estacionamento = db.Column(db.Integer, nullable=False)
    cod_tipopagamento = db.Column(db.Integer, nullable=False)
    cod_veiculo = db.Column(db.Integer, nullable=False)
    valor_estacionamento = db.Column(db.Float, nullable=False)
    entrada_estacionamento = db.Column(db.DateTime, nullable=False)
    saida_estacionamento = db.Column(db.DateTime, nullable=False)
    def __repr__(self):
        return '<Name %r>' % self.name
 


