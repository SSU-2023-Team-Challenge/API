from config.default import *

SQLALCHEMY_DATABASE_URI = 'sqlite:///{}'.format(os.path.join(BASE_DIR, 'pybo.db'))
SQLALCHEMY_TRACK_MODIFICATIONS = False
SECRET_KEY = b'\x90\xa2VH]r\x0e\xf9\x01\xbc\x7f\xff\x1d\x9b[\x15'

