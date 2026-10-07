import importlib.util,json,tempfile,unittest,zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('skill_surface_gate',ROOT/'scripts/release-gate.py')
gate=importlib.util.module_from_spec(spec);spec.loader.exec_module(gate)
class SkillDistribution(unittest.TestCase):
    def test_sealed_distribution_retains_exact_archive_bytes_not_just_members(self):
        # Recompressing the authority (even with equal members) must fail this test.
        pack=self.load_packager()
        with tempfile.TemporaryDirectory() as d:
            r=Path(d);src=r/'source';src.mkdir()
            entry=b'metadata:\n  version: "2.7.0-rc4"\n'
            (src/'SKILL.md').write_bytes(entry)
            with zipfile.ZipFile(src/'sealed.zip','w',compression=zipfile.ZIP_STORED) as z:
                z.comment=b'externally sealed archive identity'
                z.writestr('sample/SKILL.md',entry)
            m={'name':'sample','version':'2.7.0-rc4','source_root':str(src),'files':['SKILL.md'],'source_distribution':'sealed.zip','preserve_source_distribution':True}
            receipt=pack.package(m,r/'out.zip',r/'fresh')
            self.assertEqual((r/'out.zip').read_bytes(),(src/'sealed.zip').read_bytes())
            self.assertTrue(receipt['preserved_source_distribution'])
            self.assertEqual(pack.verify(receipt,src),[])
    def test_preserving_sealed_distribution_requires_an_explicit_authority(self):
        pack=self.load_packager()
        with tempfile.TemporaryDirectory() as d:
            r=Path(d);src=r/'source';src.mkdir()
            (src/'SKILL.md').write_bytes(b'metadata:\n  version: "2.7.0-rc4"\n')
            m={'name':'sample','version':'2.7.0-rc4','source_root':str(src),'files':['SKILL.md'],'preserve_source_distribution':True}
            with self.assertRaisesRegex(ValueError,'authority'):
                pack.package(m,r/'out.zip',r/'fresh')
    def test_current_original_distribution_preserves_paths_even_for_byte_identical_license_alias(self):
        pack=self.load_packager()
        with tempfile.TemporaryDirectory() as d:
            r=Path(d);src=r/'source';src.mkdir();(src/'references').mkdir()
            entry=b'metadata:\n  version: "1.2.3"\n'
            legal=b'MIT License\nOriginal copyright\n'
            (src/'SKILL.md').write_bytes(entry)
            (src/'references/LICENSE').write_bytes(legal)
            (src/'LICENSE').write_bytes(legal)
            with zipfile.ZipFile(src/'original.zip','w') as z:
                z.writestr('sample/SKILL.md',entry);z.writestr('sample/references/LICENSE',legal)
            m={'name':'sample','version':'1.2.3','source_root':str(src),'files':['SKILL.md','LICENSE'],'source_distribution':'original.zip'}
            with self.assertRaisesRegex(ValueError,'original distribution'):
                pack.package(m,r/'alias.zip',r/'alias-extract')
            m['files']=['SKILL.md','references/LICENSE']
            receipt=pack.package(m,r/'preserved.zip',r/'fresh')
            self.assertEqual(receipt['source_distribution']['files'],m['files'])
            self.assertEqual(pack.verify(receipt,src),[])
            (src/'original.zip').write_bytes(b'changed authority')
            self.assertTrue(pack.verify(receipt,src))
    def load_packager(self):
        file=ROOT/'scripts/runtime-package.py'
        self.assertTrue(file.is_file(),'generic minimal runtime packager is missing')
        spec=importlib.util.spec_from_file_location('runtime_package',file)
        module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module);return module
    def test_runtime_zip_is_allowlisted_original_bytes_and_fresh_extractable(self):
        pack=self.load_packager()
        with tempfile.TemporaryDirectory() as d:
            r=Path(d);src=r/'source';src.mkdir();(src/'references').mkdir()
            (src/'SKILL.md').write_bytes(b'---\nname: sample\nmetadata:\n  version: "1.2.3"\n---\nDo the task.\n')
            (src/'references/LICENSE').write_bytes(b'MIT License\nOriginal copyright\n')
            (src/'build.lock').write_text('not a runtime dependency')
            manifest={'name':'sample','version':'1.2.3','source_root':str(src),'files':['SKILL.md','references/LICENSE']}
            out=r/'sample.zip';receipt=pack.package(manifest,out,r/'fresh')
            self.assertEqual(receipt['status'],'PASS')
            with zipfile.ZipFile(out) as z:
                self.assertEqual(set(z.namelist()),{'sample/SKILL.md','sample/references/LICENSE'})
                self.assertEqual(z.read('sample/SKILL.md'),(src/'SKILL.md').read_bytes())
            self.assertEqual((r/'fresh/sample/SKILL.md').read_bytes(),(src/'SKILL.md').read_bytes())
            self.assertEqual(pack.verify(receipt,src),[])
            receipt_path=r/'receipt.json';receipt_path.write_text(json.dumps(receipt))
            policy={'project_form':'agent-skill','minimal_runtime_receipt':str(receipt_path),'distribution_surface':{'runtime':manifest['files']},'runtime_artifact':'sample.zip'}
            (src/'sample.zip').write_bytes(out.read_bytes())
            self.assertEqual(gate.check_minimal_runtime(src,policy),[])
            (src/'sample.zip').write_bytes(b'different package')
            self.assertTrue(gate.check_minimal_runtime(src,policy))
            with zipfile.ZipFile(out,'a') as z:z.writestr('sample/build.lock','noise')
            self.assertTrue(pack.verify(receipt,src))
    def test_runtime_manifest_rejects_escape_and_stale_version(self):
        pack=self.load_packager()
        with tempfile.TemporaryDirectory() as d:
            r=Path(d);(r/'SKILL.md').write_text('metadata:\n  version: "2.0"\n')
            m={'name':'sample','version':'1.0','source_root':str(r),'files':['SKILL.md']}
            with self.assertRaises(ValueError):pack.package(m,r/'out.zip',r/'fresh')
            m.update(version='2.0',files=['../outside'])
            with self.assertRaises(ValueError):pack.package(m,r/'out.zip',r/'fresh')
    def test_public_surface_cannot_contain_build_noise_or_unclassified_files(self):
        self.assertTrue(callable(getattr(gate,'check_distribution_surface',None)),'surface gate missing')
        with tempfile.TemporaryDirectory() as d:
            r=Path(d);(r/'SKILL.md').write_text('method');(r/'README.md').write_text('# Skill')
            policy={'project_form':'agent-skill','distribution_surface':{'runtime':['SKILL.md'],'execution':['SKILL.md'],'redistribution':['SKILL.md'],'showcase':['README.md'],'evidence':[]}}
            self.assertEqual(gate.check_distribution_surface(r,policy),[])
            (r/'package-lock.json').write_text('{}')
            self.assertTrue(gate.check_distribution_surface(r,policy))
    def test_process_value_preview_must_precede_install_and_tasks(self):
        self.assertTrue(callable(getattr(gate,'check_readme_profile',None)),'Agent Skill README profile gate missing')
        with tempfile.TemporaryDirectory() as d:
            r=Path(d)
            p={'readme_profile':{'workflow_is_product':True,'workflow_preview':'flow.png','interactive_url':'https://example.test/','install_anchor':'## Install','task_anchor':'## Quick Start'}}
            text='# Skill\n\n## Install\nGet it.\n\n## Flow\n![Flow](flow.png)\n[Open Interactive Diagram](https://example.test/)\n\n## Quick Start\nDo task.\n'
            (r/'README.md').write_text(text)
            self.assertTrue(gate.check_readme_profile(r,p))
            (r/'README.md').write_text(text.replace('## Install\nGet it.\n\n','')+'\n## Install\nGet it.\n')
            self.assertEqual(gate.check_readme_profile(r,p),[])
