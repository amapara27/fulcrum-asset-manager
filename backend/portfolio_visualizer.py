import matplotlib.pyplot as plt
import pandas as pd
from sklearn.decomposition import PCA
from datetime import datetime
import os

# creates and saves scatterplot visualization
def save_portfolio_scatterplot(df, clustered_coins, user_assets, output_dir="data/visualizations"):
    os.makedirs(output_dir, exist_ok=True)

    pca = PCA(n_components=2)
    pca_components = pca.fit_transform(df)

    pca_df = pd.DataFrame(
        data=pca_components,
        columns=['PC1', 'PC2']
    )
    pca_df['Ticker'] = df.index
    pca_df['Cluster'] = clustered_coins.values

    plt.figure(figsize=(14, 10))

    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A']
    cluster_names = [f'Cluster {i}' for i in range(len(colors))]


    for i in range(len(colors)):
        cluster_data = pca_df[pca_df['Cluster'] == i]
        plt.scatter(
            cluster_data['PC1'],
            cluster_data['PC2'],
            c=colors[i],
            label=cluster_names[i],
            alpha=0.4,
            s=80,
            edgecolors='none'
        )

    user_data = pca_df[pca_df['Ticker'].isin(user_assets)]

    if not user_data.empty:
        # plot user assets with larger markers and borders
        for i in range(len(colors)):
            user_cluster_data = user_data[user_data['Cluster'] == i]
            if not user_cluster_data.empty:
                plt.scatter(
                    user_cluster_data['PC1'],
                    user_cluster_data['PC2'],
                    c=colors[i],
                    s=300,
                    alpha=0.9,
                    edgecolors='black',
                    linewidths=2.5,
                    marker='*',
                    zorder=5
                )

        # add labels for user's assets
        for idx, row in user_data.iterrows():
            plt.annotate(
                row['Ticker'],
                (row['PC1'], row['PC2']),
                fontsize=11,
                fontweight='bold',
                alpha=1.0,
                xytext=(5, 5),
                textcoords='offset points',
                bbox=dict(boxstyle='round,pad=0.3', facecolor='yellow', alpha=0.7, edgecolor='black'),
                zorder=6
            )

    # add labels for other assets (smaller, more subtle)
    other_data = pca_df[~pca_df['Ticker'].isin(user_assets)]
    for idx, row in other_data.iterrows():
        plt.annotate(
            row['Ticker'],
            (row['PC1'], row['PC2']),
            fontsize=7,
            alpha=0.5,
            xytext=(2, 2),
            textcoords='offset points'
        )

    # add custom legend entry for user assets
    if not user_data.empty:
        plt.scatter([], [], c='gold', s=300, marker='*',
                   edgecolors='black', linewidths=2.5,
                   label='Your Portfolio', alpha=0.9)

    variance_ratio = pca.explained_variance_ratio_
    plt.xlabel(f'First Principal Component ({variance_ratio[0]:.1%} variance)', fontsize=13)
    plt.ylabel(f'Second Principal Component ({variance_ratio[1]:.1%} variance)', fontsize=13)

    title = 'Asset Clustering Visualization'
    if user_data.empty:
        subtitle = f'(Total Variance Explained: {variance_ratio.sum():.1%})'
    else:
        subtitle = f'Your {len(user_assets)} Asset{"s" if len(user_assets) > 1 else ""} Highlighted ★ (Total Variance: {variance_ratio.sum():.1%})'

    plt.title(f'{title}\n{subtitle}', fontsize=15, fontweight='bold', pad=20)
    plt.legend(loc='best', fontsize=10, framealpha=0.9)
    plt.grid(True, alpha=0.2, linestyle='--')
    plt.tight_layout()

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"portfolio_clusters_{timestamp}.png"
    filepath = os.path.join(output_dir, filename)

    # Save the figure
    plt.savefig(filepath, dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()

    return filepath


def generate_cluster_report(df, clustered_coins, user_assets, output_dir="data/visualizations"):
    filepath = save_portfolio_scatterplot(df, clustered_coins, user_assets, output_dir)
    return filepath
