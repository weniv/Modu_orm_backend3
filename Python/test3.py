# pandas 데이터 프래임 셈플
import pandas as pd

data = {
    "name": ["A", "B", "C", "D", "E"],
    "score": [100, 90, 80, 70, 60],
    "grade": ["A", "B", "C", "D", "F"],
}

df = pd.DataFrame(data)
df
