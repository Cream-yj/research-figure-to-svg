---
name: research-figure-to-svg
description: 将科研配图、论文示意图或已有 SVG 转换或微调为分层、文字可编辑的 SVG，供用户导入 Figma。连贯多行文字保留为一个文本对象，默认使用 Noto Sans 的 Display SemiCondensed SemiBold 字形。适用于图片转可编辑图、保留原排版重建、单栏适配及字体调整；普通图片润色不使用本技能。
---

# 科研配图转可编辑 SVG

把用户提供的科研图片或 SVG 做成可继续编辑的文件。默认忠实保留原图的布局、内容、配色和素材；用户只要求改宽度、字体或局部元素时，只做对应调整。默认交付本地 SVG 和 PNG 预览，保留源文件。

## 先明确可编辑性的边界

- **SVG 文件可编辑**：标签使用真实的 `<text>` / `<tspan>`；卡片、线条、箭头等使用独立矢量元素和语义分组。把整张图片嵌入 `<image>` 或把文字描成 `<path>`，不满足此目标。
- **Figma 原生文字可编辑**：还需在目标 Figma 文件中确认标签是 `TEXT` 节点。仅检查 SVG 含有 `<text>`，不能保证直接导入后仍是原生文字；Figma 的矢量导入行为可能转换文字。
- 用户只要本地 SVG、自行导入时，直接制作文件。需要检查 Figma 导入结果时，优先使用 Figma MCP；MCP 额度耗尽或不可用时改用 Computer Use，在目标文件中核对实际文字属性。检查或测试副本按已授权范围操作，技能本身不代表上传用户文件的授权；无法完成实际检查时说明验证范围，不能把 SVG 检查通过说成 Figma 验证通过。

## 原图检查与范围判断

先看原图及参考图。已有 SVG 同时检查 `viewBox`、尺寸、分组、文本节点、字体、位图和内部引用，并渲染预览，不能只看 XML 就判断版式正常。

- **已有 SVG**：优先复用其形状、人物、渐变和分组，修改真实文本和必要几何属性。彩色词组分成多个文字元素导致间距错误时，可合并为一行 `<text>`，以 `<tspan>` 保留颜色、强调和空格。
- **截图或位图**：辨认文字及各模块，重建可编辑的框、箭头、标签和分组。人物插画等复杂素材优先复用用户提供的矢量素材；必要的位图局部必须说明，不能把整张截图作为底板后覆盖文字。
- **数据图表**：有数据或绘图源码时优先从它们重新导出。没有数据时不要虚构数值、曲线或误差条；只能按可靠可见内容重建，并标明哪些信息未核验。
- 对看不清的文字、公式、数值或会改变研究含义的取舍先核对。已经确认过的布局、方向和改动范围不重复询问。

“保留原排版”“只换字体”“只改宽度”不能解释成重新设计。参考图与原图有不同研究内容时，按用户指定的内容来源处理，不能自行替换结论。

## 连贯多行文字：一个文本对象

按内容识别文本块，而不是按屏幕上的行数拆对象。一个完整句子、标签或段落，即使显示两行或多行，也保留为一个 `<text>`，内部用 `<tspan>` 设置换行位置。不能每行生成一个 `<text>`，也不能只把几个独立文本框放进同一个 `<g>` 就称为一个文本对象。

- 合并已拆开的行时，核对完整原文、行序、词间空格、行距和对齐；保留行内颜色、粗细等差异。不要靠相邻距离自动合并独立标题、列表项或不同卡片中的文字。
- 需要 Figma 原生文字时，一个逻辑文本块对应一个 `TEXT` 节点，`characters` 中使用真正的 `\n`；需要混合样式时设置字符范围样式。SVG 转 Figma 的转换器也应以父 `<text>` 为单位收集各行，不能逐个 `<tspan>` 或逐行创建文本层。
- 单个 `<text>` 是 SVG 的结构要求，不能保证 Figma 直接导入后的节点数量。若目标软件仍拆行，检查实际导入结果，并使用可用的原生文字恢复流程；交付时说明验证范围。

例如下方两行属于同一条服药信息；末尾空格保留了原句的词边界，两个 `<tspan>` 仍归属于同一个 `<text>`：

