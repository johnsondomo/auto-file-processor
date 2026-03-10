# Auto File Processor 📁

一个简单实用的批量文件处理工具，帮你自动化处理重复的文件操作。

## ✨ 功能特点

- 🔤 批量重命名文件（支持自定义模板）
- 🔄 批量修改文件扩展名
- 📊 导出文件信息（JSON 格式）
- 🎯 支持文件类型过滤
- 🔍 预览模式（dry-run）

## 🚀 快速开始

### 安装

无需安装，直接运行：

```bash
# 确保有 Python 3.6+
python3 auto_file_processor.py --help
```

### 使用示例

```bash
# 1. 列出目录下所有文件
python3 auto_file_processor.py /path/to/dir --list

# 2. 列出特定类型文件
python3 auto_file_processor.py /path/to/dir --list --ext .txt

# 3. 批量重命名（预览）
python3 auto_file_processor.py /path/to/dir --rename "{index}_{name}" --dry-run

# 4. 批量重命名（实际执行）
python3 auto_file_processor.py /path/to/dir --rename "{index}_{name}"

# 5. 修改扩展名（预览）
python3 auto_file_processor.py /path/to/dir --change-ext .txt .md --dry-run

# 6. 修改扩展名（实际执行）
python3 auto_file_processor.py /path/to/dir --change-ext .txt .md

# 7. 导出文件信息
python3 auto_file_processor.py /path/to/dir --export
```

## 📋 重命名模板变量

| 变量 | 说明 | 示例 |
|------|------|------|
| `{name}` | 原文件名 | `report` |
| `{index}` | 序号（3 位） | `001`, `002` |
| `{date}` | 当前日期 | `20260309` |
| `{prefix}` | 前缀 | `file` |
| `{suffix}` | 后缀 | `` |

### 模板示例

```bash
# 添加序号前缀
--rename "{index}_{name}"
# 结果：001_report.txt, 002_summary.txt

# 添加日期前缀
--rename "backup_{date}_{name}"
# 结果：backup_20260309_report.txt

# 添加固定前缀
--rename "processed_{name}"
# 结果：processed_report.txt
```

## 💡 使用场景

- 📸 批量整理照片文件名
- 📄 统一文档命名格式
- 🔄 批量转换文件扩展名
- 📊 生成文件清单

## 🛠️ 定制服务

需要定制功能？比如：
- 特定格式的文件处理
- 与其他工具集成
- 图形界面版本
- 企业批量部署

**联系我：**
- 📧 GitHub Issues
- 💰 定制价格：200 元起

## 📄 许可证

MIT License - 免费使用，欢迎贡献

---

**觉得有用？给个 ⭐Star 支持一下！**
