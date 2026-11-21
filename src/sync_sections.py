"""Keep the menu in step with the pages: proto.json's section list for each page (what the hamburger menu, custom flow
and section links read) is rebuilt from the page's own section list (this.sections in boards_<Page>.json), so sections
added, removed, renamed or moved on a page show up in the menu the same way. Run by rebuild_index.py.
  python3 src/sync_sections.py [proto.json ...]   (default: proto.json)"""
import json, re, sys, uuid, os
NS = uuid.UUID('6f1c1a52-4f0e-4b8e-9a51-6a7a2d1e0f00')
def sync(proto_path):
    P = json.load(open(proto_path)); changed = []
    for fn, B in P['boards'].items():
        src = 'boards_' + fn.replace('.dc.html', '') + '.json'
        if not os.path.exists(src): continue
        m = re.search(r'this\.sections = (\[.*?\]);', json.load(open(src))['script'])
        if not m: continue
        S = json.loads(m.group(1)); old = {x['sid']: x for x in B.get('sections', [])}
        new = []
        for i, s in enumerate(S):
            o = old.get(s['id']); aid = o['aid'] if o else str(uuid.uuid5(NS, fn + '#' + s['id']))
            new.append({'aid': aid, 'name': s['label'], 'sid': s['id'], 'top': s['top'], 'h': s['h']})
            a = P['artboards'].get(aid, {'board': fn}); a.update({'board': fn, 'section': i, 'name': s['label']}); P['artboards'][aid] = a
        keep = {x['aid'] for x in new}
        for x in B.get('sections', []):   # sections taken off the page leave the menu (and the links to them) too
            if x['aid'] not in keep: P['artboards'].pop(x['aid'], None)
        if new != B.get('sections'): changed.append(fn.replace('.dc.html', ''))
        B['sections'] = new
    json.dump(P, open(proto_path, 'w'), ensure_ascii=False, separators=(',', ':'))
    return changed
if __name__ == '__main__':
    for p in (sys.argv[1:] or ['proto.json']): print(p, 'sections synced:', ', '.join(sync(p)) or 'no changes')
