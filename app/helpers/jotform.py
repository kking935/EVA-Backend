import os
from dotenv import load_dotenv
load_dotenv()
import requests
from data.short_questions import SDOH_QUESTIONS
from data.settings import FORM_TITLE, EMAIL_RECIPIENT

URL = f"https://api.jotform.com/form?apiKey={os.environ.get('JOTFORM_API_KEY')}"
HEADERS = { "Content-Type": "application/x-www-form-urlencoded" }
DEFAULT_FORM_DATA = {
    "emails[0][type]": "notification",
    "emails[0][name]": "notification",
    "emails[0][from]": "default",
    "emails[0][to]": EMAIL_RECIPIENT,
    "emails[0][subject]": "New MASLOW SDOH Survey Submission",
    "emails[0][html]": "false",

    "properties[title]": FORM_TITLE,
    "properties[labelAlign]": "Top",
    "properties[background]": "white",
    # "properties[height]": 1000,
    # "properties[formWidth]": 600,
    # "properties[labelWidth]": 1,
    "properties[sendpostdata]": "Yes",
    "properties[activeRedirect]": "thankurl",
    "properties[thankurl]": "http://localhost:5000/api/submit",

}

DEFAULT_QUESTION_DATA = {
    "type": "control_textarea",
    "rows": 8,
    "cols": 75,
    "validation": "None",
    "required": "No",
    "readonly": "No",
    "size": 20,
    "labelAlign": "Top",
    "hint": "",
}


def create_jotform_form():
    data = {}

    data["questions[0][type]"] = "control_head"
    data["questions[0][text]"] = FORM_TITLE
    data["questions[0][order]"] = "0"
    data["questions[0][headerType]"] = "Large"
    data["questions[0][subHeader]"] = "Please complete the form."

    for idx, question_obj in enumerate(SDOH_QUESTIONS):
        id = str(question_obj['question_id'])
        data[f"questions[{id}][text]"] = question_obj['question']
        data[f"questions[{id}][order]"] = str(idx + 1)
        data[f"questions[{id}][name]"] = "question-" + id
        for key, value in DEFAULT_QUESTION_DATA.items():
            data[f"questions[{id}][{key}]"] = value

    cur_order = str(len(SDOH_QUESTIONS) + 1)
    data[f"questions[{cur_order}][text]"] = "SUBMIT"
    data[f"questions[{cur_order}][order]"] = str(cur_order)
    data[f"questions[{cur_order}][labelALign]"] = "Right"
    data[f"questions[{cur_order}][type]"] = "control_button"

    data = {**data, **DEFAULT_FORM_DATA}
    # print(data)
    response = requests.post(URL, data=data, headers=HEADERS)
    return response.json()

form_response = create_jotform_form()
if form_response['responseCode'] != 200:
    print("ERROR: ", form_response['content'])
else:
    print("Success! ", form_response['content']['url'])

