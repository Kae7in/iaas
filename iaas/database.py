# from . import app
# from flask_sqlalchemy import SQLAlchemy
# from sqlalchemy import create_engine
# from sqlalchemy.orm import scoped_session, sessionmaker
# from sqlalchemy.ext.declarative import declarative_base
# import os
#
# # engine = create_engine('sqlite:///' + os.getcwd() + '/integers.db', convert_unicode=True)
# # db_session = scoped_session(sessionmaker(autocommit=False,
# #                                          autoflush=False,
# #                                          bind=engine))
# # Base = declarative_base()
# # Base.query = db_session.query_property()
#
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////integers.db'
# db = SQLAlchemy(app)
#
#
# # def init_db():
# #     # import all modules here that might define models so that
# #     # they will be registered properly on the metadata.  Otherwise
# #     # you will have to import them first before calling init_db()
# #     import iaas.models
# #     Base.metadata.create_all(bind=engine)
