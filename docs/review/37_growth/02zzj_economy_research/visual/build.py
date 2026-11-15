"""Merge the extraction passes into one dependency web and build the page.

python3 build.py SRC_DIR [OUT_DIR]    (SRC_DIR holds out_*.json and paradigms.json from the extraction passes)
Writes web_data.json (the merged web) and index.html (the page) next to this file.
"""
import glob, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
DOMAINS = {'energy', 'food', 'materials', 'metals', 'textiles', 'building', 'transport', 'exchange', 'institutions', 'information'}
PARADIGMS = {'foraging', 'horticultural_tribal', 'chiefdom', 'early_state', 'agrarian_empire', 'feudal_manorial', 'commercial_city_state',
             'early_modern_state', 'industrial', 'socialist_planned', 'service_information', 'pastoral_nomadic', 'irrigation',
             'maritime_trading', 'frontier_settler', 'plantation_slave', 'gift_economy'}
ETYPES = {'input', 'enables', 'replaces', 'byproduct'}

# ids made by different passes for the same thing -> one id (filled in after reading the passes)
ALIAS = json.load(open(os.path.join(HERE, 'aliases.json'))) if os.path.exists(os.path.join(HERE, 'aliases.json')) else {}


def main(src, dest=HERE):
    nodes, edges, report = {}, [], []
    for f in sorted(glob.glob(os.path.join(src, 'out_*.json'))):
        d = json.load(open(f))
        for n in d['nodes']:
            i = ALIAS.get(n['id'], n['id'])
            n['id'] = i
            n['parts'] = [str(n.get('part', '')).zfill(2)] if n.get('part') else []
            if i in nodes:
                m = nodes[i]
                m['parts'] = sorted(set(m['parts'] + n['parts']))
                m['chokepoint'] = bool(m.get('chokepoint')) or bool(n.get('chokepoint'))
                if len(n.get('desc', '')) > len(m.get('desc', '')):
                    for k in ('desc', 'label', 'place', 'kind', 'domain', 'paradigm'):
                        if n.get(k):
                            m[k] = n[k]
                if isinstance(n.get('start'), (int, float)) and n.get('date_src') == 'part' and (
                        m.get('date_src') != 'part' or n['start'] < m['start']):
                    m['start'], m['date_src'] = n['start'], 'part'
                if n.get('wide') and not m.get('wide'):
                    m['wide'] = n['wide']
            else:
                nodes[i] = n
        for e in d['edges']:
            e['from'] = ALIAS.get(e['from'], e['from'])
            e['to'] = ALIAS.get(e['to'], e['to'])
            e['part'] = os.path.basename(f)
            edges.append(e)
    # clean nodes
    for n in nodes.values():
        n['part'] = n['parts'][0] if n['parts'] else ''
        if n.get('domain') not in DOMAINS:
            report.append(f"domain? {n['id']} {n.get('domain')}")
            n['domain'] = 'materials'
        if n.get('paradigm') not in PARADIGMS:
            report.append(f"paradigm? {n['id']} {n.get('paradigm')}")
            n['paradigm'] = None
        if not isinstance(n.get('start'), (int, float)):
            report.append(f"start? {n['id']} {n.get('start')}")
            n['start'] = 0
        n['start'] = int(n['start'])
        if n.get('wide') is not None and not isinstance(n['wide'], (int, float)):
            n['wide'] = None
    # clean edges: drop dangling, self, duplicates (keep the first note; prefer the more specific type)
    rank = {'replaces': 0, 'byproduct': 1, 'input': 2, 'enables': 3}
    seen, out, dangling = {}, [], {}
    for e in edges:
        if e['from'] not in nodes or e['to'] not in nodes:
            for k in ('from', 'to'):
                if e[k] not in nodes:
                    dangling[e[k]] = dangling.get(e[k], 0) + 1
            continue
        if e['from'] == e['to']:
            continue
        t = e.get('type') if e.get('type') in ETYPES else 'enables'
        key = (e['from'], e['to'])
        rec = {'from': e['from'], 'to': e['to'], 'type': t, 'note': e.get('note', ''), 'src': e.get('src', 'part')}
        if key in seen:
            old = seen[key]
            if rank[t] < rank[old['type']]:
                old['type'] = t
            if not old['note'] and rec['note']:
                old['note'] = rec['note']
            continue
        seen[key] = rec
        out.append(rec)
    par = json.load(open(os.path.join(src, 'paradigms.json'))) if os.path.exists(os.path.join(src, 'paradigms.json')) else {}
    data = {'nodes': sorted(nodes.values(), key=lambda n: (n['start'], n['id'])), 'edges': out, 'paradigms': par}
    json.dump(data, open(os.path.join(dest, 'web_data.json'), 'w'), indent=1, ensure_ascii=False)
    tpl = open(os.path.join(HERE, 'template.html')).read()
    blob = json.dumps(data, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/')
    open(os.path.join(dest, 'index.html'), 'w').write(tpl.replace('__DATA__', blob))
    print(f"{len(nodes)} nodes, {len(out)} edges ({len(edges) - len(out)} dropped or merged)")
    if dangling:
        print('dangling ids:', ', '.join(f'{k}({v})' for k, v in sorted(dangling.items(), key=lambda x: -x[1])))
    for r in report:
        print(r)


if __name__ == '__main__':
    main(*sys.argv[1:3])
