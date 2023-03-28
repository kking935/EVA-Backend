# SET ENVIRONMENT VARIABLES
# -------------------------
import json
import os
import subprocess

with open('spark_nlp_for_healthcare.json', 'r') as f:
    data = json.load(f)
    for key, value in data.items():
        os.environ[key] = value
        
public_version = os.environ.get('PUBLIC_VERSION')
jsl_version = os.environ.get('JSL_VERSION')
secret = os.environ.get('SECRET')

# INSTALL LIBRARIES USING ENVIRONMENT VARIABLES
# ---------------------------------------------
subprocess.call(['pip', 'install', '--upgrade', '-q', 'pyspark==3.1.2', 'spark-nlp=={}'.format(public_version)])
subprocess.call(['pip', 'install', '--upgrade', '-q', 'spark-nlp-jsl=={}'.format(jsl_version), '--extra-index-url', 'https://pypi.johnsnowlabs.com/{}'.format(secret)])
subprocess.call(['pip', 'install', '-q', 'spark-nlp-display'])

# IMPORT LIBRARIES
# ----------------
import sparknlp
import sparknlp_jsl

from sparknlp.base import *
from sparknlp.annotator import *
from sparknlp_jsl.annotator import *
from sparknlp.pretrained import PretrainedPipeline # specific to de-identification

from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.ml import Pipeline,PipelineModel
from pyspark.sql.types import StringType, IntegerType

import pandas as pd
import warnings

# CONFIGURE SPARK SESSION
# -----------------------

# Configure pd, warnings, and model settings
pd.set_option('display.max_colwidth', 200)

warnings.filterwarnings('ignore')

params = {"spark.driver.memory":"16G", 
          "spark.kryoserializer.buffer.max":"2000M", 
          "spark.driver.maxResultSize":"2000M"} 

# Start authenticated sparksession for NLP-Healthcare
spark = sparknlp_jsl.start(os.environ["SECRET"],params=params)
spark

# LOAD DE-IDENTIFICATION PIPELINE
# --------------------------------

# Download clinical_deidentification model (1.6GB) and Create the de-identification pipeline
deid_pipeline = PretrainedPipeline("clinical_deidentification", 'en', "clinical/models")

# DEFINE DE-IDENTIFICATION FUNCTION
# ---------------------------------
def deidentify_data(phi_data):
    return deid_pipeline.annotate(phi_data)[0]
