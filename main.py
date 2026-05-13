import pandas as pd
import matplotlib.pyplot as plt

# 讀取 CSV 資料
data = pd.read_csv("data/student_data.csv")

# 計算各題型正確率
accuracy = data.groupby("question_type")["correct"].mean()

# 顯示數據
print("\n=== 各題型正確率 ===")
print(accuracy)

# 畫長條圖
accuracy.plot(kind="bar")

# 圖表標題
plt.title("English Ability Analysis")

# Y 軸名稱
plt.ylabel("Accuracy")

# 顯示圖表
plt.show()