# 科研配图转可编辑 SVG

**research-figure-to-svg** 是一个 Codex 技能，用于将科研配图、论文示意图或已有 SVG 转换、修复或微调为分层且文字可编辑的 SVG，方便继续在 Figma 中编辑。

它优先保留原图的布局、研究内容、配色和素材。默认使用 **Noto Sans · Display SemiCondensed SemiBold**，并把连贯的多行文字保留在一个文本对象中。

本仓库包含给 Codex 使用的工作流程和一个只读 SVG 检查脚本。图片重建由 Codex 结合输入素材和可用工具完成；检查脚本本身不执行图片转 SVG。

## 适用场景

| 输入或需求 | 处理方式 |
| --- | --- |
| 已有 SVG，只换字体、改宽度或微调间距 | 复用原有图形、分组和素材，修改对应文字与必要几何属性 |
| 科研示意图截图或 PNG/JPEG | 重建文字、卡片、箭头和模块分组；复杂插画优先复用原始素材 |
| 连贯的两行文字被拆成两个文本框 | 核对原文后合并为一个 `<text>`，内部使用 `<tspan>` 换行 |
| 彩色关键词与句子被拆开，间距错乱 | 合并为一个文本对象，使用行内 `<tspan>` 保留颜色和强调 |
| 作者在 Figma 中改过一部分，需要继续修改 | 以作者最新导出的 SVG 为基础，保留已完成的调整 |
| 论文单栏适配或指定比例 | 按实际栏宽计算尺寸和字号，在授权范围内调整布局 |
| 有数据或绘图源码的图表 | 优先重新导出，不依据截图虚构数值、曲线或误差条 |

普通图片润色不使用此技能。复杂插画允许保留为局部位图，但交付时应说明；把整张截图嵌入 SVG 不构成文字可编辑的重建。

## 安装与更新

需要能使用本地技能的 Codex 环境。检查脚本只依赖 **Python 3 标准库**；预览还需要可用的 SVG 渲染工具和实际字体文件，字体核验或绘图所需工具按任务选择。

### 首次安装

默认安装到个人技能目录；已设置 `CODEX_HOME` 时使用对应目录：

```bash
mkdir -p "${CODEX_HOME:-$HOME/.codex}/skills"
git clone https://github.com/Cream-yj/research-figure-to-svg.git \
  "${CODEX_HOME:-$HOME/.codex}/skills/research-figure-to-svg"
```

如果目标目录已存在，先检查内容，避免覆盖本地修改。安装后在 Codex 中使用 `$research-figure-to-svg`；如果当前会话尚未列出新技能，重新打开会话并检查技能是否可见。

### 更新 Git 克隆安装的版本

```bash
git -C "${CODEX_HOME:-$HOME/.codex}/skills/research-figure-to-svg" status --short
git -C "${CODEX_HOME:-$HOME/.codex}/skills/research-figure-to-svg" pull --ff-only
```

有本地修改或无法快进时，先比较并保留修改，不强制覆盖。通过复制文件安装、目录中没有 `.git` 的版本，需要另行获取最新仓库并比较后更新。

## 使用示例

在 Codex 中调用技能，并附上图片或 SVG，也可以提供本机可读取的文件路径。说明修改范围、需要保留的内容，以及有无尺寸约束。

### 保留原排版重建

```text
$research-figure-to-svg
把这张科研示意图转成分层、文字可编辑的 SVG，保留原排版、配色和文字内容。
字体用 Noto Sans 的 Display SemiCondensed SemiBold。
我自己导入 Figma，请交付本地 SVG 和 PNG 预览。
```

### 继续修改作者的新版

```text
$research-figure-to-svg
这是我修改了一部分的最新版 SVG。保留我已改的布局、人物、配色和文案，
把连贯的多行文字合并为一个文本对象，修正彩色词组间距，统一指定字形。
请另存新版，不覆盖原文件。
```

### 只调整字体和宽度

```text
$research-figure-to-svg
这个 SVG 的原排版已经合适，只调整宽度、字体和必要的间距。
不要重新设计，也不要拉伸人物或字形。
```

### 适配论文单栏

```text
$research-figure-to-svg
把这张图适配到论文单栏，栏宽按我的模板确定。
画布高:宽 = 5:4，允许精简重复说明，但保留关键研究内容。
请检查最终栏宽下的可读性，并给出 SVG 和预览。
```

`高:宽 = 5:4` 是竖版，`宽:高 = 5:4` 是横版。技能默认沿用原图比例；5:4 和任何会议的栏宽都不是所有任务的固定默认值。放入宽度为 W 的版面时，图高为 `W × 画布高 / 画布宽`，占用空间还取决于内容和字号。

## 字体与字形

默认要求包含完整字形，而非仅有字体家族名：

