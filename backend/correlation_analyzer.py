import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

prices = pd.read_csv("data/prices_original.csv")
prices = prices.drop(columns=['date'])

correlation_matrix = prices.corr()

# correlation heatmap
plt.figure(figsize=(20, 16))
sns.heatmap(correlation_matrix,
            annot=True,
            fmt='.2f',
            cmap='coolwarm',
            center=0,
            square=True,
            linewidths=2,
            cbar_kws={"shrink": 0.8},
            annot_kws={"size": 8})
plt.title('Cryptocurrency Price Correlation Heatmap', fontsize=16, pad=20)
plt.xticks(rotation=45, ha='right', fontsize=10)
plt.yticks(rotation=0, fontsize=10)
plt.tight_layout()
plt.savefig('data/correlation_heatmap.png', dpi=300, bbox_inches='tight')
plt.show()