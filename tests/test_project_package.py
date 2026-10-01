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
        (ROOT/'usage').mkdir(exist_ok=True)
        self.temp=tempfile.TemporaryDirectory(dir=ROOT/'usage')
        self.addCleanup(self.temp.cleanup)
        self.base=Path(self.temp.name)
        self.export=self.base/'export'
        self.export.mkdir()
        self.git('init','-q')
        self.git('config','user.name','Fixture')
        self.git('config','user.email','fixture@example.invalid')
        self.policy={'license_status':'PASS','authorization':'NOT_AUTHORIZED','private_literals':[]}
    def git(self,*args):
        return subprocess.run(['git','-C',str(self.export),*args],capture_output=True,check=True)
    def commit(self,content):
        (self.export/'app.py').write_text(content,encoding='utf-8')
        self.git('add','--','app.py')
        self.git('commit','-qm','fixture')
    def test_ordinary_project_without_skill_metadata_packages(self):
        self.commit('print("hello")\n')
        result=module.package(self.export.resolve(),self.base/'project.zip',self.policy)
        self.assertEqual(result['status'],'PACKAGE_PASS')
        self.assertEqual(result['remote_publish'],'STOP')
        with zipfile.ZipFile(self.base/'project.zip') as bundle:
            self.assertEqual(bundle.namelist(),['app.py'])
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

if __name__=='__main__':
    unittest.main()
