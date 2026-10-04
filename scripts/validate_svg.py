#!/usr/bin/env python3
"""Read-only structural checks for an editable scientific SVG."""

import argparse
from collections import Counter
import json
import math
from pathlib import Path
import re
import xml.etree.ElementTree as ET


def validate(path, expected_fonts):
    root = ET.parse(path).getroot()
    errors = []
    warnings = []
    if root.tag.split('}')[-1] != 'svg':
        errors.append('Root element is not svg.')
    viewbox = root.get('viewBox', '').replace(',', ' ').split()
    try:
        viewbox = [float(v) for v in viewbox]
        if len(viewbox) != 4 or not all(math.isfinite(v) for v in viewbox) or min(viewbox[2:]) <= 0:
            raise ValueError()
    except ValueError:
        errors.append('Missing or invalid viewBox.')
        viewbox = None

    ids = [e.get('id') for e in root.iter() if e.get('id')]
    duplicate_ids = [name for name, count in Counter(ids).items() if count > 1]
    if duplicate_ids:
        errors.append(f'Duplicate ids: {duplicate_ids}')
    references = set()
    external_references = set()
    counts = Counter(e.tag.split('}')[-1] for e in root.iter())
    fonts = Counter()
    weights = Counter()

    def walk(element, inherited_font='', inherited_weight='400'):
        style = dict(part.split(':', 1) for part in element.get('style', '').split(';') if ':' in part)
        style = {k.strip(): v.strip() for k, v in style.items()}
        family = style.get('font-family', element.get('font-family', inherited_font))
        weight = style.get('font-weight', element.get('font-weight', inherited_weight))
        if element.tag.split('}')[-1] in {'text', 'tspan'} and (element.text or '').strip():
            primary = family.split(',')[0].strip().strip('\"\'')
            if primary:
                fonts[primary] += 1
            else:
                warnings.append('A text segment has no resolvable inline/inherited font family.')
            weights[weight] += 1
        for value in element.attrib.values():
            for match in re.findall(r'url\(\s*[\"\']?([^\)\"\']+)', value):
                reference = match.strip()
                if reference.startswith('#'):
                    references.add(reference[1:])
                elif not reference.startswith('data:'):
                    external_references.add(reference)
        for name, value in element.attrib.items():
            if name.split('}')[-1] == 'href' and element.tag.split('}')[-1] != 'a':
                if value.startswith('#'):
                    references.add(value[1:])
                elif not value.startswith('data:'):
                    external_references.add(value)
        for child in element:
            walk(child, family, weight)

    walk(root)
    missing = sorted(references - set(ids))
    if missing:
        errors.append(f'Missing internal references: {missing}')
    if external_references:
        errors.append(f'Non-self-contained references: {sorted(external_references)}')
    unexpected = sorted(set(fonts) - set(expected_fonts))
    if unexpected:
        errors.append(f'Unexpected declared fonts: {unexpected}')
    if not counts['text']:
        errors.append('No text elements; editable labels have not been established.')
    if counts['image']:
        warnings.append('Contains image elements; do not claim this is entirely vector artwork.')
    if counts['style']:
        warnings.append('Stylesheets are not resolved by this checker; inspect class-based typography separately.')
    warnings.append('Actual font loading, visual bounds, completeness and Figma TEXT nodes require separate checks.')
    return {
        'file': str(path.resolve()), 'structural_checks_passed': not errors,
        'width': root.get('width'), 'height': root.get('height'), 'viewBox': viewbox,
        'height_width_ratio': viewbox[3] / viewbox[2] if viewbox else None,
        'text_elements': counts['text'], 'text_spans': counts['tspan'],
        'groups': counts['g'], 'paths': counts['path'], 'images': counts['image'],
        'declared_font_segments': dict(fonts), 'declared_weight_segments': dict(weights),
        'errors': errors, 'warnings': sorted(set(warnings)),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('svg', type=Path)
    parser.add_argument('--font-family', action='append', dest='fonts')
    args = parser.parse_args()
    fonts = args.fonts or ['Noto Sans', 'Noto Sans SC', 'Noto Sans CJK SC']
    try:
        result = validate(args.svg, fonts)
    except (OSError, ET.ParseError) as error:
        result = {'structural_checks_passed': False, 'errors': [str(error)]}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result['structural_checks_passed'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
