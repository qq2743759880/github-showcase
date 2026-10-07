import importlib.util,json,tempfile,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def load(file):
    spec=importlib.util.spec_from_file_location(file,ROOT/'scripts'/file)
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module);return module
gate=load('release-gate.py');pack=load('runtime-package.py')
class PublicationIntegrity(unittest.TestCase):
    def test_preview_cannot_replace_stable_default_or_share_its_version(self):
        check=getattr(gate,'check_release_channels',None)
        self.assertTrue(callable(check),'Stable / Preview coexistence gate missing')
        channels={'stable':{'version':'v1.4.2','url':'https://raw.githubusercontent.com/owner/tool/v1.4.2/dist/tool.zip'},'preview':{'version':'v2.0.0-rc2','url':'https://raw.githubusercontent.com/owner/tool/v2.0.0-rc2/dist/tool.zip','prerelease':True},'default_install':'stable'}
        self.assertEqual(check({'release_channels':channels}),[])
        channels['default_install']='preview'
        self.assertTrue(check({'release_channels':channels}))
        channels['default_install']='stable';channels['preview']['prerelease']=False
        self.assertTrue(check({'release_channels':channels}))
        channels['preview']['prerelease']=True;channels['preview']['version']='v1.4.2'
        self.assertTrue(check({'release_channels':channels}))
    def test_historical_version_cannot_download_from_mutable_branch(self):
        self.assertTrue(callable(getattr(gate,'check_immutable_artifact',None)),'historical artifact gate missing')
        base={'version':'v2.4.1','default_branch':'develop'}
        for url,want in [
            ('https://raw.githubusercontent.com/owner/tool/develop/dist/tool.zip',False),
            ('https://raw.githubusercontent.com/owner/tool/v2.4.1/dist/tool.zip',True),
            ('https://raw.githubusercontent.com/owner/tool/'+'a'*40+'/dist/tool.zip',True),
            ('https://github.com/owner/tool/releases/download/v2.4.1/tool.zip',True),
            ('https://github.com/owner/tool/releases/download/latest/tool.zip',False)]:
            with self.subTest(url=url):self.assertEqual(not gate.check_immutable_artifact({'release_artifact':{**base,'url':url}}),want)
    def test_license_identifiers_preserve_authoritative_value_in_any_language(self):
        self.assertTrue(callable(getattr(gate,'check_license_integrity',None)),'license identity gate missing')
        with tempfile.TemporaryDirectory() as d:
            root=Path(d)
            for identifier in ['MIT','Apache-2.0','GPL-3.0','BSD-3-Clause','MPL-2.0']:
                (root/'SKILL.md').write_text('---\nlicense: '+identifier+'\n---\n')
                policy={'license_identifier':{'identifier':identifier,'source':'SKILL.md','documents':['README.md']}}
                (root/'README.md').write_text('# Tool\n\n`'+identifier+'` 开源许可证。',encoding='utf-8')
                self.assertEqual(gate.check_license_integrity(root,policy),[])
                (root/'README.md').write_text('# Tool\n\n`'+identifier+' License` 开源许可证。',encoding='utf-8')
                self.assertTrue(gate.check_license_integrity(root,policy))
                (root/'README.md').write_text('# Tool\n\n许可由其他本地化名称代替。',encoding='utf-8')
                self.assertTrue(gate.check_license_integrity(root,policy))
    def test_package_declares_execution_separately_from_redistribution(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);source=root/'source';source.mkdir();(source/'references').mkdir()
            (source/'SKILL.md').write_text('metadata:\n  version: "1.0"\nmethod\n')
            (source/'references/LICENSE').write_text('original legal text')
            m={'name':'sample','version':'1.0','source_root':str(source),'files':['SKILL.md','references/LICENSE'],'execution':['SKILL.md'],'redistribution':['SKILL.md','references/LICENSE']}
            receipt=pack.package(m,root/'package.zip',root/'fresh')
            self.assertEqual(receipt.get('execution'),['SKILL.md'])
            self.assertEqual(receipt.get('redistribution'),['SKILL.md','references/LICENSE'])
            m['execution']=['missing.py']
            with self.assertRaises(ValueError):pack.package(m,root/'other.zip',root/'other')


