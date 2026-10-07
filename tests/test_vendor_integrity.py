import hashlib
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

spec=importlib.util.spec_from_file_location('vendor_verify',Path(__file__).resolve().parents[1]/'scripts/verify-vendors.py')
verifier=importlib.util.module_from_spec(spec)
spec.loader.exec_module(verifier)

class IntegrityBehavior(unittest.TestCase):
    def fixture(self,root):
        name='vendor/example/SKILL.md'
        file=root/name
        file.parent.mkdir(parents=True)
        file.write_text('original',encoding='utf-8')
        entry={'name':'example','phase':'F01','role':'primary','upstream':'https://example.invalid','revision':'test','entry':name,'files':[name],'hashes':{name:hashlib.sha256(file.read_bytes()).hexdigest()},'license':{'spdx':'MIT'},'modifications':[]}
        (root/'vendors.lock.json').write_text(json.dumps({'vendors':[entry]}),encoding='utf-8')
        return file

    def test_unchanged_snapshot_passes(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory)
            self.fixture(root)
            self.assertEqual(verifier.verify(root),[])

    def test_tampered_snapshot_fails(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory)
            file=self.fixture(root)
            file.write_text('changed',encoding='utf-8')
            self.assertTrue(verifier.verify(root))

    def test_unlocked_file_fails(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory)
            file=self.fixture(root)
            file.with_name('extra.txt').write_text('extra',encoding='utf-8')
            self.assertTrue(verifier.verify(root))

if __name__=='__main__':
    unittest.main()
