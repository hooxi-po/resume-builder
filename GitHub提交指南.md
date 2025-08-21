# GitHub 代码提交指南

本指南将帮助您快速设置Git并将代码提交到GitHub。

## 📋 准备工作

### 1. 创建GitHub账号
- 访问 [GitHub官网](https://github.com) 注册账号
- 验证邮箱地址

### 2. 创建GitHub仓库
1. 登录GitHub后点击右上角的 `+` 号
2. 选择 `New repository`
3. 填写仓库名称（建议使用英文）
4. 选择 `Public`（公开）或 `Private`（私有）
5. 点击 `Create repository`
6. **复制仓库地址**（形如：`https://github.com/用户名/仓库名.git`）

## 🚀 快速开始

### 步骤1：安装和配置Git

1. **双击运行** `install_git.bat`
2. 按照提示下载并安装Git：
   - 官方地址：https://gitforwindows.org/
   - 国内镜像：https://registry.npmmirror.com/-/binary/git-for-windows/v2.47.1.windows.1/Git-2.47.1-64-bit.exe
3. 安装完成后重新运行 `install_git.bat`
4. 输入您的GitHub用户名和邮箱

### 步骤2：提交代码到GitHub

1. **双击运行** `quick_commit.bat`
2. 首次运行时输入GitHub仓库地址
3. 输入提交信息（描述本次更改）
4. 等待脚本自动完成提交

## 🔧 详细说明

### install_git.bat 功能
- ✅ 检查Git安装状态
- ✅ 配置Git用户信息
- ✅ 初始化Git仓库
- ✅ 创建.gitignore文件

### quick_commit.bat 功能
- ✅ 检查Git和仓库状态
- ✅ 添加远程仓库（首次使用）
- ✅ 自动添加所有文件
- ✅ 提交到本地仓库
- ✅ 推送到GitHub

## 🔐 认证设置

### 方法1：使用Personal Access Token（推荐）

1. 访问GitHub设置：https://github.com/settings/tokens
2. 点击 `Generate new token` → `Generate new token (classic)`
3. 设置Token名称和权限：
   - 勾选 `repo`（完整仓库访问权限）
   - 设置过期时间
4. 复制生成的Token（只显示一次！）
5. 首次推送时，用户名输入GitHub用户名，密码输入Token

### 方法2：使用SSH密钥

```bash
# 生成SSH密钥
ssh-keygen -t rsa -b 4096 -C "your_email@example.com"

# 复制公钥内容
cat ~/.ssh/id_rsa.pub
```

然后在GitHub设置中添加SSH密钥：https://github.com/settings/keys

## 📝 常用Git命令

```bash
# 查看状态
git status

# 查看提交历史
git log --oneline

# 查看远程仓库
git remote -v

# 拉取最新代码
git pull

# 查看分支
git branch
```

## ❗ 常见问题

### 1. 推送失败：认证错误
**解决方案**：配置Personal Access Token或SSH密钥

### 2. 推送失败：分支不存在
**解决方案**：脚本会自动尝试main和master分支

### 3. 网络连接问题
**解决方案**：
- 检查网络连接
- 尝试使用VPN
- 使用SSH方式（如果HTTPS不稳定）

### 4. 文件过大
**解决方案**：
- Git有100MB单文件限制
- 使用Git LFS处理大文件
- 将大文件添加到.gitignore

## 🎯 最佳实践

1. **定期提交**：建议每完成一个功能就提交一次
2. **清晰的提交信息**：描述本次更改的内容
3. **使用.gitignore**：忽略不需要版本控制的文件
4. **备份重要代码**：GitHub可以作为代码备份

## 📞 获取帮助

- [Git官方文档](https://git-scm.com/doc)
- [GitHub帮助文档](https://docs.github.com/)
- [Git教程](https://www.liaoxuefeng.com/wiki/896043488029600)

---

🎉 **恭喜！现在您可以轻松地将代码提交到GitHub了！**