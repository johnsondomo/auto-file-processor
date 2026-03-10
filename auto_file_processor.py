#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Auto File Processor - 批量文件处理工具
作者：johnsondomo
GitHub: https://github.com/johnsondomo/auto-file-processor

功能：
- 批量重命名文件
- 批量转换文件扩展名
- 批量提取文件信息
- 支持自定义规则

使用：
    python auto_file_processor.py --help
"""

import os
import sys
import argparse
import json
from datetime import datetime
from pathlib import Path


class FileProcessor:
    """文件批量处理器"""
    
    def __init__(self, directory):
        self.directory = Path(directory)
        self.results = []
    
    def list_files(self, extension=None):
        """列出目录下的文件"""
        files = []
        for f in self.directory.iterdir():
            if f.is_file():
                if extension is None or f.suffix == extension:
                    files.append(f)
        return files
    
    def batch_rename(self, pattern, extension=None):
        """
        批量重命名文件
        
        pattern 支持：
        - {name}: 原文件名
        - {index}: 序号
        - {date}: 当前日期
        - {prefix}: 前缀
        - {suffix}: 后缀
        
        示例：
        - "{prefix}_{name}" → 前缀_原文件名
        - "{index}_{name}" → 001_原文件名
        - "backup_{date}_{name}" → backup_20260309_原文件名
        """
        files = self.list_files(extension)
        results = []
        
        for index, file in enumerate(files, 1):
            old_name = file.stem
            new_name = pattern.format(
                name=old_name,
                index=str(index).zfill(3),
                date=datetime.now().strftime('%Y%m%d'),
                prefix='file',
                suffix=''
            )
            new_path = file.with_name(new_name + file.suffix)
            
            try:
                file.rename(new_path)
                results.append({
                    'old': str(file.name),
                    'new': str(new_path.name),
                    'status': 'success'
                })
            except Exception as e:
                results.append({
                    'old': str(file.name),
                    'new': str(new_path.name),
                    'status': 'error',
                    'error': str(e)
                })
        
        return results
    
    def batch_change_extension(self, old_ext, new_ext):
        """批量修改文件扩展名"""
        files = self.list_files(old_ext)
        results = []
        
        for file in files:
            new_path = file.with_suffix(new_ext)
            try:
                file.rename(new_path)
                results.append({
                    'old': str(file.name),
                    'new': str(new_path.name),
                    'status': 'success'
                })
            except Exception as e:
                results.append({
                    'old': str(file.name),
                    'new': str(new_path.name),
                    'status': 'error',
                    'error': str(e)
                })
        
        return results
    
    def get_file_info(self, extension=None):
        """获取文件信息"""
        files = self.list_files(extension)
        info = []
        
        for file in files:
            stat = file.stat()
            info.append({
                'name': file.name,
                'size': stat.st_size,
                'size_mb': round(stat.st_size / 1024 / 1024, 2),
                'created': datetime.fromtimestamp(stat.st_ctime).isoformat(),
                'modified': datetime.fromtimestamp(stat.st_mtime).isoformat(),
                'extension': file.suffix
            })
        
        return info
    
    def export_info(self, output_file='file_info.json'):
        """导出文件信息到 JSON"""
        info = self.get_file_info()
        with open(self.directory / output_file, 'w', encoding='utf-8') as f:
            json.dump(info, f, ensure_ascii=False, indent=2)
        return output_file


def main():
    parser = argparse.ArgumentParser(
        description='批量文件处理工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
示例:
  # 列出文件
  python auto_file_processor.py /path/to/dir --list
  
  # 批量重命名
  python auto_file_processor.py /path/to/dir --rename "{index}_{name}"
  
  # 修改扩展名
  python auto_file_processor.py /path/to/dir --change-ext .txt .md
  
  # 导出文件信息
  python auto_file_processor.py /path/to/dir --export
        '''
    )
    
    parser.add_argument('directory', help='目标目录')
    parser.add_argument('--list', '-l', action='store_true', help='列出文件')
    parser.add_argument('--ext', '-e', help='文件扩展名过滤 (如：.txt)')
    parser.add_argument('--rename', '-r', help='重命名模板')
    parser.add_argument('--change-ext', '-c', nargs=2, metavar=('OLD', 'NEW'), help='修改扩展名')
    parser.add_argument('--export', action='store_true', help='导出文件信息')
    parser.add_argument('--dry-run', '-n', action='store_true', help='预览操作，不实际执行')
    
    args = parser.parse_args()
    
    if not os.path.isdir(args.directory):
        print(f"错误：目录不存在 - {args.directory}")
        sys.exit(1)
    
    processor = FileProcessor(args.directory)
    
    if args.list:
        files = processor.list_files(args.ext)
        print(f"\n找到 {len(files)} 个文件:\n")
        for f in files:
            print(f"  {f.name}")
    
    elif args.rename:
        if args.dry_run:
            print("【预览模式】以下文件将被重命名:\n")
        files = processor.list_files(args.ext)
        for i, f in enumerate(files, 1):
            new_name = args.rename.format(
                name=f.stem,
                index=str(i).zfill(3),
                date=datetime.now().strftime('%Y%m%d'),
                prefix='file',
                suffix=''
            )
            print(f"  {f.name} → {new_name}{f.suffix}")
        
        if not args.dry_run:
            results = processor.batch_rename(args.rename, args.ext)
            print(f"\n处理完成：{len(results)} 个文件")
            success = sum(1 for r in results if r['status'] == 'success')
            print(f"成功：{success}, 失败：{len(results) - success}")
    
    elif args.change_ext:
        old_ext, new_ext = args.change_ext
        if not new_ext.startswith('.'):
            new_ext = '.' + new_ext
        if not old_ext.startswith('.'):
            old_ext = '.' + old_ext
            
        if args.dry_run:
            print(f"【预览模式】以下文件将从 {old_ext} 改为 {new_ext}:\n")
        files = processor.list_files(old_ext)
        for f in files:
            print(f"  {f.name} → {f.stem}{new_ext}")
        
        if not args.dry_run:
            results = processor.batch_change_extension(old_ext, new_ext)
            print(f"\n处理完成：{len(results)} 个文件")
    
    elif args.export:
        output = processor.export_info()
        print(f"文件信息已导出到：{output}")
    
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
