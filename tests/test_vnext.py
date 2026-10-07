import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[1]
def load(name,file):
    spec=importlib.util.spec_from_file_location(name,ROOT/'scripts'/file)
    module=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module
gate=load('vnext_gate','release-gate.py')
route=load('vnext_route','route-plan.py')
fidelity=load('vnext_fidelity','skill-fidelity.py')

class VNextBehavior(unittest.TestCase):
    def policy(self):
        return {'project_kind':'docs','license_status':'PASS','authorization':'NOT_AUTHORIZED','private_literals':[]}

    def test_quality_fail_returns_nonzero_even_when_safety_passes(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d); export=root/'export'; export.mkdir()
            (export/'README.md').write_text('# Useful guide\n',encoding='utf-8')
            policy=root/'policy.json'; policy.write_text(json.dumps(self.policy()),encoding='utf-8')
            result=subprocess.run([sys.executable,str(ROOT/'scripts/release-gate.py'),str(export),'--policy',str(policy),'--showcase-gate'],capture_output=True,text=True)
            self.assertNotEqual(result.returncode,0)
            self.assertEqual(json.loads(result.stdout)['F09'],'PASS')

    def test_plain_filename_mention_does_not_consume_asset(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d)
            (root/'README.md').write_text('# Guide\nhero.svg is an unlinked file\n',encoding='utf-8')
            (root/'hero.svg').write_text('<svg/>',encoding='utf-8')
            self.assertEqual(gate.check_orphan_assets(root),['hero.svg'])

    def test_buried_document_cannot_consume_visual(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d)
            (root/'README.md').write_text('# Guide\n',encoding='utf-8')
            (root/'buried.md').write_text('![hidden](hero.svg)',encoding='utf-8')
            (root/'hero.svg').write_text('<svg/>',encoding='utf-8')
            self.assertEqual(gate.check_orphan_assets(root),['hero.svg'])

    def test_literal_markdown_template_is_not_a_broken_reader_link(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d)
            (root/'README.md').write_text('# Guide\n```markdown\n[example](NOT_A_REAL_FILE.md)\n```\n',encoding='utf-8')
            self.assertEqual(gate.check_broken_links(root),[])

    def test_old_pass_keywords_are_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d); receipt=root/'old.md'
            receipt.write_text('READER_COMPREHENSION_GATE PASS 5/5 SELF_DOGFOOD_PASS',encoding='utf-8')
            (root/'README.md').write_text('# Guide\n',encoding='utf-8')
            self.assertTrue(gate.check_comprehension_receipt(receipt,root))
            self.assertTrue(gate.check_self_dogfood_receipt(receipt,root))

    def test_changed_readme_invalidates_comprehension(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d); readme=root/'README.md'; readme.write_text('# Guide\nUseful instructions.\n',encoding='utf-8')
            receipt=root/'reader.json'
            receipt.write_text(json.dumps({'kind':'reader-comprehension','status':'PASS','independent':True,'reviewer':'fixture','readme_sha256':gate.evidence.sha256(readme),'answers':[{'question':q,'answer':'A useful guide','quote':'Useful instructions.'} for q in ['what','problem','input','output','difference']]}),encoding='utf-8')
            self.assertEqual(gate.check_comprehension_receipt(receipt,root),[])
            readme.write_text('# Changed\nUseful instructions.\n',encoding='utf-8')
            self.assertTrue(gate.check_comprehension_receipt(receipt,root))

    def test_scanner_checks_exported_vendor_text(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d); (root/'vendor').mkdir()
            token='gh'+'p_'+'aB3cD4eF5gH6iJ7kL8mN9oP0qR1sT2uV3wX4'
            (root/'vendor/config.txt').write_text('api_key="'+token+'"',encoding='utf-8')
            self.assertEqual(gate.check(root,self.policy())['F10'],'STOP')

    def test_privacy_checks_large_text(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d); (root/'long.txt').write_text('a'*2_100_000+'PRIVATE_SENTINEL',encoding='utf-8')
            policy=self.policy(); policy['private_literals']=['PRIVATE_SENTINEL']
            self.assertEqual(gate.check(root,policy)['F10'],'STOP')

    def test_code_requires_new_clone_evidence(self):
        with tempfile.TemporaryDirectory() as d:
            policy=self.policy(); policy['project_kind']='code'
            result=gate.run_showcase_gate(Path(d),policy)
            self.assertIn('FRESH_CLONE_FAIL',result['gates'])

    def test_usage_content_changes_export_digest(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d); (root/'usage').mkdir()
            proof=root/'usage/result.txt'; proof.write_text('before',encoding='utf-8')
            original=gate.evidence.tree_digest(root)
            proof.write_text('after',encoding='utf-8')
            self.assertNotEqual(original,gate.evidence.tree_digest(root))

    def test_nonempty_commit_string_does_not_prove_clone(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d); export=root/'export'; export.mkdir()
            receipt=root/'clone.json'; receipt.write_text(json.dumps({'kind':'fresh-clone','status':'PASS',
                'commit':'arbitrary-string','export_digest':gate.evidence.tree_digest(export)}),encoding='utf-8')
            with self.assertRaisesRegex(ValueError,'separate local clone'):
                gate.evidence.fresh_clone(receipt,export,{'include_code':True,'entry_points':['server.py']},expected_commit='actual-commit')

    def test_design_does_not_load_software_metrics_or_demo_skills(self):
        data={'project':'design','project_roots':[{'path':'./design','root_type':'design'}], 'facts_source':{'preverified':False},'public_narrative':'narrative.md','architecture_spec':{},'workflow_spec':{},'metrics':[],'demo_scenario':{'status':'NOT_AVAILABLE'},'publication_policy':{'authorization':'NOT_AUTHORIZED'},'domain_profiles':[],'run_ledger':{'dir':'run'}}
        result=route.plan(data,['F02','F03','F05','F07','F08'])
        self.assertEqual([p['phase'] for p in result['phases']],['F01','F02','F08'])
        self.assertEqual({c['name'] for p in result['phases'] for c in p['capabilities']},{'readme-skill'})

    def test_skill_entry_alone_is_not_fidelity(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d); export=root/'export'; export.mkdir()
            trace=root/'trace.json'; trace.write_text(json.dumps({'routed_core':['readme-skill'],'calls':[{'skill':'readme-skill','loaded_resources':['vendor/readme-skill/SKILL.md'],'obligations':{},'outputs':[]}]}),encoding='utf-8')
            result=fidelity.validate(trace,export)
            self.assertEqual(result['status'],'FAIL')
            self.assertEqual(result['scores']['readme-skill']['covered'],0)

if __name__=='__main__':
    unittest.main()
