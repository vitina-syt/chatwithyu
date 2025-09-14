#!/usr/bin/env python3
"""
鸢尾花数据集数据导出脚本
将数据集信息保存到文件中
"""

import os
import numpy as np
import pandas as pd
from sklearn.datasets import load_iris

def create_data_folder():
    """创建数据文件夹"""
    data_dir = "ML/data"
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
        print(f"✅ 创建文件夹: {data_dir}")
    return data_dir

def save_iris_data():
    """保存鸢尾花数据集到文件"""
    # 加载数据
    iris = load_iris()
    
    # 创建数据文件夹
    data_dir = create_data_folder()
    
    # 1. 保存原始数据为CSV
    df = pd.DataFrame(iris.data, columns=iris.feature_names)
    df['target'] = iris.target
    df['target_name'] = [iris.target_names[i] for i in iris.target]
    
    csv_file = os.path.join(data_dir, "iris_data.csv")
    df.to_csv(csv_file, index=False)
    print(f"✅ 保存CSV文件: {csv_file}")
    
    # 2. 保存数据信息为文本文件
    info_file = os.path.join(data_dir, "iris_info.txt")
    with open(info_file, 'w', encoding='utf-8') as f:
        f.write("鸢尾花数据集信息\n")
        f.write("=" * 50 + "\n\n")
        
        f.write("数据集概述:\n")
        f.write(f"- 样本数量: {iris.data.shape[0]}\n")
        f.write(f"- 特征数量: {iris.data.shape[1]}\n")
        f.write(f"- 类别数量: {len(iris.target_names)}\n\n")
        
        f.write("特征名称:\n")
        for i, name in enumerate(iris.feature_names):
            f.write(f"{i+1}. {name}\n")
        f.write("\n")
        
        f.write("类别名称:\n")
        for i, name in enumerate(iris.target_names):
            f.write(f"{i}. {name}\n")
        f.write("\n")
        
        f.write("数据统计信息:\n")
        f.write("-" * 30 + "\n")
        for i, feature in enumerate(iris.feature_names):
            f.write(f"{feature}:\n")
            f.write(f"  最小值: {iris.data[:, i].min():.2f}\n")
            f.write(f"  最大值: {iris.data[:, i].max():.2f}\n")
            f.write(f"  平均值: {iris.data[:, i].mean():.2f}\n")
            f.write(f"  标准差: {iris.data[:, i].std():.2f}\n\n")
        
        f.write("类别分布:\n")
        f.write("-" * 30 + "\n")
        unique, counts = np.unique(iris.target, return_counts=True)
        for i, (target, count) in enumerate(zip(unique, counts)):
            f.write(f"{iris.target_names[target]}: {count} 个样本\n")
    
    print(f"✅ 保存信息文件: {info_file}")
    
    # 3. 保存原始数据为numpy格式
    np_file = os.path.join(data_dir, "iris_data.npy")
    np.save(np_file, iris.data)
    print(f"✅ 保存numpy文件: {np_file}")
    
    # 4. 保存目标标签
    target_file = os.path.join(data_dir, "iris_target.npy")
    np.save(target_file, iris.target)
    print(f"✅ 保存目标文件: {target_file}")
    
    # 5. 保存元数据
    metadata_file = os.path.join(data_dir, "iris_metadata.json")
    import json
    metadata = {
        "feature_names": iris.feature_names.tolist(),
        "target_names": iris.target_names.tolist(),
        "data_shape": iris.data.shape,
        "description": "鸢尾花数据集 - 经典的机器学习数据集"
    }
    with open(metadata_file, 'w', encoding='utf-8') as f:
        json.dump(metadata, f, ensure_ascii=False, indent=2)
    print(f"✅ 保存元数据文件: {metadata_file}")
    
    return data_dir

def main():
    """主函数"""
    print("🌸 鸢尾花数据集导出工具")
    print("=" * 50)
    
    try:
        data_dir = save_iris_data()
        
        print("\n🎉 数据导出完成!")
        print(f"📁 数据保存在: {data_dir}")
        print("\n📋 生成的文件:")
        print("  - iris_data.csv (CSV格式数据)")
        print("  - iris_info.txt (数据信息)")
        print("  - iris_data.npy (numpy数据)")
        print("  - iris_target.npy (目标标签)")
        print("  - iris_metadata.json (元数据)")
        
    except Exception as e:
        print(f"❌ 导出失败: {e}")

if __name__ == "__main__":
    main()
