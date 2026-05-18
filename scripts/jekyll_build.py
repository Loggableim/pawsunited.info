#!/usr/bin/env python3
"""
PawsUnited NEON RETRO — Direct Static Site Builder
Processes Liquid templates with a simple Python-based engine.
"""

import os, re, yaml, shutil
from pathlib import Path

BASE = Path('E:/Pawsunited')
SITE = BASE / '_site_built'


def load_data():
    data = {}
    for f in sorted((BASE / '_data').glob('*.yml')):
        with open(f, encoding='utf-8') as fh:
            data[f.stem] = yaml.safe_load(fh)
    return data


def load_file(path):
    with open(path, encoding='utf-8') as f:
        return f.read()


def write_file(path, content):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)


def parse_frontmatter(content):
    m = re.match(r'^---\n(.*?)\n---\n?', content, flags=re.DOTALL)
    if m:
        return yaml.safe_load(m.group(1)) or {}, content[m.end():]
    return {}, content


class TemplateEngine:
    def __init__(self, data, includes_dir):
        self.data = data
        self.includes_dir = Path(includes_dir)

    def render_page(self, page_path):
        raw = load_file(page_path)
        fm, body = parse_frontmatter(raw)
        if not fm:
            return None
        ctx = {'page': fm, 'site': {'data': self.data}}
        layout = load_file(BASE / '_layouts' / 'default.html')
        layout = re.sub(r'^---[\s\S]*?---\n', '', layout, count=1)
        return self._process(layout, ctx)

    def _process(self, template, ctx):
        result = self._expand_includes(template, ctx)
        result = self._process_statements(result, ctx)
        result = self._substitute_vars(result, ctx)
        return result

    def _expand_includes(self, template, ctx):
        pattern = r'\{%-?\s*include\s+(\S+)\.html\s*-?%\}'
        def replacer(m):
            name = m.group(1)
            inc_path = self.includes_dir / f'{name}.html'
            if not inc_path.exists():
                return f'<!-- MISSING INCLUDE: {name} -->'
            inc = load_file(inc_path)
            inc = self._expand_includes(inc, ctx)
            inc = self._process_statements(inc, ctx)
            inc = self._substitute_vars(inc, ctx)
            return inc
        return re.sub(pattern, replacer, template)

    def _process_statements(self, template, ctx):
        # Strategy: Extract for loop regions FIRST so the assigns inside
        # them aren't destroyed by the global assign pass
        for_regions = []
        def save_for(m):
            for_regions.append(m.group(0))
            return f'__FOR_REGION_{len(for_regions)-1}__'
        
        # Save for loops
        saved = re.sub(
            r'\{%-?\s*for\s+\w+(?:,\s*\w+)?\s+in\s+.+?-?\s*%\}(.*?)\{%-?\s*endfor\s*-?%\}',
            save_for, template, flags=re.DOTALL
        )
        
        # Process assigns on template WITHOUT for loop bodies
        result = self._process_assign(saved, ctx)
        
        # Restore for loop regions
        for i, region in enumerate(for_regions):
            result = result.replace(f'__FOR_REGION_{i}__', region)
        
        # Process for loops (their assign tags are preserved because
        # they were saved before the global assign pass)
        result = self._process_for(result, ctx)
        
        # Process unless/if
        result = self._process_unless(result, ctx)
        result = self._process_if(result, ctx)
        return result

    # ── Variable Resolution ──────────────────────────────

    def _resolve_var(self, expr, ctx):
        expr = expr.strip()
        if expr.startswith("'") and expr.endswith("'"):
            return expr[1:-1]
        if expr.startswith('"') and expr.endswith('"'):
            return expr[1:-1]
        try:
            if '.' in expr: return float(expr)
            return int(expr)
        except:
            pass
        if expr == 'true': return True
        if expr == 'false': return False
        if expr in ('nil', 'null'): return None

        # page.field
        m = re.match(r'page\.(\w+)', expr)
        if m:
            return ctx.get('page', {}).get(m.group(1), '')

        # site.data.X.Y.Z
        m = re.match(r'^site\.data\.(\w+)\.(\w+)\.(\w+)$', expr)
        if m:
            d = self.data.get(m.group(1), {})
            if isinstance(d, dict): d = d.get(m.group(2), {})
            if isinstance(d, dict): return d.get(m.group(3), '')
            return str(d) if d else ''

        # site.data.X.Y
        m = re.match(r'^site\.data\.(\w+)\.(\w+)$', expr)
        if m:
            d = self.data.get(m.group(1), {})
            if isinstance(d, dict): return d.get(m.group(2), {})
            return d if d else ''

        # site.data.X
        m = re.match(r'^site\.data\.(\w+)$', expr)
        if m:
            return self.data.get(m.group(1), '')

        # site.data.X[page.lang]
        m = re.match(r"^site\.data\.(\w+)\[page\.lang\]$", expr)
        if m:
            lang = ctx.get('page', {}).get('lang', 'de')
            return self.data.get(m.group(1), {}).get(lang, {})

        # site.data.content[page.lang].Y.Z
        m = re.match(r"^site\.data\.content\[page\.lang\]\.(\w+)\.(\w+)", expr)
        if m:
            lang = ctx.get('page', {}).get('lang', 'de')
            content = self.data.get('content', {}).get(lang, {})
            section = content.get(m.group(1), {})
            if isinstance(section, dict):
                return section.get(m.group(2), '')
            return ''

        # site.data.content[page.lang].Y
        m = re.match(r"^site\.data\.content\[page\.lang\]\.(\w+)", expr)
        if m:
            lang = ctx.get('page', {}).get('lang', 'de')
            content = self.data.get('content', {}).get(lang, {})
            return content.get(m.group(1), {})

        # var.field
        m = re.match(r'(\w+)\.(\w+)', expr)
        if m:
            obj = self._resolve_var(m.group(1), ctx)
            if isinstance(obj, dict):
                val = obj.get(m.group(2))
                return val if val is not None else ''
            return ''

        # var[int]
        m = re.match(r'(\w+)\[(\d+)\]', expr)
        if m:
            obj = self._resolve_var(m.group(1), ctx)
            if isinstance(obj, (list, tuple)):
                idx = int(m.group(2))
                return obj[idx] if idx < len(obj) else ''
            if isinstance(obj, dict):
                return obj.get(int(m.group(2)), '')
            return ''

        # var[var]
        m = re.match(r'(\w+)\[(\w+)\]', expr)
        if m:
            obj = self._resolve_var(m.group(1), ctx)
            key = self._resolve_var(m.group(2), ctx)
            if isinstance(obj, dict) and isinstance(key, str):
                return obj.get(key, {})
            return ''

        # var['key']
        m = re.match(r"(\w+)\['(\w+)'\]", expr)
        if m:
            obj = self._resolve_var(m.group(1), ctx)
            if isinstance(obj, dict):
                return obj.get(m.group(2), {})
            return ''

        # Plain variable
        if expr in ctx:
            return ctx[expr]

        return ''

    # ── Assign ──────────────────────────────────

    def _process_assign(self, template, ctx):
        pattern = r'\{%-?\s*assign\s+(\w+)\s*=\s*(.+?)\s*-?%\}'
        def replacer(m):
            var_name = m.group(1)
            value_expr = m.group(2).strip()
            default_match = re.search(r'\|\s*default:\s*(.+)', value_expr)
            main_expr = re.sub(r'\|\s*default:\s*.+', '', value_expr).strip()
            val = self._resolve_var(main_expr, ctx)
            if default_match and (val is None or val == '' or val == {}):
                default_val = self._resolve_var(default_match.group(1).strip(), ctx)
                val = default_val
            ctx[var_name] = val
            return ''
        return re.sub(pattern, replacer, template)

    # ── If ──────────────────────────────────────

    def _process_if(self, template, ctx):
        pattern = r'\{%-?\s*if\s+(.+?)\s*-?%\}(.*?)\{%-?\s*endif\s*-?%\}'

        def _eval(cond):
            cond = cond.strip()
            m = re.match(r"(.+?)\s*!=\s*(.+)", cond)
            if m:
                l = str(self._resolve_var(m.group(1).strip(), ctx) or '')
                r = str(self._resolve_var(m.group(2).strip(), ctx) or '')
                return l != r
            m = re.match(r"(.+?)\s*==\s*(.+)", cond)
            if m:
                l = str(self._resolve_var(m.group(1).strip(), ctx) or '')
                r = str(self._resolve_var(m.group(2).strip(), ctx) or '')
                return l == r
            val = self._resolve_var(cond, ctx)
            if val is None or val == '' or val == 0 or val is False:
                return False
            if isinstance(val, (list, dict)) and len(val) == 0:
                return False
            return bool(val)

        def replacer(m):
            cond = m.group(1).strip()
            body = m.group(2)
            else_m = re.search(r'\{%-?\s*else\s*-?%\}', body)
            true_body, false_body = body, ''
            if else_m:
                true_body = body[:else_m.start()]
                false_body = body[else_m.end():]
            if _eval(cond):
                return true_body
            return false_body

        while re.search(pattern, template, re.DOTALL):
            template = re.sub(pattern, replacer, template, flags=re.DOTALL)
        return template

    # ── Unless ──────────────────────────────────

    def _process_unless(self, template, ctx):
        pattern = r'\{%-?\s*unless\s+(.+?)\s*-?%\}(.*?)\{%-?\s*endunless\s*-?%\}'
        def replacer(m):
            cond = m.group(1).strip()
            body = m.group(2)
            negated = False
            m2 = re.match(r"(.+?)\s*==\s*(.+)", cond)
            if m2:
                l = str(self._resolve_var(m2.group(1).strip(), ctx) or '')
                r = str(self._resolve_var(m2.group(2).strip(), ctx) or '')
                if l != r: negated = True
            m2 = re.match(r"(.+?)\s*!=\s*(.+)", cond)
            if m2 and not negated:
                l = str(self._resolve_var(m2.group(1).strip(), ctx) or '')
                r = str(self._resolve_var(m2.group(2).strip(), ctx) or '')
                if l == r: negated = True
            if not negated:
                val = self._resolve_var(cond, ctx)
                if val is None or val == '' or val == 0 or val is False or val == {}:
                    negated = True
                elif isinstance(val, (list, tuple)) and len(val) == 0:
                    negated = True
            return body if negated else ''
        return re.sub(pattern, replacer, template, flags=re.DOTALL)

    # ── For ─────────────────────────────────────

    def _process_for(self, template, ctx):
        pattern = r'\{%-?\s*for\s+(\w+)(?:,\s*(\w+))?\s+in\s+(.+?)\s*-?%\}(.*?)\{%-?\s*endfor\s*-?%\}'

        def replacer(m):
            loop_var = m.group(1)
            second_var = m.group(2)
            collection_expr = m.group(3).strip()
            body = m.group(4)

            collection = self._resolve_var(collection_expr, ctx)
            if not collection:
                return ''

            if isinstance(collection, dict):
                items = [[k, v] for k, v in collection.items()]
            elif isinstance(collection, (list, tuple)):
                items = list(collection)
            else:
                items = []

            parts = []
            for idx, item in enumerate(items):
                new_ctx = dict(ctx)
                new_ctx['forloop'] = {
                    'first': idx == 0, 'last': idx == len(items) - 1,
                    'index': idx + 1, 'index0': idx, 'length': len(items),
                }
                if isinstance(item, tuple) and len(item) == 2 and second_var:
                    new_ctx[loop_var] = item[0]
                    new_ctx[second_var] = item[1]
                elif isinstance(item, dict):
                    new_ctx[loop_var] = item
                else:
                    new_ctx[loop_var] = item

                # Process body: assigns → unless → if → vars
                p = self._process_assign(body, new_ctx)
                p = self._process_unless(p, new_ctx)
                p = self._process_if(p, new_ctx)
                p = self._substitute_vars(p, new_ctx)
                parts.append(p)

            return ''.join(parts)

        while re.search(r'\{%-?\s*for\s+', template):
            template = re.sub(pattern, replacer, template, flags=re.DOTALL)
        return template

    # ── Variable Substitution ───────────────────

    def _substitute_vars(self, template, ctx):
        pattern = r'\{\{\s*(.+?)\s*\}\}'
        def replacer(m):
            expr = m.group(1).strip()
            dm = re.search(r'\|\s*default:\s*(.+?)$', expr)
            if dm:
                me = expr[:dm.start()].strip()
                val = self._resolve_var(me, ctx)
                if val is None or val == '':
                    val = self._resolve_var(dm.group(1).strip(), ctx)
                return str(val) if val is not None else ''
            if '| absolute_url' in expr:
                me = expr.replace('| absolute_url', '').strip()
                val = self._resolve_var(me, ctx)
                if val and not str(val).startswith('http'):
                    return f'https://pawsunited.info{val}'
                return str(val) if val else ''
            val = self._resolve_var(expr, ctx)
            if isinstance(val, dict):
                return ''
            return str(val) if val is not None else ''
        return re.sub(pattern, replacer, template)