class PublicationSurface(unittest.TestCase):
    def fixture(self,root,text='name: Verify\non: push\npermissions:\n  contents: read\njobs: {}\n'):
        (root/'SKILL.md').write_text('metadata:\n  version: "1.0"\nmethod\n')
        (root/'README.md').write_text('# Method\nRead the instruction.')
        path='.github/workflows/release.yml';(root/path).parent.mkdir(parents=True)
        (root/path).write_text(text)
        return {'project_form':'agent-skill','authorization':'NOT_AUTHORIZED','license_status':'PASS','private_literals':[],
            'distribution_surface':{'execution':['SKILL.md'],'redistribution':['SKILL.md'],'runtime':['SKILL.md'],'showcase':['README.md'],'publication':[path],'evidence':[]},
            'publication_purposes':{path:'Run public repository verification'}}
    def test_explicit_publication_is_allowlisted_and_not_reader_content(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);p=self.fixture(root)
            self.assertEqual(gate.check_distribution_surface(root,p),[])
            p['distribution_surface']['publication']=[];p['distribution_surface']['showcase'].append('.github/workflows/release.yml')
            self.assertTrue(gate.check_distribution_surface(root,p))
    def test_publication_requires_purpose_and_disjoint_canonical_paths(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);p=self.fixture(root)
            for bad in [{}, {'.github/workflows/release.yml':''}]:
                p['publication_purposes']=bad
                self.assertTrue(gate.check_distribution_surface(root,p))
            p=self.fixture_existing(root)
            p['distribution_surface']['showcase'].append('.github/workflows/release.yml')
            self.assertTrue(gate.check_distribution_surface(root,p))
            p=self.fixture_existing(root);p['distribution_surface']['publication']='.github/workflows/release.yml'
            self.assertTrue(gate.check_distribution_surface(root,p))
    def fixture_existing(self,root):
        return {'project_form':'agent-skill','authorization':'NOT_AUTHORIZED','license_status':'PASS','private_literals':[],
            'distribution_surface':{'execution':['SKILL.md'],'redistribution':['SKILL.md'],'runtime':['SKILL.md'],'showcase':['README.md'],'publication':['.github/workflows/release.yml'],'evidence':[]},
            'publication_purposes':{'.github/workflows/release.yml':'Public verification'}}
    def test_root_and_job_write_permissions_require_separate_publication_authorization(self):
        cases=['permissions:\n  contents: write\njobs: {}\n',
               'permissions:\n  contents: read\njobs:\n  deploy:\n    permissions:\n      pages: write\n      id-token: write\n',
               'permissions: write-all\njobs: {}\n']
        for text in cases:
            with self.subTest(text=text),tempfile.TemporaryDirectory() as d:
                root=Path(d);p=self.fixture(root,text);p['authorization']='APPROVED'
                self.assertTrue(gate.check_distribution_surface(root,p))
                p['publication_authorization']='APPROVED'
                self.assertEqual(gate.check_distribution_surface(root,p),[])
    def test_missing_dynamic_malformed_or_duplicate_permissions_fail_closed(self):
        for text in ['jobs: {}\n','permissions: "${{ inputs.permissions }}"\njobs: {}\n',
                     'permissions: [write]\njobs: {}\n','permissions:\n  contents: maybe\njobs: {}\n',
                     'permissions: {}\npermissions: write-all\njobs: {}\n',
                     'permissions: {}\njobs:\n  test:\n    permissions: [write]\n', 'permissions: [\n']:
            with self.subTest(text=text),tempfile.TemporaryDirectory() as d:
                root=Path(d);p=self.fixture(root,text);p['publication_authorization']='APPROVED'
                self.assertTrue(gate.check_distribution_surface(root,p))
    def test_private_paths_receipts_and_logs_cannot_be_laundered_as_publication(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);p=self.fixture(root)
            path=root/'.github/workflows/release.yml'
            path.write_text('permissions: {}\njobs: {}\n# original: '+ 'C:'+'/Users/dev/private/config.json\n')
            self.assertTrue(gate.check_distribution_surface(root,p))
            path.write_text('permissions: {}\njobs: {}\n')
            for name,text in [('receipts/private.json','{"passed":true}'),('.github/run.log','private output'),('.github/result.json','{"kind":"skill-fidelity","trace_path":"run.json"}')]:
                f=root/name;f.parent.mkdir(parents=True,exist_ok=True);f.write_text(text)
                p['distribution_surface']['publication'].append(name);p['publication_purposes'][name]='Publish delivery metadata'
                self.assertTrue(gate.check_distribution_surface(root,p))
                p['distribution_surface']['publication'].remove(name);p['publication_purposes'].pop(name);f.unlink()
    def test_publication_files_are_scanned_by_existing_secret_gate(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);p=self.fixture(root)
            (root/'.github/workflows/release.yml').write_text('permissions: {}\njobs: {}\nenv:\n  API_KEY: '+ 'sk-'+'proj-'+'AbCdEfGh1234567890'*5+'\n')
            result=gate.check(root,p)
            self.assertEqual(result['F09'],'BLOCK');self.assertGreater(result['secret_findings'],0)
    def test_release_metadata_binds_actual_immutable_artifact_identity(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);p=self.fixture(root);name='.github/release.json'
            p['distribution_surface']['publication'].append(name);p['publication_purposes'][name]='Release immutable runtime artifact'
            artifact={'version':'v1.0','url':'https://github.com/owner/tool/releases/download/v1.0/tool.zip'}
            p['release_artifact']=artifact
            (root/name).write_text(json.dumps({'release_tag':artifact['version'],'artifact_url':artifact['url']}))
            self.assertEqual(gate.check_distribution_surface(root,p),[])
            (root/name).write_text(json.dumps({'release_tag':artifact['version'],'zip_path':'dist/tool.zip'}))
            self.assertEqual(gate.check_distribution_surface(root,p),[])
            (root/name).write_text(json.dumps({'artifact_url':artifact['url']}))
            self.assertEqual(gate.check_distribution_surface(root,p),[])
            (root/name).write_text(json.dumps({'release_tag':'v1.0','artifact_url':'https://raw.githubusercontent.com/owner/tool/main/tool.zip'}))
            self.assertTrue(gate.check_distribution_surface(root,p))
            p.pop('release_artifact')
            p['release_channels']={'stable':artifact,'preview':{'version':'v2.0-rc1','url':'https://github.com/owner/tool/releases/download/v2.0-rc1/tool.zip','prerelease':True},'default_install':'stable'}
            (root/name).write_text(json.dumps({'release_channels':p['release_channels']}))
            self.assertEqual(gate.check_distribution_surface(root,p),[])
    def test_runtime_packager_rejects_publication_even_without_export_gate(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);p=self.fixture(root)
            manifest={'name':'sample','version':'1.0','source_root':str(root),'files':['SKILL.md','.github/workflows/release.yml']}
            with self.assertRaises(ValueError):pack.package(manifest,root.parent/(root.name+'.zip'),root.parent/(root.name+'-fresh'))
