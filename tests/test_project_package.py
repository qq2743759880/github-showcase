import importlib.util
import json
from pathlib import Path
import subprocess
import tempfile
import unittest
import zipfile

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('project_package',ROOT/'scripts/package-project.py')
module=importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

class ProjectPackageTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.base=Path(self.temp.name)
        self.export=self.base/'export'
        self.export.mkdir()
        self.git('init','-q')
        self.git('config','user.name','Fixture')
        self.git('config','user.email','fixture@example.invalid')
        self.policy={'project_kind':'docs','license_status':'PASS','authorization':'NOT_AUTHORIZED','private_literals':[]}
        self.receipt=self.base/'reader.json'
        self.fidelity=self.base/'fidelity.json'
    def git(self,*args):
        return subprocess.run(['git','-C',str(self.export),*args],capture_output=True,check=True)
    def commit(self,content):
        (self.export/'guide.txt').write_text(content,encoding='utf-8')
        text='# Guide\n\nA guide for reading project instructions.\n\n## Contents\n\n[Start](#quick-start)\n\n## Quick Start\n\nRead guide.txt for the useful result.\n'
        (self.export/'README.md').write_text(text,encoding='utf-8')
        self.receipt.write_text(json.dumps({'kind':'reader-comprehension','status':'PASS','independent':True,
            'reviewer':'fixture','readme_sha256':module.hashlib.sha256((self.export/'README.md').read_bytes()).hexdigest(),
            'answers':[{'question':q,'answer':'Fixture assertion','quote':'A guide for reading project instructions.'} for q in ['what','problem','input','output','difference']]}),encoding='utf-8')
        self.git('add','--','guide.txt','README.md')
        self.git('commit','-qm','fixture')
        # Synthetic protocol fixture only; semantic judgment belongs to a reviewer.
        import sys
        sys.path.insert(0,str(ROOT/'scripts'))
        import evidence
        contract=json.loads((ROOT/'references/core-contracts.json').read_text(encoding='utf-8'))['readme-skill']
        proof=self.base/'workflow.txt'; proof.write_text('Synthetic complete workflow evidence for package protocol test.',encoding='utf-8')
        trace=self.base/'trace.json'
        trace.write_text(json.dumps({'routed_core':['readme-skill'],'calls':[{'skill':'readme-skill',
            'loaded_resources':[contract['entry']], 'obligations':{key:{'observation':'Synthetic fixture',
            'evidence':[{'path':'workflow.txt','sha256':evidence.sha256(proof)}]} for key in contract['obligations']},
            'outputs':[{'path':'README.md','consumer':'README.md','link':'README.md','sha256':evidence.sha256(self.export/'README.md')}]}]}),encoding='utf-8')
        subprocess.run([sys.executable,str(ROOT/'scripts/skill-fidelity.py'),str(trace),str(self.export),'--output',str(self.fidelity)],check=True,capture_output=True)
    def test_ordinary_project_without_skill_metadata_packages(self):
        self.commit('print("hello")\n')
        result=module.package(self.export.resolve(),self.base/'project.zip',self.policy,self.receipt,self.fidelity)
        self.assertEqual(result['status'],'PACKAGE_PASS')
        self.assertEqual(result['remote_publish'],'STOP')
        with zipfile.ZipFile(self.base/'project.zip') as bundle:
            self.assertEqual(set(bundle.namelist()),{'guide.txt','README.md'})
    def test_gate_rejection_leaves_no_archive(self):
        self.commit('print("hello")\n')
        self.policy['license_status']='BLOCK'
        with self.assertRaisesRegex(ValueError,'F09 BLOCK; F10 STOP'):
            module.package(self.export.resolve(),self.base/'project.zip',self.policy)
        self.assertFalse((self.base/'project.zip').exists())
    def test_untracked_private_file_blocks_package(self):
        self.commit('print("hello")\n')
        (self.export/'private.txt').write_text('private',encoding='utf-8')
        with self.assertRaisesRegex(ValueError,'clean'):
            module.package(self.export.resolve(),self.base/'project.zip',self.policy)
        self.assertFalse((self.base/'project.zip').exists())

    def test_package_cannot_disable_fidelity_with_policy(self):
        self.commit('ordinary public instructions\n')
        self.policy['require_fidelity']=False
        with self.assertRaisesRegex(ValueError,'SKILL_FIDELITY_FAIL'):
            module.package(self.export.resolve(),self.base/'project.zip',self.policy,self.receipt)
        self.assertFalse((self.base/'project.zip').exists())

    def test_changed_workflow_proof_invalidates_package(self):
        self.commit('ordinary public instructions\n')
        (self.base/'workflow.txt').write_text('Changed after receipt',encoding='utf-8')
        with self.assertRaisesRegex(ValueError,'SKILL_FIDELITY_FAIL'):
            module.package(self.export.resolve(),self.base/'project.zip',self.policy,self.receipt,self.fidelity)

    def test_committed_usage_directory_is_not_publishable(self):
        self.commit('ordinary public instructions\n')
        (self.export/'usage').mkdir()
        (self.export/'usage/private.txt').write_text('runtime evidence',encoding='utf-8')
        self.git('add','usage'); self.git('commit','-qm','private runtime output')
        with self.assertRaisesRegex(ValueError,'private directory'):
            module.package(self.export.resolve(),self.base/'project.zip',self.policy,self.receipt,self.fidelity)

if __name__=='__main__':
    unittest.main()
