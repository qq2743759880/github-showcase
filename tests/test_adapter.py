import importlib.util
from pathlib import Path
import unittest

spec=importlib.util.spec_from_file_location('validator', Path(__file__).resolve().parents[1]/'scripts/validate-adapter.py')
validator=importlib.util.module_from_spec(spec)
spec.loader.exec_module(validator)

class AdapterBehavior(unittest.TestCase):
    def fixture(self):
        return {'project_roots':[{'path':'./project','root_type':'code'}], 'facts_source':{'preverified':False,'files':[],'private_files':[]},'public_narrative':'./narrative.md','architecture_spec':{},'workflow_spec':{},'metrics':[],'demo_scenario':{'status':'NOT_AVAILABLE'},'publication_policy':{'authorization':'NOT_AUTHORIZED'},'domain_profiles':[],'run_ledger':{'dir':'usage/current'},'source_release':{'include_code':True,'entry_points':['app.py'],'excluded':['.env'], 'fresh_clone_verify':{'runtime_deps_cmd':'python -m pip install -r requirements.txt','verification_deps_cmd':'python -m pip install -r requirements-test.txt','run_cmd':'python app.py --check','check_cmd':'python -m unittest discover'}}}

    def test_code_with_separate_dependencies_is_accepted(self):
        self.assertEqual(validator.validate(self.fixture()),[])

    def test_missing_verification_dependency_step_is_rejected(self):
        data=self.fixture()
        del data['source_release']['fresh_clone_verify']['verification_deps_cmd']
        self.assertTrue(validator.validate(data))

    def test_docs_need_no_runtime(self):
        data=self.fixture()
        data['project_roots'][0]['root_type']='docs'
        del data['source_release']
        self.assertEqual(validator.validate(data),[])

    def test_code_without_source_is_rejected(self):
        data=self.fixture()
        data['source_release']['include_code']=False
        self.assertTrue(validator.validate(data))

    def test_escaping_entry_point_is_rejected(self):
        data=self.fixture()
        data['source_release']['entry_points']=['../private.py']
        self.assertTrue(validator.validate(data))

    def test_unsubstantiated_metric_is_rejected(self):
        data=self.fixture()
        data['metrics']=[{'label':'speed','value':100}]
        self.assertTrue(validator.validate(data))

if __name__=='__main__':
    unittest.main()