def build():
    print('🏗️  PawsUnited NEON RETRO — Direct Build\n')
    data = load_data()
    engine = TemplateEngine(data, BASE / '_includes')

    if SITE.exists():
        shutil.rmtree(SITE)

    if (BASE / 'assets').exists():
        shutil.copytree(BASE / 'assets', SITE / 'assets')
    for f in ['CNAME', 'robots.txt', 'sitemap.xml']:
        src = BASE / f
        if src.exists():
            shutil.copy2(src, SITE / f)

    pages = []
    for root, dirs, files in os.walk(str(BASE)):
        rp = Path(root).relative_to(BASE)
        parts = list(rp.parts)
        if parts and parts[0].startswith(('.', '_', 'scripts', 'node_modules', 'vendor')):
            continue
        for f in files:
            if f == 'index.html' and root != str(BASE / '_includes') and root != str(BASE / '_layouts'):
                pages.append(Path(root) / f)

    pages = sorted(set(pages))
    rendered = 0

    for page_path in pages:
        html = engine.render_page(page_path)
        if html is None:
            continue
        rel = page_path.relative_to(BASE)
        out = SITE / rel
        write_file(out, html)
        rendered += 1
        print(f'  ✅ {rel} ({len(html)} bytes)')

    legal_src = BASE / '_preview' / 'legal'
    legal_dst = SITE / 'legal'
    if legal_src.exists():
        legal_dst.mkdir(parents=True, exist_ok=True)
        for f in legal_src.glob('*.html'):
            shutil.copy2(f, legal_dst)
            print(f'  ✅ legal/{f.name} (copied)')

    print(f'\n✅ {rendered} Seiten → {SITE}')
    print('🎉 Fertig!')


if __name__ == '__main__':
    build()
