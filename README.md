# 科研配图转可编辑 SVG

一个 Codex 技能：将科研配图、论文示意图或已有 SVG 转换或微调为分层、文字可编辑的 SVG，方便后续导入 Figma。

## 默认行为

- 使用 **Noto Sans · Display SemiCondensed SemiBold**，保留 Display、半窄体和实际 600 字重。
- 优先保留原图布局、文字、配色和素材；局部调整遵循用户指定范围。
- 保留真实 `<text>` / `<tspan>` 文本节点；连贯多行文字属于一个 `<text>`，按模块分组。
- 交付 SVG 和 PNG 预览，保留源文件。
- 检查字体声明、分组、内部引用和位图使用，并通过实际渲染核验排版。

**可编辑性边界：** SVG 含有真实文本节点，不代表 Figma 导入后一定保留原生文字。技能会明确区分 SVG 结构验证与 Figma 原生 `TEXT` 节点验证，不把未经验证的导入状态当成已确认结果。

## 安装到 Codex

将本仓库放入个人技能目录：

```bash
git clone https://github.com/Cream-yj/research-figure-to-svg.git "$HOME/.codex/skills/research-figure-to-svg"
```

已安装该技能时，请先检查现有目录，避免覆盖本地修改。

## 使用

在 Codex 中调用，并附上图片或 SVG：

```text
$research-figure-to-svg 把这张科研图转成可编辑 SVG，保留原排版。
```

也可以指定单栏尺寸、比例或局部修改范围。默认 family 为 Noto Sans、style 为 Display SemiCondensed SemiBold；用户的明确要求优先。技能会核对实际字体元数据和渲染结果。

从 Figma 导出修改稿时，选择整张图的最外层 Frame，勾选 `Include "id" attribute`，取消勾选 `Outline text`。这些设置保留对象 ID 和真实文字，不会自动把已拆开的多个文本框合并。

## SVG 结构检查

检查脚本只依赖 Python 3 标准库：

```bash
python3 scripts/validate_svg.py "/path/to/figure.svg"
```

用户明确指定其他字体时，可以覆盖允许的字体声明：

```bash
python3 scripts/validate_svg.py "/path/to/figure.svg" --font-family "指定字体"
```

脚本输出 JSON，失败时返回非零退出码；同时报告包含多个 `<tspan>` 的文本对象数及声明的字重、字宽、可变轴。默认字体名单包含指定静态字形及 Display 家族；用户明确要求普通 Noto Sans 时，可用 `--font-family "Noto Sans"`。

结构检查不能自动推断段落边界，也不验证实际字体加载、视觉边界、科研内容完整性或 Figma 导入状态，这些需要单独检查。

## 文件

- [SKILL.md](SKILL.md)：技能说明、工作流程和示例。
- [agents/openai.yaml](agents/openai.yaml)：Codex 技能界面信息。
- [scripts/validate_svg.py](scripts/validate_svg.py)：只读 SVG 结构检查脚本。

仓库不包含用户科研图片或字体文件；Noto Sans 的获取和使用方式见技能说明。
