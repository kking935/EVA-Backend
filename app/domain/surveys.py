from app.domain.base_domain import BaseDomain
from app.domain.reports import ReportsDomain
from app.models import AnswerModel, SurveyModel
from app.repository.base_repository import BaseRepository
from app.utils.gpt_handler import finalize_survey, generate_individual_risks, initialize_survey

class SurveysDomain(BaseDomain):
    def __init__(self, repository: BaseRepository, questions_domain: BaseDomain, report_domain: ReportsDomain):
        super().__init__(repository)
        self.__repository = repository
        self.__report_domain = report_domain
        self.__questions_domain = questions_domain

    def create_default_survey(self):
        default_survey = {}
        QUESTIONS = self.__questions_domain.get_all()
        for question in QUESTIONS:
            default_survey[question['qid']] = {
                'qid': question['qid'],
                'question': question['question'],
            }
        return default_survey

    def new_survey(self):
        survey = SurveyModel(survey=self.create_default_survey())
        survey = initialize_survey(survey)
        return self.__repository.create(survey.dict())
                                        
    def add_answer(self, answer: AnswerModel):
        survey_obj = SurveyModel(**self.get(answer.sid))
        survey_obj.survey[answer.qid].answer = answer.answer
        generate_individual_risks(survey_obj, survey_obj.survey[answer.qid])

        survey_obj.cur_qid = str(int(survey_obj.cur_qid) + 1)
        self.update(survey_obj)

        if int(survey_obj.cur_qid) > len(survey_obj.survey):
            survey_obj = finalize_survey(survey_obj)
            return self.__report_domain.create(survey_obj)
        else:
            return survey_obj.survey[survey_obj.cur_qid]