| 项目 | 默认值 |
| --- | --- |
| Figma typographic family | `Noto Sans` |
| Figma typographic style | `Display SemiCondensed SemiBold` |
| 实际字重 | 600 |
| 半窄字宽 | SemiCondensed；可变字体对应 `wdth=87.5` |
| 已核验静态字体的 legacy family | `Noto Sans Display SemiCondensed SemiBold` |
| 已核验静态字体的 PostScript 名称 | `NotoSans-DisplaySemiCondensedSemiBold` |

指定了这一字形时，通过字号、间距和颜色区分信息层级。用户明确允许其他字重或指定其他字体时，按用户要求处理。

静态字体的 legacy subfamily 可能显示为 `Regular`，但实际字重仍是 600。可变字体需要同时核对 Display 设计版本、`wght=600` 和 `wdth=87.5`，并确认渲染器应用了这些轴。不要用水平拉伸文字模拟半窄体，也不要把完整 Figma style 字符串填入 CSS `font-style`。

原图已有斜体强调时，可以保留对应的 **Display SemiCondensed SemiBold Italic**。已核验官方斜体文件的 legacy family 为 `Noto Sans SemiCondensed SemiBold`，名称中没有 Display；实际字形应根据字体元数据确认。不要任意拼接字体名称。

字体优先使用用户提供或本机已有文件。缺失时获取到任务目录，技能不擅自安装系统字体。中英文混排时，中文可使用经过字形核验的 Noto Sans SC / Noto Sans CJK SC。

