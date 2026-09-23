# Instagram AI Account Analyzer

一个基于 Make、Apify 和 OpenAI API 搭建的 Instagram 账号内容分析 Agent。

输入 Instagram 账号链接后，系统会自动抓取近期帖子，完成数据清洗、排序和聚合，并调用大语言模型生成结构化账号分析报告，最终输出至 Google Docs。

## 项目流程

```text
本地网页表单
    ↓ Webhook
Make 自动化工作流
    ↓
Apify Instagram Scraper
    ↓
账号归属过滤与数据清洗
    ↓
按发布时间倒序排列，选取近期 20 条帖子
    ↓
OpenAI 结构化分析
    ↓
Google Docs 分析报告
```

## 核心功能

- 输入 Instagram 账号链接后自动触发分析流程
- 抓取并筛选目标账号的近期帖子
- 按发布时间倒序排列，选取近期 20 条内容
- 聚合文案、发布时间、点赞数、评论数、播放量和原帖链接
- 保留每条帖子的原始文案
- 输出账号概览、内容主题、发布规律和互动表现
- 自动生成并保存 Google Docs 报告
- 支持本地网页表单重复提交不同账号

## 技术工具

- **Make**：工作流编排与模块连接
- **Apify**：Instagram 公开数据抓取
- **OpenAI API**：内容理解与结构化报告生成
- **Google Docs**：报告输出与存档
- **Python Web Server**：本地表单和 Webhook 转发

## 本地运行

本项目使用 Python 标准库，无需安装第三方依赖。

1. 设置 Make Webhook 地址：

   ```bash
   export MAKE_WEBHOOK_URL="你的 Make Webhook 地址"
   ```

2. 启动本地服务：

   ```bash
   python3 src/instagram_server.py
   ```

3. 浏览器访问：

   ```text
   http://127.0.0.1:8769/
   ```

4. 输入 Instagram 账号链接和 Webhook API Key，提交分析任务。

## 报告内容

- 执行摘要
- 账号概览
- 内容主题及证据
- 发布规律
- 平均互动表现
- 高互动帖子
- 近期帖子原始文案
- 数据范围与分析限制

## 安全说明

- 仓库不包含真实 Webhook 地址、OpenAI Key、Apify Token 或 Webhook API Key。
- 敏感配置通过环境变量或运行时输入提供。
- `.env`、日志、缓存和本地应用文件已加入 `.gitignore`。
- 请仅分析公开账号和公开内容，并遵守平台规则及适用法律。

## 项目成果

完成了从账号链接输入、帖子抓取、数据整理、AI 分析到文档生成的端到端自动化流程，并针对字段映射、数据聚合、帖子排序、JSON 输出和 API 异常进行了调试与优化。

