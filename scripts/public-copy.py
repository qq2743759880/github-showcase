"""Bounded reader-label taxonomy check; never rewrites or translates copy."""
import hashlib,re
from html.parser import HTMLParser
from pathlib import Path

PATTERN=re.compile(r'\b(?:Languages\s+Hero|Runtime\s+Showcase|F0[1-9]|F10|(?:Reader|Showcase|Publication|Execution|Redistribution)\s+Surface|Hero)\b',re.I)
MIXED=re.compile(r'[\u4e00-\u9fff].*\b(?:Showcase|Consumer|Producer|Binding|Route)\b',re.I)
SKIP={'vendor','private','scripts','tests','test','.git','node_modules'}

class Labels(HTMLParser):
    def __init__(self):
        super().__init__();self.stack=[];self.active=[];self.labels=[]
    def handle_starttag(self,tag,attrs):
        attrs=dict(attrs)
        if tag=='img' and attrs.get('alt'):self.labels.append(attrs['alt'])
        if tag=='input' and attrs.get('type') in {'button','submit'}:self.labels.append(attrs.get('value',''))
        high=tag in {'title','h1','h2','h3','h4','h5','h6','button','figcaption','label'} or (tag=='a' and any(t=='nav' for t in self.stack))
        self.stack.append(tag)
        if high:self.active.append([tag,[]])
        if tag in {'img','input','br','hr','meta','link'}:self.handle_endtag(tag)
    def handle_data(self,data):
        if not any(t in {'code','pre','script','style','svg'} for t in self.stack):
            for _,parts in self.active:parts.append(data)
    def handle_endtag(self,tag):
        for item in list(self.active):
            if item[0]==tag:self.labels.append(''.join(item[1]));self.active.remove(item)
        if tag in self.stack:self.stack=self.stack[:len(self.stack)-1-self.stack[::-1].index(tag)]

def visible_labels(text,markdown):
    if not markdown:
        parser=Labels();parser.feed(text);return parser.labels
    lines=[];fence=None
    for line in text.splitlines():
        marker=re.match(r'^\s{0,3}(`{3,}|~{3,})',line)
        if marker:
            token=marker.group(1)
            if fence is None:fence=token
            elif token[0]==fence[0] and len(token)>=len(fence):fence=None
            lines.append('');continue
        lines.append('' if fence else line)
    clean=re.sub(r'<!--.*?-->','', '\n'.join(lines),flags=re.S)
    clean=re.sub(r'`+[^`\n]*`+','',clean)
    labels=[];previous=''
    for line in clean.splitlines():
        heading=re.match(r'^\s{0,3}#{1,6}\s+(.+?)\s*#*$',line)
        if heading:labels.append(heading.group(1))
        elif re.fullmatch(r'\s{0,3}(?:=+|-+)\s*',line) and previous.strip():labels.append(previous.strip())
        labels.extend(re.findall(r'!\[([^\]]*)\]\([^\n)]*\)',line))
        # Markdown navigation/CTA labels are visible; destinations are never inspected.
        labels.extend(re.findall(r'(?<!!)\[([^\]]+)\]\([^\n)]*\)',line))
        previous=line
    parser=Labels();parser.feed(clean);labels.extend(parser.labels)
    return [re.sub(r'[*_]+','',s).strip() for s in labels]

def check(export,policy):
    export=Path(export).resolve();errors=[];allowed=set()
    allowances=policy.get('public_copy_allowlist',[])
    if not isinstance(allowances,list):errors.append('public_copy_allowlist must be a list');allowances=[]
    for item in allowances:
        try:
            term=item['term'];ev=item['evidence'];name=ev['path'];path=(export/name).resolve()
            if not isinstance(term,str) or not term.strip() or not item['purpose'].strip():raise ValueError('term/purpose required')
            if '\\' in name or Path(name).is_absolute() or not path.is_relative_to(export) or set(Path(name).parts)&SKIP or Path(name).suffix.lower() not in {'.md','.html','.htm'} or any(p.is_symlink() for p in [(export/name),*(export/name).parents] if p.is_relative_to(export)):raise ValueError('public project document evidence required')
            raw=path.read_bytes()
            if hashlib.sha256(raw).hexdigest()!=ev['sha256'] or term not in raw.decode('utf-8'):raise ValueError('project term evidence changed or absent')
            allowed.add(term.casefold())
        except (KeyError,ValueError,TypeError,AttributeError,OSError) as exc:errors.append('invalid public_copy_allowlist: '+str(exc))
    for path in sorted(export.rglob('*')):
        if not path.is_file() or path.suffix.lower() not in {'.md','.html','.htm'} or set(path.relative_to(export).parts)&SKIP:continue
        if path.is_symlink():errors.append('reader document symlink: '+str(path.relative_to(export)));continue
        try:text=path.read_text(encoding='utf-8')
        except (OSError,UnicodeError) as exc:errors.append('unreadable reader document: '+str(exc));continue
        for label in visible_labels(text,path.suffix.lower()=='.md'):
            matches=[m.group(0) for m in PATTERN.finditer(label)]
            if MIXED.search(label):matches.append(label)
            for term in matches:
                if term.casefold() not in allowed:errors.append(str(path.relative_to(export))+': internal taxonomy in reader label: '+label);break
    return errors
