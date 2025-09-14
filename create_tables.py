#!/usr/bin/env python3
"""
数据库建表脚本
用于在MySQL中创建所有必要的表
"""

import sys
import os
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.src.models.database import engine, init_db
from backend.src.models.db_models import Base

def create_tables():
    """创建数据库表"""
    print("🏗️  开始创建数据库表...")
    print("=" * 50)
    
    try:
        # 创建所有表
        init_db()
        print("✅ 数据库表创建成功!")
        
        # 验证表是否创建
        with engine.connect() as connection:
            result = connection.execute(text("SHOW TABLES"))
            tables = [row[0] for row in result.fetchall()]
            
            expected_tables = ['pdf_files', 'conversations', 'document_chunks', 'system_logs', 'user_sessions']
            
            print("\n📋 创建的表:")
            for table in expected_tables:
                if table in tables:
                    print(f"  ✅ {table}")
                else:
                    print(f"  ❌ {table} - 未找到")
        
        return True
        
    except SQLAlchemyError as e:
        print(f"❌ 创建表失败: {e}")
        return False
    except Exception as e:
        print(f"❌ 未知错误: {e}")
        return False

def test_connection():
    """测试数据库连接"""
    print("🔍 测试数据库连接...")
    print("=" * 50)
    
    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1 as test"))
            test_value = result.fetchone()[0]
            
            if test_value == 1:
                print("✅ 数据库连接成功!")
                return True
            else:
                print("❌ 数据库连接测试失败!")
                return False
                
    except SQLAlchemyError as e:
        print(f"❌ 数据库连接失败: {e}")
        print("\n💡 解决方案:")
        print("1. 确保MySQL容器正在运行: docker ps | grep mysql")
        print("2. 启动MySQL容器: docker-compose up -d mysql-db")
        print("3. 等待容器完全启动（约30秒）")
        return False

def main():
    """主函数"""
    print("🚀 PDF QA 数据库建表工具")
    print("=" * 60)
    
    # 测试连接
    if not test_connection():
        print("\n❌ 无法连接到数据库，请检查MySQL服务状态")
        return 1
    
    # 创建表
    if create_tables():
        print("\n🎉 数据库表创建完成!")
        print("\n📊 现在您可以:")
        print("1. 启动API服务器")
        print("2. 上传PDF文件")
        print("3. 开始问答对话")
        return 0
    else:
        print("\n❌ 建表失败")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
