#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
批量修改文件名脚本
功能：遍历指定目录下的所有文件，识别并修改后缀为".adoc.docx"的文件，将其修改为仅保留".docx"后缀
支持预览模式和日志输出
"""

import os
import argparse
import logging
from datetime import datetime

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('rename_files.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def traverse_directory(directory):
    """遍历目录下的所有文件"""
    files_to_process = []
    try:
        for root, _, files in os.walk(directory):
            for file in files:
                file_path = os.path.join(root, file)
                if file.endswith('.adoc.docx'):
                    files_to_process.append(file_path)
        return files_to_process
    except Exception as e:
        logger.error(f"遍历目录时出错: {str(e)}")
        return []

def generate_new_filename(old_filepath):
    """生成新的文件名"""
    directory = os.path.dirname(old_filepath)
    old_filename = os.path.basename(old_filepath)
    # 移除.adoc前缀，保留.docx后缀
    new_filename = old_filename.replace('.adoc.docx', '.docx')
    return os.path.join(directory, new_filename)

def preview_rename(files_to_process):
    """预览模式，显示将要执行的修改操作"""
    logger.info("=== 预览模式 ===")
    logger.info(f"找到 {len(files_to_process)} 个需要修改的文件:")
    
    for old_filepath in files_to_process:
        new_filepath = generate_new_filename(old_filepath)
        logger.info(f"将修改: {old_filepath} -> {new_filepath}")
    
    logger.info("=== 预览完成 ===")

def execute_rename(files_to_process):
    """执行实际的重命名操作"""
    logger.info("=== 执行模式 ===")
    success_count = 0
    error_count = 0
    
    for old_filepath in files_to_process:
        new_filepath = generate_new_filename(old_filepath)
        try:
            os.rename(old_filepath, new_filepath)
            logger.info(f"成功修改: {old_filepath} -> {new_filepath}")
            success_count += 1
        except Exception as e:
            logger.error(f"修改失败 {old_filepath}: {str(e)}")
            error_count += 1
    
    logger.info(f"=== 执行完成 ===")
    logger.info(f"成功修改: {success_count} 个文件")
    logger.info(f"修改失败: {error_count} 个文件")

def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='批量修改文件名脚本')
    parser.add_argument('directory', help='要遍历的目录路径')
    parser.add_argument('--preview', action='store_true', help='预览模式，不执行实际修改')
    args = parser.parse_args()
    
    directory = args.directory
    if not os.path.exists(directory):
        logger.error(f"目录不存在: {directory}")
        return
    
    if not os.path.isdir(directory):
        logger.error(f"路径不是目录: {directory}")
        return
    
    logger.info(f"开始处理目录: {directory}")
    logger.info(f"开始时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # 遍历目录，找到需要修改的文件
    files_to_process = traverse_directory(directory)
    
    if not files_to_process:
        logger.info("未找到需要修改的文件")
        return
    
    # 根据模式执行操作
    if args.preview:
        preview_rename(files_to_process)
    else:
        execute_rename(files_to_process)
    
    logger.info(f"结束时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    main()
