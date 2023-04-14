
from app.config.sdoh_questions import SDOH_QUESTIONS
from app.domain.base_domain import BaseDomain
from app.internal.db import initialize_db
from app.models import LabelsModel, QuestionsModel, SublabelModel
from app.repository.base_repository import BaseRepository

db = initialize_db()

questions_repository = BaseRepository(db=db, table_name='Questions', table_key='qid')
questions_domain = BaseDomain(repository=questions_repository)

questions = questions_domain.get_all()
for question in questions:
    questions_domain.delete(question['qid'])

for question in SDOH_QUESTIONS:
    labels = []
    for label in question['labels']:
        sublabels = []
        for sublabel in label['sublabels']:
            sublabels.append(SublabelModel(slid=sublabel['slid'], sublabel=sublabel['sublabel']))
        labels.append(LabelsModel(lid=label['lid'], label=label['label'], sublabels=sublabels))
    
    questions_domain.create(QuestionsModel(
        qid=question['qid'],
        question=question['question'],
        labels=labels,
    ))