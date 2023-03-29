from app.data.sdoh_questions import SDOH_QUESTIONS
from urllib.parse import parse_qs
# from helpers.deid import deidentify_data

def decode_form(form):
    try:
        form_dict = parse_qs(form)
        for key, value in form_dict.items():
            form_dict[key] = str(value[0])
        return form_dict
    except Exception as e:
        return e
    
def build_survey(form):
    survey = {}
    for entry in form:
        survey[str(entry.question_id)] = {
            "question_id": str(entry.question_id),
            "question": entry.question,
            "answer": entry.answer
        }
    return survey

# def build_survey(form_data):
#     survey = {}
#     cur_question = 1
#     while f"question-{cur_question}" in form_data:
#         survey[str(cur_question)] = {
#             "question_id": str(cur_question),
#             "question": SDOH_QUESTIONS[cur_question - 1]['question'],
#             "answer": form_data[f"question-{cur_question}"]
#             # "answer": deidentify_data(form_data[f"question-{cur_question}"])
#         }
#         cur_question += 1
#     return survey
