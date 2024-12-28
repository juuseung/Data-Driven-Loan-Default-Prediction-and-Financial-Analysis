from typing import Union
import pandas as pd
from constants import *
import joblib

def preprocess(loanDF):
    """
    This function handles all the preprocessing logic of phase-1
    """
    # 1. drop un-necessary columns
    # loanDF = pd.DataFrame([data])
    # 1. Deleting unncessary columns
    
    loanDF.columns = loanDF.rename(columns=str.lower).columns
    loanDF.columns = loanDF.columns.str.replace('-', '_')
    # print(loanDF.columns)

    try:
        col_to_drop = ["id", "year", "lump_sum_payment"]
        loanDF.drop(columns=col_to_drop, axis=1, inplace=True)
    except Exception as e:
        print("INFO: Could not delete unnecssary columns")
    

    # 2. Fill null values
    # Replace null values with mean values
    # Fill null values with mean values
    loanDF.fillna(preprocessing_params["mean_values"], inplace=True)

    # Fill null values with mode values
    loanDF.fillna(preprocessing_params["mode_values"], inplace=True)

    # assert sum(loanDF.isna().sum())==0, "Total Null Values after processing should be 0"
    # 3. Creating new feature
    loanDF["loan_amount_to_property"] = (
        loanDF["loan_amount"].astype(float) / loanDF["property_value"].astype(float)
    )

    # 4. formtiing values in categorical columns
    loanDF["gender"] = loanDF["gender"].str.replace("Sex Not Available", "unknown")

    # To avoid creating multiple columns of same values, in onehot-encoding.
    loanDF["gender"] = loanDF["gender"].str.lower()
    loanDF["total_units"] = loanDF["total_units"].str.replace("U", "").astype(int)
    loanDF["age"] = loanDF["age"].str.replace(">", "over")
    loanDF["age"] = loanDF["age"].str.replace("<", "under")
    loanDF["region"] = loanDF["region"].str.replace("-", "_")
    loanDF["region"] = loanDF["region"].str.lower()
    loanDF["security_type"] = loanDF["security_type"].str.lower()

    # 5. Age encoding

    # Replace values in the 'age' column using the age_encoding dictionary
    loanDF["age"] = loanDF["age"].map(age_encoding)
    loanDF[numeric_cols] = loanDF[numeric_cols].astype(float)

    # SPlitting into numerical and categorical datasets
    numerical_df = loanDF[numeric_cols].astype(float).copy()
    categorical_df = loanDF[categorical_cols].copy()
    print("INFO: Numericals containing null values:", sum(numerical_df.isna().sum()))
    rob_scaler = joblib.load(f"{MODELS_DIR_PATH}/robust_scaler.pkl")
    numerical_df_scaled = pd.DataFrame(
        rob_scaler.transform(numerical_df), columns=numerical_df.columns
    )

    cat_encoder = joblib.load(f"{MODELS_DIR_PATH}/cat_encoder.pkl")
    categorical_df_encoded = pd.DataFrame(
        cat_encoder.transform(categorical_df),
        columns=cat_encoder.get_feature_names_out(),
    )

    loanDF_preprocessed = pd.concat(
        [numerical_df_scaled, categorical_df_encoded], axis=1
    )

    return loanDF_preprocessed

def get_df(submit_data: Union[pd.DataFrame, dict]):
    """
    This function converts python dictionary to a pandas dataframe
    """
    loanDF = None
    y_true = None
    # If submit_data is dict
    if isinstance(submit_data, dict):    
        if "Status" in submit_data.keys():
            y_true = submit_data["Status"]
            del submit_data["Status"]
            if len(submit_data)==1:
                y_true = [y_true]
        
        loanDF = pd.DataFrame([submit_data]) # just one row of data.
    # if submit_data is a df
    elif isinstance(submit_data, pd.DataFrame) and "Status" in submit_data.columns:
        y_true = submit_data["Status"]
        loanDF = submit_data.drop("Status")
    
    return loanDF, y_true

def predict(submit_data):
    """
    This is a utilty function for prediction.
    """
    # convert the given dict to a DataFrame
    loanDF, y_true = get_df(submit_data)
    # preprocess data according to phase-1
    df = preprocess(loanDF)
    
    # Loading model from phase-2
    model = joblib.load(f"{MODELS_DIR_PATH}/decision_tree.pkl")
    
    # Prediction
    y_pred = model.predict(df)
    print({"predicted":list(y_pred), "actual": list(y_true)})
    return list(y_pred), list(y_true)
