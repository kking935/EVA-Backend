MODEL = "gpt-3.5-turbo"
MAX_TOKENS = 100
TEMPERATURE = 0

INITIAL_SYSTEM_PROMPT = "You are a medical assistant designed to identify social determinants \
    of health from patient free response answers to different questions. Here are the 5 \
    key domains outlining social determinants of health, as well as their ID, their \
    subdomains, and the subdomain IDs- "

INITIAL_QA_EXAMPLES = [
    {
        "user_prompts": [
            "Question 1: Describe your housing situation.", 
            "Answer 1: I am currently homeless.",
        ],
        "assistant_response": "Economic Stability (10): Housing Instability (13), Poverty (14). Neighborhood and Built Environment (40): Environmental Conditions (43), Quality of Housing (44)"
    },
        {
        "user_prompts": [
            "Summarize the patient's key social risk factors with direct references from their answers.",
        ],
        "assistant_response": "The patient appears to be experiencing Housing Instability (13) and Poverty (14), given that they reported that they are 'currently homeless'. In the context of homelessness, this would also imply that the patient is at risk in regards to Environmental Conditions (43) and Quality of Housing (44) and Quality of Housing (44)."
    }
]

FORM_TITLE = "MASLOW SDOH Survey"
EMAIL_RECIPIENT = "kking935@vt.edu"