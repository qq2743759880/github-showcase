import importlib.util
from pathlib import Path
import tempfile
import unittest

spec = importlib.util.spec_from_file_location('single_gate', Path(__file__).resolve().parents[1]/'scripts/release-gate.py')
gate = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gate)

class SinglePage(unittest.TestCase):
    def check(self, text, images=(), files=()):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root/'README.md').write_text(text, encoding='utf-8')
            for name in files:
                p=root/name; p.parent.mkdir(parents=True, exist_ok=True); p.write_text('asset')
            return gate.check_single_page(root, {'single_page': {'required_sections':['setup'], 'required_previews':list(images)}})

    def document(self, link='#setup', body='Run the tool with your project to produce a report.', anchor='<a name="setup"></a>', heading='Install'):
        return '# Other project\n\nReadable introduction.\n\n## Contents\n\n[Install]('+link+')\n\n'+anchor+'\n## '+heading+'\n\n'+body+'\n'

    def test_custom_anchor_and_external_supplements(self):
        self.assertEqual(self.check(self.document(body='Run the tool. [Source](https://example.com) [License](LICENSE)'), files=['LICENSE']), [])
    def test_english_heading(self):
        self.assertEqual(self.check(self.document(anchor='', heading='Setup')), [])
    def test_chinese_encoded_heading(self):
        text=self.document(link='#%E5%AE%89%E8%A3%85', anchor='<a name="setup"></a>', heading='安装')
        self.assertEqual(self.check(text), [])
    def test_missing_target(self):
        self.assertTrue(self.check(self.document(link='#absent')))
    def test_duplicate_target(self):
        self.assertTrue(self.check(self.document(body='Run.\n<a name="setup"></a>')))
    def test_cross_document_index(self):
        self.assertTrue(self.check(self.document(link='docs/guide.md#setup')))
    def test_link_only_stub(self):
        self.assertTrue(self.check(self.document(body='[See guide](docs/guide.md)')))
    def test_prose_stub(self):
        self.assertTrue(self.check(self.document(body='详见[安装说明](docs/guide.md)。')))
    def test_preview_in_other_document_is_insufficient(self):
        self.assertTrue(self.check(self.document(), ['assets/flow.svg'], ['assets/flow.svg']))
    def test_inline_preview(self):
        self.assertEqual(self.check(self.document(body='Run the tool.\n![Flow](assets/flow.svg)'), ['assets/flow.svg'], ['assets/flow.svg']), [])
    def test_rebased_image_missing(self):
        self.assertTrue(self.check(self.document(body='Run.\n![Flow](diagrams/flow.svg)'), ['diagrams/flow.svg'], ['docs/diagrams/flow.svg']))
    def test_fenced_fake_anchor(self):
        self.assertTrue(self.check(self.document(anchor='', heading='Install', body='```text\n## Setup\n<a name="setup"></a>\n```')))
    def test_fenced_fake_links_ignored(self):
        self.assertEqual(self.check(self.document(body='Run the tool.\n~~~text\n[Fake](docs/fake.md)\n~~~')), [])
    def test_index_must_precede_explanation(self):
        self.assertTrue(self.check(self.document().replace('## Contents', '## More\n\nSome explanation.\n\n## Contents')))
    def test_default_without_contract_still_rejects_missing_index(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory); (root/'README.md').write_text('# Sample\n\nIntro\n\n## Usage\nRun.')
            self.assertTrue(gate.check_single_page(root, {}))

if __name__ == '__main__': unittest.main()
