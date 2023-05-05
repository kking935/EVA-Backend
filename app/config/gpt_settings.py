MODEL = "gpt-3.5-turbo"
# MODEL = "gpt-4"

# MAX_TOKENS = 100
MAX_TOKENS = 500
TEMPERATURE = 0

# INITIAL_SYSTEM_PROMPT = "You are a medical assistant designed to identify social determinants \
#     of health from patient free response answers to different questions. Here are the 5 \
#     key domains outlining social determinants of health, as well as their ID, their \
#     subdomains, and the subdomain IDs- "
INITIAL_SYSTEM_PROMPT = "You are a medical assistant designed to identify negative social risk factors \
    related to determinants of health from patient free response answers to different questions. \
    You only report risk factors that are bad, not risk factors that are good. \
    Here are the 5 key domains outlining social determinants of health, as well as their their \
    subdomains- "

INITIAL_QA_EXAMPLES = [
    {
        "user_prompts": [
            "Question 1: Describe your housing situation.", 
            "Answer 1: I am currently homeless.",
        ],
        "assistant_response": "Economic Stability: Housing Instability, Poverty. Neighborhood and Built Environment: Environmental Conditions, Quality of Housing."
    },
    {
        "user_prompts": [
            "Question 2: What is the highest level of education you have acquired?", 
            "Answer 2: I graduated from Virginia Tech with a bachelor's degree in finance.",
        ],
        "assistant_response": ""
    },
    {
        "user_prompts": [
            "Summarize the patient's key social risk factors with direct references from their answers.",
        ],
        "assistant_response": "The patient appears to be experiencing Housing Instability and Poverty, given that they reported that they are 'currently homeless'. In the context of homelessness, this would also imply that the patient is at risk in regards to Environmental Conditions and Quality of Housing and Quality of Housing."
    }
]

FORM_TITLE = "MASLOW SDOH Survey"
EMAIL_RECIPIENT = "kking935@vt.edu"