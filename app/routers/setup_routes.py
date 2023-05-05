
from app.domain.base_domain import BaseDomain
from app.domain.reports import ReportsDomain
from app.domain.surveys import SurveysDomain
from app.models import LabelsModel, QuestionsModel, ReportsModel, SurveyModel, UsersModel
from app.repository.base_repository import BaseRepository
from app.repository.custom_id import CustomIdRepository, custom_label_id, custom_question_id, custom_report_id
from app.routers.base_router import create_base_router
from app.routers.read_only import create_read_only_router
from app.routers.surveys import create_survey_router

def setup_routes(app, db):
    questions_repository = CustomIdRepository(db=db, table_name='Questions', table_key='qid', custom_id_function=custom_question_id)
    questions_domain = BaseDomain(repository=questions_repository)
    # questions_router = create_read_only_router(domain=questions_domain, item_name='questions', model=QuestionsModel)
    questions_router = create_base_router(domain=questions_domain, item_name='questions', model=QuestionsModel)
    app.include_router(questions_router)

    labels_repository = CustomIdRepository(db=db, table_name='Labels', table_key='lid', custom_id_function=custom_label_id)
    labels_domain = BaseDomain(repository=labels_repository)
    labels_router = create_read_only_router(domain=labels_domain, item_name='labels', model=LabelsModel)
    app.include_router(labels_router)



    users_repository = BaseRepository(db=db, table_name='Users', table_key='uid')
    users_domain = BaseDomain(repository=users_repository)
    users_router = create_base_router(domain=users_domain, item_name='users', model=UsersModel)
    app.include_router(users_router)

    reports_repository = CustomIdRepository(db=db, table_name='Reports', table_key='rid', custom_id_function=custom_report_id)
    reports_domain = ReportsDomain(repository=reports_repository)
    reports_router = create_base_router(domain=reports_domain, item_name='reports', model=ReportsModel, create_request_model=SurveyModel)
    app.include_router(reports_router)

    surveys_repository = BaseRepository(db=db, table_name='Surveys', table_key='sid')
    surveys_domain = SurveysDomain(repository=surveys_repository, questions_domain=questions_domain, report_domain=reports_domain)
    surveys_router = create_survey_router(domain=surveys_domain)
    app.include_router(surveys_router)
