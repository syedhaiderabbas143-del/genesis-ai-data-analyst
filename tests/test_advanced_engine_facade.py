import pandas as pd
from services.advanced_engine_facade import dashboard_with_engine, ask_with_engine

def test_facade_is_dataframe_scoped():
    df = pd.DataFrame({"sales": [1, 2, 3], "cost": [2, 4, 6]})
    assert dashboard_with_engine(df)["rows"] == 3
    assert ask_with_engine(df, "summary")["rows"] == 3
