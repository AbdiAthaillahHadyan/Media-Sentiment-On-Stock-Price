import seaborn as sns
import matplotlib.pyplot as plt


def create_scatterplot(data, x, y, title, file_path):
    try:
        sns.regplot(x=data[x], y=data[y], scatter_kws={"alpha":0.6})
        plt.xlabel(f"{x.replace('_', ' ').title()}")
        plt.ylabel(f"{y.replace('_', ' ').title()}")
        plt.title(title)
        plt.savefig(file_path)
        print(f"Saved {file_path}")
        plt.close()
    except Exception as e:
        print(f"failed to save scatterplot {file_path}: {e}")