# Lean 形式化数学

这是 *Mathematics in Lean* 的中文版本。本教程依赖 Lean 4、VS Code 与 Mathlib，旨在帮助读者一边阅读教材，一边在本仓库的 Lean 文件中运行示例并完成练习。

你可以阅读本仓库中的 `html` 版本，也可以阅读根目录下的 `mathematics_in_lean.pdf`。教材配套的 Lean 文件位于 `MIL` 目录，并按章节组织。

本版本面向 [Lean 4](https://leanprover.github.io/) 与 [Mathlib](https://github.com/leanprover-community/mathlib4)。Lean 3 版本见 [mathematics_in_lean3](https://github.com/leanprover-community/mathematics_in_lean3)。

## 在本地使用

1. 按照 [Lean 安装说明](https://lean-lang.org/install/) 安装 Lean 4 与 VS Code。

2. 在 VS Code 右上角点击 forall 符号，依次选择 `Open Project`、`Download Project` 和 `Mathematics in Lean` 获取项目。

3. 教材的每一节都有对应的 Lean 文件，其中包含示例和练习。建议复制 `MIL` 目录，在副本中实验和完成练习。这样可以保留原文件不变，也便于以后更新仓库。副本可以命名为 `my_files`，也可以使用你喜欢的其他名称。

随后可以在浏览器中打开 `html/index.html` 阅读中文教材，并在 VS Code 中完成练习。

本教材和仓库仍在持续完善。若要更新仓库，可在 `mathematics_in_lean` 目录中运行：

```bash
git pull
lake exe cache get
```

这假定你没有直接修改 `MIL` 目录中的原文件，因此上面建议先复制一份再练习。

## 使用 GitHub Codespaces

如果本地安装 Lean 遇到困难，可以通过 GitHub Codespaces 直接在浏览器中使用 Lean。这需要一个 GitHub 账号。登录后可以点击：

<a href='https://codespaces.new/leanprover-community/mathematics_in_lean' target="_blank" rel="noreferrer noopener"><img src='https://github.com/codespaces/badge.svg' alt='Open in GitHub Codespaces' style='max-width: 100%;'></a>

请将机器类型设为 `4-core`，然后点击 `Create codespace`。创建过程可能需要几分钟；系统会在云端创建虚拟机，并安装 Lean 与 Mathlib。

打开 `MIL` 目录中的任意 `.lean` 文件会启动 Lean，不过这也可能需要一点时间。仍然建议按本地使用说明复制 `MIL` 目录，在副本中练习。若要更新仓库，可在浏览器中的终端运行 `git pull`，然后运行 `lake exe cache get`。

Codespaces 每月提供一定数量的免费时长。完成工作后，按 `Ctrl/Cmd+Shift+P`，输入 `stop current codespace`，并选择 `Codespaces: Stop Current Codespace` 停止当前工作区。若忘记停止，虚拟机会在一段空闲时间后自动停止。

要重新打开已有工作区，请访问 <https://github.com/codespaces>。

## GitHub Pages

本仓库包含 GitHub Actions 工作流。推送到 `master` 后，工作流会运行 Lean 构建，整理中文静态文档，并把 `html` 目录部署到 `gh-pages` 分支。若根目录存在 `mathematics_in_lean.pdf`，工作流也会把它复制到部署产物中。

## 贡献

原英文项目的问题和 PR 请提交到上游 [source repository](https://github.com/avigad/mathematics_in_lean_source)。中文版本的修正可直接在本仓库提交。
