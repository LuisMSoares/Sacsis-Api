from os import environ
from app.db import db, UserModel
from app import app


with app.app_context():
    try:
        # remove this in production
        db.drop_all()
        print(' * Drop all tables!')

        db.create_all()
    except:
        ...
    #Master Administrator Registration
    user = UserModel.query.filter_by(nome='Administrador Mestre').first()
    if not user:
        user = UserModel(
            nome='Administrador Mestre',
            matricula='0', cpf='0', rg='0',
            camiseta='0', admin=True
        )
    user.email = environ.get('MASTER_ADM_LOGIN','admin')
    user.hash_password( environ.get('MASTER_ADM_PASSWORD','admin') )
    user.activate_account()
    try:
        db.session.add(user)
        db.session.commit()
    except:
        db.session.rollback()