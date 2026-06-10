# 🧩 拼豆小窝 - Piggy's Perler Beads Gallery

个人拼豆作品展示网站 — 可爱像素风格，像朋友圈一样分享你的拼豆作品！

## 🌟 功能

- **朋友圈风格布局**：时间线展示，按日期倒序排列
- **侧边栏筛选**：按年/月筛选作品
- **多图展示**：每条动态支持多张图片，自动网格布局
- **5种可爱主题**：樱花粉、薄荷绿、天空蓝、薰衣草紫、蜜桃橙
- **背景音乐**：醒目的浮动音乐按钮，支持播放列表
- **个人介绍**：侧边栏展示头像、姓名、简介，管理模式下可编辑修改
- **后台管理**：点击标题5次进入管理模式，像发朋友圈一样编辑发布
- **拖拽传图**：编辑时直接拖拽图片到编辑区，自动压缩存储
- **自动保存**：所有编辑内容自动保存到浏览器本地存储
- **一键导出**：导出 posts.json 文件（含个人资料 + 关于信息 + 图片数据），方便上传更新

## 📁 文件结构

```
Pindou_Web/
├── index.html      # 主页面（包含所有功能）
├── posts.json      # 作品数据 + 网站配置（_meta 字段含关于信息）
├── images/         # 图片文件夹（传统方式，拖拽模式不需要）
├── music/          # 音乐文件夹（放背景音乐 .mp3 文件）
└── README.md
```

## 🚀 部署到 GitHub Pages

### 1. 创建 GitHub 仓库

在 GitHub 上创建一个新仓库，例如 `pindou-gallery`。

### 2. 推送代码

```bash
cd "e:/PIGGY文件/University/2026.6/Pindou_Web"

# 初始化 git
git init
git add .
git commit -m "🎉 初始化拼豆小窝网站"

# 关联远程仓库（替换为你的仓库地址）
git remote add origin git@github.com:Fried-Piggy/pindou-gallery.git

# 推送
git branch -M main
git push -u origin main
```

### 3. 开启 GitHub Pages

1. 进入仓库 → Settings → Pages
2. Source 选择 `Deploy from a branch`
3. Branch 选择 `main`，文件夹选 `/ (root)`
4. 点击 Save
5. 等待几分钟，网站会在 `https://Fried-Piggy.github.io/pindou-gallery/` 上线

## ✏️ 如何发布新作品

### 方法一：在线编辑（推荐）

1. 打开你的网站
2. **点击标题 "拼豆小窝" 5次**，进入管理模式
3. 点击左下角 ✏️ 按钮发布新动态
4. 填写标题、日期、描述、标签
5. **拖拽图片**到编辑区的虚线框中（支持多张，自动压缩）
6. 保存后，点击 📦 导出 posts.json
7. 将新的 posts.json push 到 GitHub：

```bash
git add posts.json
git commit -m "✨ 新增作品：XXX"
git push
```

> 💡 图片数据直接嵌入在 posts.json 中，无需单独上传图片文件！

### 方法二：直接编辑 JSON

`posts.json` 文件格式如下（图片可以是文件名引用，也可以是 data URL）：

```json
{
  "_meta": {
    "aboutText": "🧩 这里记录了我的拼豆作品们～\n每一颗豆豆都是用心拼出来的小可爱！",
    "exportedAt": "2026-06-10T00:00:00.000Z"
  },
  "posts": [
    {
      "id": "post_001",
      "title": "作品标题",
      "date": "2026-06-10",
      "description": "作品描述（可选）",
      "images": ["image1.jpg", "image2.jpg"],
      "tags": ["标签1", "标签2"]
    }
  ]
}
```

> 💡 `_meta.aboutText` 就是侧边栏"关于"的内容，导出时会自动包含，修改后记得也更新这里。

## 🎵 添加背景音乐

将 `.mp3` 文件放入 `music/` 文件夹，然后在管理模式下编辑音乐播放列表（可后续自定义）。

## 💡 提示

- **本地开发**：用 `python server.py` 启动（不是 `python -m http.server`），支持图片自动上传到 `images/` 文件夹
- 导出文件会下载到**系统"下载"文件夹**，请手动复制到项目目录再 git push
- 图片拖入编辑器后，保存时自动存入 `images/` 文件夹，JSON 只记录文件名
- 编辑内容会自动保存在浏览器中，不会丢失
- 按 `Ctrl+S` 手动触发保存
- 按 `Esc` 关闭弹窗
