# 科研配图转可编辑 SVG

一个 Codex 技能：将科研配图、论文示意图或已有 SVG 转换或微调为分层、文字可编辑的 SVG，方便后续导入 Figma。

## 默认行为

- 使用 **Noto Sans**，按信息层级选择字重。
- 优先保留原图布局、文字、配色和素材；局部调整遵循用户指定范围。
- 保留真实 `<text>` / `<tspan>` 文本节点，按模块分组。
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

也可以指定单栏尺寸、比例或局部修改范围。默认字体为 Noto Sans，字重由执行时判断；用户的明确要求优先。

## SVG 结构检查

检查脚本只依赖 Python 3 标准库：

```bash
python3 scripts/validate_svg.py "/path/to/figure.svg"
```

用户明确指定其他字体时，可以覆盖允许的字体声明：

```bash
python3 scripts/validate_svg.py "/path/to/figure.svg" --font-family "指定字体"
```

脚本输出 JSON，失败时返回非零退出码。结构检查不验证实际字体加载、视觉边界、科研内容完整性或 Figma 导入状态，这些需要单独检查。

## 文件

- [SKILL.md](SKILL.md)：技能说明、工作流程和示例。
- [agents/openai.yaml](agents/openai.yaml)：Codex 技能界面信息。
- [scripts/validate_svg.py](scripts/validate_svg.py)：只读 SVG 结构检查脚本。

仓库不包含用户科研图片或字体文件；Noto Sans 的获取和使用方式见技能说明。
