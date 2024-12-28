import os
if os.getcwd().endswith("dic_project"):
    INPUT_DIR = "./datasets/"
    INPUT_FILE_PATH = "./datasets/Loan_Default.csv" # To run/debug from home directory
    MODELS_DIR_PATH = "./models"
    ROOT_DIR = './src/phase3/'
else:
    INPUT_DIR = "../../datasets/"
    MODELS_DIR_PATH = "../../models" # to run from phase3 folder
    INPUT_FILE_PATH = "../../datasets/Loan_Default.csv" # to run from phase3 folder
    ROOT_DIR = "./"

model_paths = {
    "NaiveBayes": f"{MODELS_DIR_PATH}/naive_bayes.joblib",
    "DecisionTree": f"{MODELS_DIR_PATH}/decision_tree.joblib",
}

data = {
    "ID": 24890,
    "year": 2019,
    "loan_limit": "cf",
    "Gender": "Sex Not Available",
    "approv_in_adv": "nopre",
    "loan_type": "type1",
    "loan_purpose": "p1",
    "Credit_Worthiness": "l1",
    "open_credit": "nopc",
    "business_or_commercial": "nob/c",
    "loan_amount": 116500,
    "rate_of_interest": None,
    "Interest_rate_spread": None,
    "Upfront_charges": None,
    "term": 360.0,
    "Neg_ammortization": "not_neg",
    "interest_only": "not_int",
    "lump_sum_payment": "not_lpsm",
    "property_value": 118000.0,
    "construction_type": "sb",
    "occupancy_type": "pr",
    "Secured_by": "home",
    "total_units": "1U",
    "income": 1740.0,
    "credit_type": "EXP",
    "Credit_Score": 758,
    "co-applicant_credit_type": "CIB",
    "age": "25-34",
    "submission_of_application": "to_inst",
    "LTV": 98.72881356,
    "Region": "south",
    "Security_Type": "direct",
    "Status": 1,
    "dtir1": 45.0,
}


numeric_cols = [
    "loan_amount",
    "rate_of_interest",
    "interest_rate_spread",
    "upfront_charges",
    "term",
    "property_value",
    "total_units",
    "income",
    "credit_score",
    "ltv",
    "dtir1",
    "loan_amount_to_property",
    "age",
]
categorical_cols = [
    "loan_limit",
    "gender",
    "approv_in_adv",
    "loan_type",
    "loan_purpose",
    "credit_worthiness",
    "open_credit",
    "business_or_commercial",
    "neg_ammortization",
    "interest_only",
    "construction_type",
    "occupancy_type",
    "secured_by",
    "credit_type",
    "co_applicant_credit_type",
    "submission_of_application",
    "region",
    "security_type",
]

# Load preprocessing parameters
preprocessing_params = {
    "mean_values": {
        "rate_of_interest": 4.045,
        "interest_rate_spread": 0.442,
        "upfront_charges": 3224.996,
        "term": 335.137,
        "property_value": 497893.466,
        "income": 6957.339,
        "ltv": 72.746,
        "dtir1": 37.733
    },
    "mode_values": {
        "loan_limit": "cf",
        "approv_in_adv": "nopre",
        "loan_purpose": "p3",
        "neg_ammortization": "not_neg",
        "age": "45-54",
        "submission_of_application": "to_inst",
    },
}


# We can use ordinal encoding for age, as increasing values signify higher ages.
age_encoding = {
    "under25": 1,
    "25-34": 2,
    "35-44": 3,
    "45-54": 4,
    "55-64": 5,
    "65-74": 6,
    "over74": 7,
}

