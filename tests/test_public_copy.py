import importlib.util,tempfile,unittest,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
s=importlib.util.spec_from_file_location('copy_gate',ROOT/'scripts/release-gate.py')
gate=importlib.util.module_from_spec(s);s.loader.exec_module(gate)

class PublicCopy(unittest.TestCase):
    def check(self,text,policy=None,name='README.md'):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);(root/name).write_text(text,encoding='utf-8')
            fn=getattr(gate,'check_public_copy',None)
            self.assertIsNotNone(fn,'PUBLIC_COPY_FAIL gate missing')
            return fn(root,policy or {})
    def test_COPY_01_chinese_internal_heading(self):
        self.assertTrue(self.check('## Languages Hero\n中文内容',{'public_copy_language':'zh'}))
    def test_COPY_02_english_internal_heading(self):
        self.assertTrue(self.check('## Languages Hero\nEnglish content',{'public_copy_language':'en'}))
    def test_COPY_03_natural_chinese(self):
        self.assertEqual(self.check('## 技术栈\nPython'),[])
    def test_COPY_04_runtime_technical_term(self):
        self.assertEqual(self.check('## Runtime API\nThe Runtime requires Python 3.12.\n服务运行时使用 Python 3.12。'),[])
    def test_COPY_05_asset_filename(self):
        self.assertEqual(self.check('![项目主视觉](assets/hero.png)'),[])
    def test_COPY_06_project_term_evidence(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);(root/'README.md').write_text('## Publication Surface',encoding='utf-8')
            fact=root/'ARCHITECTURE.md';fact.write_text('github-showcase defines Publication Surface.',encoding='utf-8')
            policy={'public_copy_allowlist':[{'term':'Publication Surface','purpose':'Explain this product architecture','evidence':{'path':'ARCHITECTURE.md','sha256':hashlib.sha256(fact.read_bytes()).hexdigest()}}]}
            fn=getattr(gate,'check_public_copy',None);self.assertIsNotNone(fn)
            self.assertEqual(fn(root,policy),[])
            fact.write_text('changed',encoding='utf-8');self.assertTrue(fn(root,policy))
    def test_COPY_07_phase_heading(self):
        self.assertTrue(self.check('## F06 Visual'))
    def test_COPY_08_html_navigation(self):
        self.assertTrue(self.check('<nav><a href="#x">Reader Surface</a><button>Execution Surface</button></nav>',name='index.html'))
    def test_COPY_09_code_examples(self):
        self.assertEqual(self.check('```json\n{"phase":"F06","role":"hero"}\n```\n```markdown\n## Reader Surface\n```\n`F06` is an example.'),[])
    def test_COPY_10_mixed_labels(self):
        for label in ['语言 Hero','项目 Showcase','能力 Consumer']:
            with self.subTest(label=label):self.assertTrue(self.check('## '+label))
    def test_caption_and_alt_leak(self):
        for text in ['![Languages Hero](assets/hero.png)','<figure><figcaption>F06 Visual</figcaption></figure>']:
            self.assertTrue(self.check(text,name='index.html' if text.startswith('<') else 'README.md'))
    def test_private_vendor_code_not_reader_copy(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d)
            for folder in ['vendor','private','scripts']:
                (root/folder).mkdir();(root/folder/'example.md').write_text('## F06 Visual')
            fn=getattr(gate,'check_public_copy',None);self.assertIsNotNone(fn);self.assertEqual(fn(root,{}),[])
    def test_no_default_self_product_exemption(self):
        self.assertTrue(self.check('## Publication Surface',{'project_name':'github-showcase'}))
    def test_setext_and_inline_markup(self):
        self.assertTrue(self.check('Reader Surface\n==============\n## **F06** Visual'))
    def test_body_and_identifier_not_banned(self):
        self.assertEqual(self.check('## HTTP route API\nThe consumer reads a receipt.\nUse [API](https://example.invalid/Hero/F06).'),[])
    def test_final_showcase_gate_blocks_copy(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);(root/'README.md').write_text('## Languages Hero',encoding='utf-8')
            result=gate.run_showcase_gate(root,{'project_kind':'docs','license_status':'PASS','authorization':'NOT_AUTHORIZED'})
            self.assertIn('PUBLIC_COPY_FAIL',result['gates']);self.assertFalse(result['READY_FOR_APPROVAL'])
    def test_allowlist_cannot_waive_other_terms(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);fact=root/'fact.md';fact.write_text('Publication Surface',encoding='utf-8')
            (root/'README.md').write_text('## Reader Surface',encoding='utf-8')
            policy={'public_copy_allowlist':[{'term':'Publication Surface','purpose':'Explain architecture','evidence':{'path':'fact.md','sha256':hashlib.sha256(fact.read_bytes()).hexdigest()}}]}
            self.assertTrue(gate.check_public_copy(root,policy))
    def test_missing_purpose_and_malformed_allowlist(self):
        self.assertTrue(self.check('## Publication Surface',{'public_copy_allowlist':None}))
        self.assertTrue(self.check('## Publication Surface',{'public_copy_allowlist':[{'term':'Publication Surface','purpose':''}]}))
