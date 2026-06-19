# Lean 形式化数学

这是 *Mathematics in Lean* 的中文版本。本教程基于 Lean 4、VS Code 和 Mathlib，目标是帮助读者在 Lean 中形式化现代数学。

你可以在本仓库的 `html` 目录中阅读已生成的中文网页，也可以打开根目录下的 `mathematics_in_lean.pdf` 阅读 PDF 版本。Lean 练习文件位于 `MIL` 目录，并按章节组织。

本版本基于 [Mathematics in Lean](https://leanprover-community.github.io/mathematics_in_lean/) 与 [Lean-zh/math-in-lean-zh](https://github.com/Lean-zh/math-in-lean-zh) 的中文翻译工作整理。Lean 3 版本见 <https://github.com/leanprover-community/mathematics_in_lean3>。

## 在本地使用

1. 按照 [Lean 安装说明](https://lean-lang.org/install/) 安装 Lean 4 和 VS Code。

2. 在 VS Code 右上角点击 forall 符号，选择 `Open Project`、`Download Project`，再选择 `Mathematics in Lean`。

3. 教材的每一节都有对应的 Lean 文件，包含例题和练习。建议复制 `MIL` 目录，在副本中实验和完成练习。这样可以保留原文件，也便于之后更新仓库。

之后，你可以在浏览器中打开 `html/index.html` 阅读中文教材，并在 VS Code 中完成练习。

如果要更新依赖缓存，请在仓库根目录运行：

```bash
lake exe cache get
```

然后可用如下命令检查 Lean 文件是否能通过构建：

```bash
lake build
```

## 使用 GitHub Codespaces

如果本地安装 Lean 不方便，可以使用 GitHub Codespaces。登录 GitHub 后点击：

<a href='https://codespaces.new/leanprover-community/mathematics_in_lean' target="_blank" rel="noreferrer noopener"><img src='https://github.com/codespaces/badge.svg' alt='Open in GitHub Codespaces' style='max-width: 100%;'></a>

请将机器类型设为 `4-core`，然后点击 `Create codespace`。打开 `MIL` 目录中的任意 `.lean` 文件即可启动 Lean。建议仍然复制 `MIL` 目录，在副本中练习。

## GitHub Pages

本仓库包含 GitHub Actions 工作流。推送到 `master` 后，工作流会先运行 `lake build`，再将 `html` 目录部署到 `gh-pages` 分支，供 GitHub Pages 使用。若根目录存在 `mathematics_in_lean.pdf`，工作流也会把它复制到部署产物中。

## 贡献

原英文项目的问题和 PR 请提交到上游 [source repository](https://github.com/avigad/mathematics_in_lean_source)。中文翻译相关修正可直接在本仓库提交。
