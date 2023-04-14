from app.domain.base_domain import BaseDomain
from app.models import AnswerModel, SurveyModel
from app.repository.base_repository import BaseRepository

class SurveysDomain(BaseDomain):
    def __init__(self, repository: BaseRepository, questions_domain: BaseDomain, report_domain: BaseDomain):
        super().__init__(repository)
        self.__repository = repository
        self.__report_domain = report_domain
        DEFAULT_SURVEY = {}
        QUESTIONS = questions_domain.get_all()
        for question in QUESTIONS:
            DEFAULT_SURVEY[question['qid']] = {
                'qid': question['qid'],
                'question': question['question'],
            }
        self.DEFAULT_SURVEY = DEFAULT_SURVEY

    def new_survey(self):
        survey = SurveyModel(survey=self.DEFAULT_SURVEY)
        return self.__repository.create(survey.dict())
                                        
    def add_answer(self, answer: AnswerModel):
        survey_obj = SurveyModel(**self.get(answer.sid))
        survey_obj.survey[answer.qid].answer = answer.answer
        survey_obj.cur_qid = str(int(survey_obj.cur_qid) + 1)
        self.update(survey_obj)

        if int(survey_obj.cur_qid) > len(survey_obj.survey):
            return self.__report_domain.create(survey_obj)
        else:
            return survey_obj.survey[survey_obj.cur_qid]
