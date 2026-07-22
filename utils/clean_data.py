import pandas as pd


def clean_dataset(df):

    cleaned_df = df.copy()

    report = []

    # -----------------------------
    # Remove Duplicates
    # -----------------------------
    duplicates = cleaned_df.duplicated().sum()

    if duplicates > 0:
        cleaned_df = cleaned_df.drop_duplicates()
        report.append(f"✅ Removed {duplicates} duplicate rows.")

    # -----------------------------
    # Fill Missing Values
    # -----------------------------
    for col in cleaned_df.columns:

        if cleaned_df[col].dtype in ["int64", "float64"]:

            if cleaned_df[col].isnull().sum() > 0:

                cleaned_df[col] = cleaned_df[col].fillna(
                    cleaned_df[col].median()
                )

                report.append(
                    f"✅ Filled missing values in '{col}' using median."
                )

        else:

            if cleaned_df[col].isnull().sum() > 0:

                cleaned_df[col] = cleaned_df[col].fillna(
                    cleaned_df[col].mode()[0]
                )

                report.append(
                    f"✅ Filled missing values in '{col}' using mode."
                )

    return cleaned_df, report