```xml
<text id="medication-label" font-family="NotoSans-DisplaySemiCondensedSemiBold" font-weight="600" font-stretch="semi-condensed" font-size="16" xml:space="preserve"><tspan x="20" y="40">Warfarin 5 mg </tspan><tspan x="20" y="60">every morning</tspan></text>
```

## 默认字体：Noto Sans / Display SemiCondensed SemiBold

除非用户另有明确要求，标题、正文和标签使用 **Noto Sans**，字形使用 **Display SemiCondensed SemiBold**。这是完整字形要求，包含 Display、半窄体和实际 600 字重；不能仅声明普通 `Noto Sans` 再加粗来代替。用户指定了此字形时，保留该字形，通过字号、间距或颜色区分信息层级；只有用户允许其他字重时才调整。

该静态字体的官方元数据是：typographic family `Noto Sans`，typographic style `Display SemiCondensed SemiBold`，legacy family `Noto Sans Display SemiCondensed SemiBold`，PostScript 名称 `NotoSans-DisplaySemiCondensedSemiBold`。legacy subfamily 标作 `Regular`，但实际字重是 600；不要因此误认成普通 Regular。

- 先确认实际用于测量和渲染的完整字形可用。优先复用用户提供或本机已有字体；缺失时可从 [Noto 官方静态字形文件](https://github.com/notofonts/noto-fonts/blob/main/hinted/ttf/NotoSansDisplay/NotoSansDisplay-SemiCondensedSemiBold.ttf) 获取到任务目录，不擅自安装系统字体。官方 Google Fonts 的 [Noto Sans Display](https://github.com/google/fonts/tree/main/ofl/notosansdisplay) 版本可能采用不同字体命名；使用其他版本前核对元数据和实际外观。
- 供 Figma 导入的 SVG 默认使用精确 PostScript 名称：常规体 `font-family="NotoSans-DisplaySemiCondensedSemiBold"`，斜体 `font-family="NotoSans-DisplaySemiCondensedSemiBoldItalic"`，并声明 `font-weight="600"`、`font-stretch="semi-condensed"`；斜体另加 `font-style="italic"`。不要继续使用带空格的 legacy family 作为默认导入声明，也不要只用普通 `Noto Sans` 配合 600、字宽或可变轴属性。不要把 Figma 的完整 style 字符串写入 CSS `font-style`。
- 浏览器预览使用同一实际字体文件。若浏览器无法解析 PostScript 名称，给正确字形建立同名 `@font-face`；自包含交付时可将字体嵌入 data URL，保留字体许可信息。`<text>` 的 family 与对应 `@font-face` 名称保持一致。嵌入字体能支持浏览器渲染，但不能替代 Figma 的实际字体匹配检查；不要为浏览器预览把正式 SVG 改回已知会错误匹配的名称。
- Figma 原生字体匹配优先使用实际可用的 `{ family: "Noto Sans", style: "Display SemiCondensed SemiBold" }`。若软件显示另一种 family/style 组合，按字体列表和元数据核对，不能只匹配 family 就认为字形一致。
- 用户已有斜体强调时，使用同一 Display 半窄 SemiBold 的斜体字形并核对元数据。[官方斜体文件](https://github.com/notofonts/noto-fonts/blob/main/hinted/ttf/NotoSansDisplay/NotoSansDisplay-SemiCondensedSemiBoldItalic.ttf) 的 typographic family/style 是 `Noto Sans` / `Display SemiCondensed SemiBold Italic`，legacy family 却是 `Noto Sans SemiCondensed SemiBold`，legacy subfamily 是 `Italic`。不能把完整名称任意拼成 `font-family`，也不能因 legacy 名称少了 Display 就判断实际字形。
- 使用可变字体时，确认其 Display 设计版本，核对并设置 `wght=600`、`wdth=87.5`（semi-condensed）；目标 Figma 的 Noto Sans 还需核对 `CTGR=100`（Display）。仅写入 CSS 可变轴不能保证 Figma 导入应用了它们，仍优先使用已验证的精确字体名称并检查实际结果。
- 中英文混排可在指定 Latin 字形后添加 Noto Sans SC 或 Noto Sans CJK SC；中文需确认对应字体和字形可用。参见 [Noto 官方用法](https://github.com/notofonts/noto-docs/blob/main/docs/website/use.md)。
- 字体变更后重新测量文字宽度、行高和边界，调整文字框、换行或间距。不要通过非等比缩放文字来塞进原框，也不要为了排版方便改成 Arial、Inter 或轮廓文字。
- 科研符号、上下标和公式要保留含义。简单公式可用 Unicode 和 `<tspan>` 的字号、基线处理；复杂公式若只能保留为路径，应先核对该局部不可编辑文字的取舍，不能宣称全部文字可编辑。
- Matplotlib 使用实际解析到指定字形的字体名称或字体文件，并设置 `rcParams["svg.fonttype"] = "none"`。导出后仍需检查数学文本，以及 Matplotlib 是否把同一段的多行文字拆成多个 `<text>`；必要时按逻辑文本块合并。见 [官方 SVG 字体说明](https://matplotlib.org/stable/users/explain/text/fonts.html#fonts-in-svg)。

## 从 Figma 导出修改稿

用户要导出修改稿继续编辑时，建议选择整张图的最外层 Frame：启用 `Include "id" attribute`，关闭 `Outline text`。前者保留基于对象名称的 ID，后者保留真实文字；两者都不会自动合并已经拆开的文本框，也不保证完整原生图层往返保留。

`Include bounding box` 针对单独文字的导出范围，`Ignore overlapping layers` 决定是否包含交叠的其他对象，按实际导出范围选择。导出后检查画布和文字是否完整，再以用户最新导出的 SVG 为编辑基础，保留用户已完成的调整；未收到新版时先完成技能等独立工作，不用旧稿覆盖用户的新修改。

## 尺寸和布局

默认沿用原图比例。需要单栏或指定比例时明确使用 `宽:高` 或 `高:宽`，不要把“5:4”自行解释成横版或竖版。

按实际论文模板的栏宽计算图高和最终字号，不能仅凭横竖判断占用空间。若宽为 W cm、画布宽高为 w×h，则放入一栏后的图高为 W×h/w；字号 s 对应约 s×(W/2.54×72)/w pt。这个估计以字体大小和画布坐标使用同一单位为前提，复杂变换须看实际渲染。

优先保证正文和关键标签的可读性。信息过密且调整超出已授权范围时，提出具体精简或重排方案后再改，不通过把字缩得很小来满足比例。加宽卡片、移动锚点时保持人物、图标和字体的原比例；不要对全图做非等比拉伸。

## 生成与验证

使用自包含 SVG、稳定且可识别的 `id` 和 `<g>`。按能一起移动或编辑的模块分组，例如记忆卡片、方法面板、注入记录、人物和结果；避免一条文字拆成逐字对象。确保渐变、剪裁和蒙版的引用有效。复杂插画是否含位图，要按实际结构说明。

如需查找本机渲染库，在 Codex 中可用 `load_workspace_dependencies` 定位运行时，再选择可用的离线 SVG 渲染器。预览用 PNG；正式可编辑交付仍是 SVG。不要用 AI 重新画文字或数值来代替可编辑重建。

字体声明或 `fc-match` 匹配成功不能单独证明实际渲染器采用了该字体。可用短文本的字形、宽度和笔画与目标字体文件的测量或渲染对照，排除静默替代。渲染器无法加载字体时，可在仅供预览的副本中用真实字体文件进行文字塑形及字形路径渲染；正式交付 SVG 始终保留 `<text>` / `<tspan>`，不能误交付用于预览的轮廓副本。这种预览只验证目标字形的排版，不证明其他软件已经解析到该字体。

### Figma 实际导入检查：MCP → Computer Use

需要确认 Figma 字体或原生文字时，检查真实目标文件；准备测试副本时保留用户现有画板。按以下顺序选择工具：

1. **Figma MCP 优先**：按对应 Figma 技能调用可用工具，检查导入后的 `TEXT` 节点及各文本样式片段。常规体应为 `{ family: "Noto Sans", style: "Display SemiCondensed SemiBold" }`，斜体为 `Display SemiCondensed SemiBold Italic`；能读取时核对 `fontWeight=600`、`variationSettings={ wght:600, wdth:87.5, CTGR:100 }` 和缺失字体状态。混合样式需逐片段检查。
2. **MCP 额度耗尽或不可用 → Computer Use**：停止重复调用 MCP，使用可用的 Computer Use 进入同一文件，选中实际文字层，在 Typography 中核对 family 与完整 style。常规体、斜体、混合样式及多行对象按本图实际使用情况检查；保存能显示所选文字与完整字形名称的截图。界面未暴露的属性不能声称已验证。
3. **报告实际范围**：区分逐节点检查与界面抽样。浏览器显示正确不证明 Figma 导入正确；只完成抽样时说明已检查的字形，不宣称全图每个节点均通过。两条路径都无法完成时交付本地文件并说明尚未验证的部分。

2026-10-06 的实际目标文件对照中，带空格的 `Noto Sans Display SemiCondensed SemiBold` 配合 600 被导入为 `Noto Sans / Bold`，实际参数为 700、100、0；仅增加 `font-stretch` 或 CSS 可变轴仍未修复。改为 `NotoSans-DisplaySemiCondensedSemiBold` 后，实际匹配为指定字形及 600、87.5、100；完整修正版的常规体和对应斜体另经真实界面抽样确认。这支持上述默认声明，不能据此推断所有 Figma 版本的内部匹配算法，也不能保证其他环境不经检查就一定匹配。

### 本地 SVG 结构检查

运行随附检查脚本：

```bash
python3 /path/to/research-figure-to-svg/scripts/validate_svg.py "/path/to/figure.svg"
```

脚本检查 XML、`viewBox`、唯一 ID、内部引用、字体声明、真实文字和位图数量，并报告包含多个 `<tspan>` 的文本对象数及声明的字重、字宽、可变轴。默认字体名单只包含上述两个精确 PostScript 名称及中文 Noto 字体，以阻止新稿重新使用已知错误匹配的声明。用户明确指定其他字体或仅检查旧稿结构时，可用 `--font-family "指定字体"` 覆盖默认检查；多种字体可重复传入该参数，覆盖名单不代表实际匹配已验证。

脚本通过只说明结构检查通过，不能自动判断哪些相邻行属于一个段落。还必须用实际指定字形渲染并检查：每个完整句子或段落是否对应一个文本对象、文字未遗漏、拼写和科研内容正确、未被遮挡或剪裁、彩色词组间距正确、人物比例未变、透明背景符合要求，以及目标栏宽下是否可读。布局保留任务还要对照原图核验模块位置、顺序、配色和装饰。

默认另存新版，不覆盖原图或旧稿。交付 SVG 链接和最终 PNG 预览，简短写明尺寸、比例、字体及重要的局部限制。明确区分“SVG 文本节点已验证”和“Figma 原生文字已验证”，不要求用户为常规可逆调整再次确认。

## 示例

**用户请求** → “把这张科研示意图转成能编辑的 SVG，我自己导入 Figma。”  
**具体操作** → 忠实重建文字、卡片和箭头，按模块分组，连贯多行文字放入同一个 `<text>`，使用 Noto Sans 的 Display SemiCondensed SemiBold 字形；验证和预览本地文件。  
**交付口径** → 提供 SVG 和 PNG，说明文字保留为文本节点；未做 Figma 导入验证，不调用 MCP。

**用户请求** → “这个 SVG 原排版就很好，只加宽一点，字体换成 Noto Sans。”  
**具体操作** → 保留面板、人物、原文和配色，调整画布及必要的框宽、文字锚点与间距；换字体后重新测量，不拉伸字体和人物。  
**交付口径** → 交付原排版微调版，报告具体宽高，源文件保留。

**用户请求** → “这个完整句子换行后变成了上下两个文本框；字体要 Noto Sans 的 Display SemiCondensed SemiBold。我已经改了一部分。”
**具体操作** → 以用户最新 SVG 为基础，保留已改内容；核对原文后合并为一个 `<text>`，内部用 `<tspan>` 定位各行，并使用完整指定字形。
**交付口径** → 说明单段多行文字与实际字形的验证结果；Figma 原生节点只在真正导入检查后确认。

**用户请求** → “改成适合单栏的高:宽 = 5:4，可以精简重复说明。”  
**具体操作** → 依据实际栏宽确认图高和字号，按已授权范围调整；保留关键科研内容，使用 Noto Sans。  
**交付口径** → 展示竖版预览和可编辑 SVG，不把此例的比例、布局或会议尺寸写成所有任务的默认值。

Figma 行为参考：[官方导入说明](https://help.figma.com/hc/en-us/articles/360040028034-Add-images-and-videos-to-designs)、[官方 SVG 导出设置](https://help.figma.com/hc/en-us/articles/13402894554519-Export-formats-and-settings-for-static-designs)。涉及在线操作时，以当前工具能力和实际验证为准。
