# 安装指南

本指南将帮助您在 macOS 系统上安装和配置 Keynote-MCP。

## 📋 系统要求

### 必需条件
- **操作系统**: macOS 10.14 或更高版本
- **Python**: 3.8 或更高版本
- **Keynote**: 任何版本的 Keynote 应用程序
- **权限**: 系统辅助功能权限

### 可选条件
- **Unsplash API 密钥**: 用于配图功能（可选）

## 🚀 安装步骤

### 1. 安装 Python

如果您还没有安装 Python，请从 [python.org](https://www.python.org/downloads/) 下载并安装 Python 3.8+。

验证安装：
```bash
python3 --version
```

### 2. 克隆项目

```bash
git clone https://github.com/easychen/keynote-mcp.git
cd keynote-mcp
```

### 3. 创建虚拟环境

```bash
python3 -m venv venv
source venv/bin/activate
```

### 4. 安装依赖

```bash
pip install -r requirements.txt
```

### 5. 配置环境变量

复制环境变量示例文件：
```bash
cp env.example .env
```

编辑 `.env` 文件：
```bash
nano .env
```

设置必要的环境变量：
```env
# Unsplash API 配置（可选）
UNSPLASH_KEY=your_unsplash_access_key_here

# 调试配置（可选）
DEBUG=false
LOG_LEVEL=INFO
```

## 🔐 权限配置

### 1. 辅助功能权限

1. 打开 **系统偏好设置** > **安全性与隐私** > **隐私**
2. 选择 **辅助功能**
3. 点击锁图标并输入密码
4. 添加以下应用：
   - **终端** (Terminal.app)
   - **Python** (或您的 Python 解释器)

### 2. 文件和文件夹权限

1. 在 **安全性与隐私** > **隐私** 中选择 **文件和文件夹**
2. 确保 Python 有权限访问：
   - **桌面文件夹**
   - **文档文件夹**
   - **下载文件夹**

### 3. 自动化权限

1. 在 **安全性与隐私** > **隐私** 中选择 **自动化**
2. 允许 Python 控制：
   - **Keynote**
   - **System Events**

## 🧪 验证安装

### 1. 运行基本测试

```bash
python -m pytest tests/test_basic.py -v
```

### 2. 启动 MCP 服务器

```bash
python start_server.py
```

您应该看到类似以下的输出：
```
🚀 启动 Keynote-MCP 服务器...
==================================================
📝 确保 Keynote 应用已安装
🔒 确保已授予必要的系统权限
🔌 MCP 客户端可以连接到此服务器
🖼️  Unsplash配图功能已启用
==================================================
```

### 3. 测试基本功能

运行示例脚本：
```bash
python examples/basic_usage.py
```

## 🔧 Unsplash 配置（可选）

如果您想使用 Unsplash 配图功能：

### 1. 获取 API 密钥

1. 访问 [Unsplash Developers](https://unsplash.com/developers)
2. 注册开发者账户
3. 创建新应用
4. 获取 **Access Key**

### 2. 配置 API 密钥

在 `.env` 文件中设置：
```env
UNSPLASH_KEY=your_actual_access_key_here
```

或者设置环境变量：
```bash
export UNSPLASH_KEY="your_actual_access_key_here"
```

### 3. 测试 Unsplash 功能

```bash
python examples/unsplash_demo.py
```

## 🐛 常见问题

### 权限被拒绝

**问题**: 运行时出现权限错误
**解决方案**: 
1. 检查辅助功能权限设置
2. 重启终端应用
3. 确保 Python 在权限列表中

### Keynote 无法启动

**问题**: AppleScript 无法控制 Keynote
**解决方案**:
1. 手动启动 Keynote 一次
2. 确保 Keynote 不是从 App Store 安装的受限版本
3. 检查自动化权限设置

### 导入错误

**问题**: 运行时出现模块导入错误
**解决方案**:
1. 确保虚拟环境已激活
2. 重新安装依赖：`pip install -r requirements.txt`
3. 检查 Python 路径设置

### Unsplash API 错误

**问题**: Unsplash 功能无法使用
**解决方案**:
1. 检查 API 密钥是否正确设置
2. 验证网络连接
3. 检查 API 配额限制

## 📞 获取帮助

如果您遇到安装问题：

1. 查看 [常见问题](troubleshooting/faq.md)
2. 搜索 [GitHub Issues](https://github.com/easychen/keynote-mcp/issues)
3. 创建新的 [Issue](https://github.com/easychen/keynote-mcp/issues/new)

## 🎉 下一步

安装完成后，您可以：

- 阅读 [快速入门指南](quickstart.md)
- 查看 [基本用法](user-guide/basic-usage.md)
- 运行 [示例代码](examples/basic-examples.md)

---

*安装过程中遇到问题？欢迎在 GitHub 上提交 Issue！* 