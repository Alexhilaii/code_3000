import pandas as pd

def load_data(anonymized_path, auxiliary_path):
    """
    Load anonymized and auxiliary datasets.
    """
    anon = pd.read_csv(anonymized_path)
    aux = pd.read_csv(auxiliary_path)
    return anon, aux


def link_records(anon_df, aux_df):
    """
    Attempt to link anonymized records to auxiliary records
    using exact matching on quasi-identifiers.

    Returns a DataFrame with columns:
      anon_id, matched_name
    containing ONLY uniquely matched records.
    """
    keys = ['age', 'zip3', 'gender']

    anon_unique = anon_df.drop_duplicates(subset=keys, keep=False)
    aux_unique = aux_df.drop_duplicates(subset=keys, keep=False)

    matches = anon_unique.merge(
        aux_unique,
        on=keys,
        how='inner',
    )
    matches = matches.rename(
        columns={'name': 'matched_name'}
    )

    return matches
   

def deanonymization_rate(matches_df, anon_df):
    """
    Compute the fraction of anonymized records
    that were uniquely re-identified.
    """
    if len(anon_df) == 0:
        return 0.0

    rate = matches_df['anon_id'].nunique() / len(anon_df)

    return rate
    
