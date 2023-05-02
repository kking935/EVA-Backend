
from app.domain.base_domain import BaseDomain
from app.internal.db import initialize_db
from app.repository.base_repository import BaseRepository

db = initialize_db()

surveys_repository = BaseRepository(db=db, table_name='Surveys', table_key='sid')
surveys_domain = BaseDomain(repository=surveys_repository)

surveys = surveys_domain.get_all()
for question in surveys:
    print('deleting survey...')
    surveys_domain.delete(question['sid'])



reports_repository = BaseRepository(db=db, table_name='Reports', table_key='rid')
reports_domain = BaseDomain(repository=reports_repository)

reports = reports_domain.get_all()
for question in reports:
    print('deleting survey...')
    reports_domain.delete(question['rid'])
