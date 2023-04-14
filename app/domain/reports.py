from typing import List
from app.domain.base_domain import BaseDomain
from app.models import ReportsModel, SurveyModel
from app.repository.base_repository import BaseRepository
from ..utils.gpt_handler import build_report

class ReportsDomain(BaseDomain):
    def __init__(self, repository: BaseRepository) -> None:
        super().__init__(repository)
        self.__repository = repository

    # Override create method to generate report
    def create(self, survey: SurveyModel):
        report: ReportsModel = build_report(survey.dict())
        return self.__repository.create(report)