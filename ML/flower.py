from sklearn.datasets import load_iris
import os
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score

def create_data_folder():
    """创建数据文件夹"""
    data_dir = "ML/data"
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
        print(f"✅ 创建文件夹: {data_dir}")
    return data_dir

def test_iris():
    iris = load_iris()
    try:
        data_dir = create_data_folder()
        iris_data_file = os.path.join(data_dir, "iris_dataframe_data.txt")
        with open(iris_data_file, 'w', encoding='utf-8') as f:
            f.write("鸢尾花数据集信息\n")
            f.write("=" * 50 + "\n\n")
            
            f.write("数据集概述:\n")
            f.write(f"- 样本: {iris.data}\n")
            f.write(f"- 目标: {iris.target}\n")
            f.write(f"- 特征: {iris.feature_names}\n")
            f.write(f"- 类别: {iris.target_names}\n\n")
        print(f"✅ 保存信息文件: {iris_data_file}")
    except Exception as e:
        print(f"❌ 保存信息文件失败: {e}")

def test_iris_model():
    iris = load_iris()
    X_train, X_test, y_train, y_test = train_test_split(iris.data, iris.target, test_size=0.3, random_state=42)

    clf = DecisionTreeClassifier()
    clf.fit(X_train, y_train)
    y_pred = clf.predict(X_test)
    print(f"准确率: {accuracy_score(y_test, y_pred)}")

if __name__ == "__main__":
    test_iris()