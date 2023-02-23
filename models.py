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
    ddesc_marcaveiculo = db.Column(db.String(50), nullable=False)
    status_marcaveiculo = db.Column(db.Integer, nullable=False)
    def __repr__(self):
        return '<Name %r>' % self.name  