可参考 [Noto 官方静态字形](https://github.com/notofonts/noto-fonts/blob/main/hinted/ttf/NotoSansDisplay/NotoSansDisplay-SemiCondensedSemiBold.ttf)、[对应斜体](https://github.com/notofonts/noto-fonts/blob/main/hinted/ttf/NotoSansDisplay/NotoSansDisplay-SemiCondensedSemiBoldItalic.ttf) 和 [Google Fonts 的 Noto Sans Display](https://github.com/google/fonts/tree/main/ofl/notosansdisplay)。版本不同，命名和外观可能不同，应核对实际使用的文件。

## 多行文字与行内样式

**一个完整句子、标签或段落，对应一个文本对象。** 换行改变显示位置，不改变对象的语义边界。

```xml
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 100">
  <text id="memory-description" font-family="Noto Sans Display SemiCondensed SemiBold" font-weight="600" font-stretch="semi-condensed" font-size="18" xml:space="preserve"><tspan x="20" y="35">Agent retrieves memory </tspan><tspan x="20" y="60">to answer the user.</tspan></text>
</svg>
```

这里是一个 `<text>` 和两个 `<tspan>`。末尾空格保留了英文词边界；行内不同颜色、下划线等也可以放在同一个 `<text>` 的 `<tspan>` 中。

- 不把每一行分别生成一个 `<text>`。
- 不把多个独立文本框放进同一个 `<g>` 就当成一个文本对象。
- 不按距离自动合并独立标题、不同列表项或不同卡片的文字。
- 需要 Figma 原生文字时，一个逻辑文本块对应一个 `TEXT` 节点，`characters` 使用真正的换行符 `\n`，混合样式按字符范围设置。

**SVG 的一个 `<text>` 不保证 Figma 直接导入后仍是一个原生文字层。** 直接导入的结果需要在目标文件中检查；如果仍被拆行，需要使用可用的原生文字恢复流程。

## 从 Figma 导出修改稿

建议选择整张图的最外层 Frame，使用 SVG 格式导出，再把最新版交给 Codex 修改。

| 导出设置 | 建议与作用 |
| --- | --- |
| `Include "id" attribute` | 勾选，保留基于对象名称的 ID |
| `Outline text` | 取消勾选，避免文字变成轮廓 |
| `Include bounding box` | 控制单独文字的导出边界，按实际需要选择 |
| `Ignore overlapping layers` | 控制是否包含交叠的其他对象，按实际导出范围选择 |

这些设置不负责合并已拆开的文本框，也不保证完整保留 Figma 原生图层层级。导出后检查画布、文字和素材是否完整。设置含义见 [Figma 官方导出说明](https://help.figma.com/hc/en-us/articles/13402894554519-Export-formats-and-settings-for-static-designs)。

自行导入本地 SVG 的工作流不要求 Figma MCP。只有任务需要在 Figma 中创建、恢复或检查原生节点时，才使用对应工具；工具额度耗尽时，交付本地文件并说明尚未验证的导入状态。

## 交付与验证范围

通常交付：

- 新版 SVG：保留真实 `<text>` / `<tspan>`，按语义模块分组。
- PNG 预览：用于检查字形、排版、边界和科研内容。
- 简短说明：尺寸与比例、实际字体、修改范围、局部位图或其他限制，以及完成了哪些验证。

默认另存文件。继续修改时以作者最新 SVG 为基础，不用旧稿覆盖作者的新调整。

| 验证层次 | 能说明什么 | 需要额外核对什么 |
| --- | --- | --- |
| SVG 结构检查 | XML、引用、ID、文本元素、字体声明与元素统计 | 字体实际加载、合理分组和内容完整性 |
| 实际字体渲染与视觉检查 | 目标字形下的间距、换行、遮挡和边界 | 其他软件是否解析到同一字体 |
| 目标 Figma 文件检查 | 实际导入后的原生节点、字体和多行对象 | 未检查的文件或其他导入方式 |

字体声明或 `fc-match` 匹配成功，不代表实际渲染器已经使用该字体。应对照目标字体文件的字形、宽度或笔画，排除静默替代。必要时可以在仅供预览的副本中用真实字体塑形并渲染字形路径；正式 SVG 仍保留真实文字，轮廓预览不能代替可编辑交付，也不能证明 Figma 导入已通过。

复杂公式、缺失字符、无法辨认的原文或会改变研究含义的取舍，应先核对。没有数据时不虚构图表数值。保留局部位图时，不声称整个图都可作为矢量形状编辑。

## SVG 检查脚本

在仓库目录运行：

```bash
python3 scripts/validate_svg.py "/path/to/figure.svg"
```

也可以在任意目录使用安装路径：

```bash
python3 "${CODEX_HOME:-$HOME/.codex}/skills/research-figure-to-svg/scripts/validate_svg.py" \
  "/path/to/figure.svg"
```

脚本只读文件，输出 JSON；成功返回退出码 0，结构错误返回退出码 1。它检查：

- SVG 根元素，以及有效的 `viewBox`。
- 重复 ID、缺失内部引用和非自包含的资源引用。
- 是否存在 `<text>`，以及可解析的行内或继承字体声明是否在允许名单中。

同时统计文本、`<tspan>`、分组、路径、位图，以及声明的字重、字宽和可变轴。存在位图、CSS 样式表或无法解析的字体声明等情况会给出警告；完整样式表不由此脚本解析。

主要输出字段：

| 字段 | 含义 |
| --- | --- |
| `structural_checks_passed` | 结构检查是否通过 |
| `text_elements` / `text_spans` | `<text>` / `<tspan>` 数量 |
| `text_elements_with_multiple_tspans` | 含多个 `<tspan>` 的文本对象数，不等于已确认的多行段落数 |
| `groups` / `paths` / `images` | 分组、路径和位图元素数量 |
| `declared_font_segments` | 声明的主字体及文本片段计数 |
| `declared_weight_segments` | 声明的字重；不等于字体文件的真实字重 |
| `declared_stretch_segments` / `declared_variation_segments` | 声明的字宽与可变轴 |
| `errors` / `warnings` | 错误和需要进一步检查的事项 |

默认名单包含指定静态字形、Display 家族、已核验斜体的 legacy family，以及中文 Noto 字体。普通 `Noto Sans` 声明不能单独证明 Display 半窄 SemiBold 匹配，默认不会以它通过字体名单检查。

用户明确指定其他字体时，可覆盖允许名单；重复参数指定多个字体：

```bash
python3 scripts/validate_svg.py "/path/to/figure.svg" \
  --font-family "Noto Sans" \
  --font-family "Noto Sans SC"
```

`--font-family` **替换**默认名单，不是在默认名单后追加。允许名单通过不证明实际字形匹配，仍需核对字体文件和渲染结果。脚本不推断段落边界，不检查文字内容、重叠或 Figma 原生节点。

## 常见问题

**为什么导入 Figma 后还是不能编辑文字，或者两行被拆开？** 先检查 SVG 是否包含真实 `<text>`，再检查 Figma 中实际生成的节点。导入行为不能由 SVG 元素计数证明；恢复原生文字时，应按一个逻辑文本块创建一个含换行的 `TEXT` 节点。

**为什么声明了 Noto Sans，预览仍然不一样？** 可能只匹配了家族名，遗漏了 Display、字宽或字重，也可能渲染器使用了替代字体。确认实际字体文件、元数据和渲染结果；不要只凭 `font-family` 字符串判断。

**图片中的人物也都会变成可编辑矢量吗？** 不一定。原始矢量素材可以复用；局部位图会保留并说明。文字和框线的可编辑性与人物是否为矢量应分别判断。

**检查脚本通过，能当作论文图片检查完成吗？** 不能。还需要核对科研内容、目标栏宽下的可读性、真实字体、遮挡和剪裁，以及需要时的 Figma 导入结果。

## 仓库结构

```text
research-figure-to-svg/
├── README.md                 使用、安装与验证说明
├── SKILL.md                  给 Codex 使用的技能流程
├── agents/openai.yaml        技能界面信息和默认调用示例
└── scripts/validate_svg.py   只读 SVG 结构检查脚本
```

技能的完整执行规则见 [SKILL.md](SKILL.md)，检查逻辑见 [validate_svg.py](scripts/validate_svg.py)。仓库不包含用户科研图片、原始研究数据或字体文件。
