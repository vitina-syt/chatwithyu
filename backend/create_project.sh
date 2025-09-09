#!/bin/bash
# create_project.sh

PROJECT_NAME="backend"

# 创建目录结构
mkdir -p $PROJECT_NAME/{app,tests,scripts,alembic}
mkdir -p $PROJECT_NAME/app/{core,models,schemas,routes,utils,db,middleware}

# 创建基础文件
touch $PROJECT_NAME/app/__init__.py
touch $PROJECT_NAME/app/main.py
touch $PROJECT_NAME/app/core/__init__.py
touch $PROJECT_NAME/app/core/config.py
touch $PROJECT_NAME/app/models/__init__.py
touch $PROJECT_NAME/app/schemas/__init__.py
touch $PROJECT_NAME/app/routes/__init__.py
touch $PROJECT_NAME/app/utils/__init__.py
touch $PROJECT_NAME/app/db/__init__.py
touch $PROJECT_NAME/app/middleware/__init__.py

# 创建配置文件
# touch $PROJECT_NAME/requirements.txt
# touch $PROJECT_NAME/.env
touch $PROJECT_NAME/.gitignore

echo "项目结构创建完成！"
