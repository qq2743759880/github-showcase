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

if __name__=='__main__':
    unittest.main()
