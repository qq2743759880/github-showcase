import importlib.util
from pathlib import Path
import tempfile
import unittest

spec=importlib.util.spec_from_file_location('release_gate',Path(__file__).resolve().parents[1]/'scripts/release-gate.py')
gate=importlib.util.module_from_spec(spec)
spec.loader.exec_module(gate)

class StopBehavior(unittest.TestCase):
    def policy(self):
        return {'license_status':'PASS','authorization':'NOT_AUTHORIZED','private_literals':[]}

    def test_clean_local_export_does_not_authorize_remote(self):
        with tempfile.TemporaryDirectory() as directory:
            result=gate.check(Path(directory),self.policy())
            self.assertEqual(result['F09'],'PASS')
            self.assertEqual(result['remote_publish'],'STOP')

    def test_synthetic_secret_blocks_delivery(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory)
            # Clearly synthetic fixture generated locally, never sent to a service.
            token='gh'+'p_'+'aB3cD4eF5gH6iJ7kL8mN9oP0qR1sT2uV3wX4'
            (root/'config.txt').write_text('api_key="'+token+'"',encoding='utf-8')
            result=gate.check(root,self.policy())
            self.assertEqual(result['F09'],'BLOCK')
            self.assertEqual(result['F10'],'STOP')

    def test_private_path_blocks_delivery(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory)
            (root/'README.md').write_text('/home/demo-private/project',encoding='utf-8')
            policy=self.policy()
            policy['private_literals']=['/home/demo-private/project']
            result=gate.check(root,policy)
            self.assertEqual(result['F10'],'STOP')

    def test_unresolved_license_blocks_delivery(self):
        with tempfile.TemporaryDirectory() as directory:
            policy=self.policy()
            policy['license_status']='BLOCKED'
            result=gate.check(Path(directory),policy)
            self.assertEqual(result['F10'],'STOP')

class ShowcaseGates(unittest.TestCase):
    """Asset Consumption / Reader Surface / Comprehension / Self-Dogfood gates."""

    def policy(self):
        return {'license_status':'PASS','authorization':'NOT_AUTHORIZED','private_literals':[]}

    def write(self, root, rel, text):
        path=root/rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding='utf-8')

    def test_visual_asset_consumption(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory)
            self.write(root,'README.md','![hero](assets/hero.svg)\n\nSee [details](docs/guide.md).\n')
            self.write(root,'assets/hero.svg','<svg/>')
            self.write(root,'assets/stray.svg','<svg/>')
            self.write(root,'docs/guide.md','guide')
            orphaned=gate.check_orphan_assets(root)
            self.assertEqual(orphaned,['assets/stray.svg'])

    def test_orphan_asset_blocks_release(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory)
            self.write(root,'README.md','# Title\n\nvalue first screen\n')
            self.write(root,'assets/stray.png','x')
            result=gate.run_showcase_gate(root,self.policy())
            self.assertIn('ORPHAN_ASSET_FAIL',result['gates'])
            self.assertFalse(result['READY_FOR_APPROVAL'])

    def test_reader_surface_before_maintainer_surface(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory)
            maintainer='# Title\n\ncommit '+('a'*40)+' uses puppeteer internals\n\n## Details\n'
            self.write(root,'README.md',maintainer)
            result=gate.run_showcase_gate(root,self.policy())
            self.assertIn('READER_SURFACE_FAIL',result['gates'])
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory)
            clean='# Title\n\nvalue for users first\n\n## Details\n\ncommit '+('a'*40)+' here\n'
            self.write(root,'README.md',clean)
            result=gate.run_showcase_gate(root,self.policy())
            self.assertNotIn('READER_SURFACE_FAIL',result['gates'])

    def test_self_dogfood_receipt_required(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory)
            self.write(root,'README.md','# Self showcase\n')
            result=gate.run_showcase_gate(root,self.policy(),require_self_dogfood=True)
            self.assertIn('SELF_DOGFOOD_MISSING',result['gates'])
        with tempfile.TemporaryDirectory() as directory:
            base=Path(directory)
            root=base/'export'; root.mkdir()
            receipt=base/'self.json'
            import json
            trace=base/'trace.json'; trace.write_text(json.dumps({'run_id':'current-test'}),encoding='utf-8')
            fidelity=base/'fidelity.json'; fidelity.write_text(json.dumps({'kind':'skill-fidelity','status':'PASS',
                'trace_path':'trace.json','trace_sha256':gate.evidence.sha256(trace),'export_digest':gate.evidence.tree_digest(root)}),encoding='utf-8')
            receipt.write_text(json.dumps({'kind':'self-dogfood','status':'PASS',
                'export_digest':gate.evidence.tree_digest(root),'product_digest':gate.evidence.tree_digest(gate.ROOT,skip_usage=True),
                'run_id':'current-test','fidelity_receipt':'fidelity.json','fidelity_sha256':gate.evidence.sha256(fidelity)}),encoding='utf-8')
            result=gate.run_showcase_gate(root,self.policy(),require_self_dogfood=True,self_dogfood_receipt=receipt)
            self.assertNotIn('SELF_DOGFOOD_MISSING',result['gates'])
            fidelity.unlink()
            self.assertIn('SELF_DOGFOOD_MISSING',gate.run_showcase_gate(root,self.policy(),require_self_dogfood=True,self_dogfood_receipt=receipt)['gates'])

    def test_showcase_gate_blocks_missing_hero_or_architecture_when_routed(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory)
            self.write(root,'README.md','# Title\n')
            policy=self.policy()
            policy['routed_assets']={'F06':'assets/hero.svg','F03':'docs/architecture.md'}
            result=gate.run_showcase_gate(root,policy)
            self.assertIn('ROUTED_ASSET_MISSING',result['gates'])
            self.assertTrue(any('F06' in m for m in result['routed_asset_missing']))
            self.assertTrue(any('F03' in m for m in result['routed_asset_missing']))
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory)
            self.write(root,'README.md','# Title\n')
            self.write(root,'assets/hero.svg','<svg/>')
            self.write(root,'docs/architecture.md','arch')
            policy=self.policy()
            policy['routed_assets']={'F06':'assets/hero.svg','F03':'docs/architecture.md'}
            result=gate.run_showcase_gate(root,policy)
            self.assertNotIn('ROUTED_ASSET_MISSING',result['gates'])


if __name__=='__main__':
    unittest.main()
