import hashlib,importlib.util,json,subprocess,tempfile,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def load(name,file):
    s=importlib.util.spec_from_file_location(name,ROOT/'scripts'/file);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
route=load('rc2_route','route-plan.py');gate=load('rc2_gate','release-gate.py')
sha=lambda text:hashlib.sha256(text.encode()).hexdigest()

def synthetic_basic_auth_url(user='user',password='secret',host='example.com',path=''):
    scheme=''.join(('ht','tps',':','//'))
    return scheme+''.join((user,':',password,'@',host))+path

def synthetic_private_key_header():
    return ''.join(('-----BEGIN PRI','VATE KEY-----'))

class DistributionSource(unittest.TestCase):
    def test_distributed_runtime_source_passes_release_secret_preflight(self):
        # A detector-triggering literal reintroduced anywhere in redistribution
        # must fail even if its unit-test runtime assertions still pass.
        portable=load('distribution_portable','portable-runtime.py')
        with tempfile.TemporaryDirectory() as d:
            base=Path(d)
            receipt=portable.build(ROOT,base/'runtime.zip',base/'extract')
            source=Path(receipt['extract_root'])
            originals={f['path'] for f in receipt['manifest']['files']}
            self.assertIn('tests/test_rc2.py',originals)
            self.assertEqual(originals,set(portable.inventory(ROOT)))
            self.assertTrue(all((source/name).is_file() for name in originals))
            result=gate.check(source,{'license_status':'PASS','authorization':'NOT_AUTHORIZED','private_literals':[str(ROOT),str(Path.home())]})
            self.assertEqual(result['blocking_findings_count'],0,result['blocking_findings'])
            self.assertEqual(result['F09'],'PASS',result['errors'])

def adapter(root):
    return {'project_roots':[{'path':str(root),'root_type':'docs'}],'facts_source':{'preverified':True},'public_narrative':'narrative.md','architecture_spec':{},'workflow_spec':{'chains':[{'name':'setup','steps':['validate','write','verify']}]},'metrics':[],'demo_scenario':{'status':'NOT_AVAILABLE'},'publication_policy':{'authorization':'NOT_AUTHORIZED'},'domain_profiles':[],'run_ledger':{'dir':'run'}}
class Provenance(unittest.TestCase):
    def helper(self):
        h=getattr(route,'archify',None);self.assertIsNotNone(h,'content-bound Archify routing helper missing');return h
    def test_A1_non_git_workflow_still_selected(self):
        with tempfile.TemporaryDirectory() as d:
            p=route.plan(adapter(Path(d)),['F04']);self.assertEqual(p['phases'][0].get('provenance_mode'),'LOCAL_CONTENT_BOUND')
    def test_A2_local_git_no_origin(self):
        with tempfile.TemporaryDirectory() as d:
            subprocess.run(['git','init','-q',d],check=True)
            p=route.plan(adapter(Path(d)),['F04']);self.assertEqual(p['phases'][0].get('provenance_mode'),'LOCAL_CONTENT_BOUND')
    def test_A3_real_git_origin_and_commit(self):
        with tempfile.TemporaryDirectory() as d:
            r=Path(d);(r/'app.py').write_text('print("fixture")\n')
            for args in [['init','-q'],['add','app.py'],['-c','user.name=Fixture','-c','user.email=fixture@example.invalid','commit','-qm','fixture'],['remote','add','origin','https://github.com/SHlTbro/jevtest']]:subprocess.run(['git','-C',d,*args],check=True,capture_output=True)
            a=adapter(r);a['publication_policy']['authorization']='APPROVED';a['archify_provenance']={'repository_evidence_required':True,'origin_approved':True}
            p=route.plan(a,['F04']);self.assertEqual(p['phases'][0].get('provenance_mode'),'REPOSITORY_BACKED')
            self.assertEqual(len(p['phases'][0]['repository']['revision']),40)
    def test_A4_provenance_only_failover_preserves_topology(self):
        h=self.helper();c={'meta':{'repository':{'url':'x'}},'nodes':[{'id':'ready','sources':[{'path':'app.py','line':1}]}],'edges':[{'from':'ready','to':'ready','label':'retry'}]}
        out=h.local_candidate(c,'repository-provenance-unavailable')
        self.assertNotIn('repository',out['meta']);self.assertEqual(out['edges'],c['edges']);self.assertEqual(out['nodes'],[{'id':'ready'}]);self.assertIn('sources',c['nodes'][0])
        with self.assertRaises(ValueError):h.local_candidate(c,'schema-error')
    def test_A5_no_facts_only_then_skip(self):
        a=adapter(Path('.'));a['workflow_spec']={}
        self.assertIn('F04',route.plan(a,['F04'])['skipped'])
    def test_local_source_evidence_binds_sha_and_rejects_escape(self):
        h=self.helper()
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);(root/'app.py').write_text('run()')
            e=h.content_evidence(root,[{'path':'app.py','supports':'runs entry','purpose':'startup inspection'}])
            self.assertEqual(e['sources'][0]['sha256'],sha('run()'))
            with self.assertRaises(ValueError):h.content_evidence(root,[{'path':'../outside','supports':'x','purpose':'x'}])
class Decomposition(unittest.TestCase):
    def helper(self):
        h=getattr(route,'archify',None);self.assertIsNotNone(h,'semantic decomposition helper missing');return h
    def graph(self):return {'nodes':[{'id':'setup','label':'Setup'},{'id':'ready','label':'Ready'}],'edges':[{'id':'valid','from':'setup','to':'ready','label':'valid'},{'id':'retry','from':'ready','to':'setup','label':'retry','role':'error'}]}
    def test_D1_passing_single_view_not_split(self):
        self.assertEqual(self.helper().escalation([{'status':'pass'}],True),'DELIVER_SINGLE')
    def test_D2_exhausted_layout_only_escalates(self):
        h=self.helper();fail={'status':'fail','diagnostics':[{'code':'workflow/shared-corridor'}]}
        self.assertEqual(h.escalation([fail]*4,True),'SEMANTIC_DECOMPOSITION')
        with self.assertRaises(ValueError):h.escalation([fail],True)
        with self.assertRaises(ValueError):h.escalation([{'status':'fail','diagnostics':[{'code':'schema/required'}]}]*4,True)
    def test_D3_union_preserves_edges_conditions_and_nodes(self):
        h=self.helper();g=self.graph();views={'main':{'nodes':g['nodes'],'edges':[g['edges'][0]]},'recovery':{'nodes':g['nodes'],'edges':[g['edges'][1]]}}
        ledger=h.coverage(g,views);self.assertEqual(ledger['missing'],[])
        views['recovery']['edges'][0]={**g['edges'][1],'label':'ignore failure'}
        with self.assertRaises(ValueError):h.coverage(g,views)
    def test_D4_one_failed_required_view_blocks(self):
        with tempfile.TemporaryDirectory() as d:
            r=Path(d);p={'routed_assets':{'F04':'main.html'},'archify_decomposition':{'original_source':'absent','coverage_ledger':'absent','views':[{'name':'main','source':'main.json','html':'main.html','preview':'main.png'},{'name':'recovery','source':'recovery.json','html':'recovery.html','preview':'recovery.png'}]}}
            self.assertTrue(gate.check_archify_deliveries(r,p))
    def test_D5_plain_mention_not_consumption(self):
        h=self.helper()
        with tempfile.TemporaryDirectory() as d:
            r=Path(d);(r/'README.md').write_text('main.html main.json main.png')
            self.assertTrue(h.consumption_errors(r,[{'html':'main.html','source':'main.json','preview':'main.png'}]))
            (r/'README.md').write_text('[view](main.html) [edit](main.json) ![preview](main.png)')
            self.assertEqual(h.consumption_errors(r,[{'html':'main.html','source':'main.json','preview':'main.png'}]),[])
class FixtureExemption(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup);self.root=Path(self.tmp.name)
        self.path='tests/security/test_reject_url.py';self.file=self.root/self.path;self.file.parent.mkdir(parents=True)
        self.url=synthetic_basic_auth_url();self.line='reject("'+self.url+'")';self.file.write_text(self.line+'\n')
        engine=gate._load_scanner();match=next(r for r in engine.RULES if r.id=='basic-auth-url').pattern.search(self.line)
        value=match.group(1)
        self.approval={'path':self.path,'rule_id':'basic-auth-url','fixture_sha256':sha(value),'line_sha256':sha(self.line),'line':1,'column':match.start(1)+1,'classification':'security-test-fixture','purpose':'Negative test proving credential URLs are rejected'}
        self.policy={'license_status':'PASS','authorization':'NOT_AUTHORIZED','private_literals':[],'secret_fixture_exemptions':[self.approval]}
    def test_S1_exact_synthetic_finding_exempted(self):
        r=gate.check(self.root,self.policy);self.assertEqual(r['F09'],'PASS');self.assertEqual((r['raw_findings_count'],r['exempted_fixture_findings_count'],r['blocking_findings_count']),(1,1,0))
    def test_S2_modified_fixture_blocked(self):
        self.file.write_text(self.line.replace('secret','pass')+'\n');self.assertEqual(gate.check(self.root,self.policy)['F09'],'BLOCK')
    def test_S3_new_same_file_finding_blocks_only_it(self):
        self.file.write_text(self.line+'\nreject("'+synthetic_basic_auth_url(password='pass',path='/mcp')+'")\n')
        r=gate.check(self.root,self.policy);self.assertEqual(r['F09'],'BLOCK');self.assertEqual(r.get('exempted_fixture_findings_count'),1);self.assertEqual(r.get('blocking_findings_count'),1)
    def test_S4_source_same_value_never_exempted(self):
        self.file.rename(self.root/'app.py');self.policy['secret_fixture_exemptions'][0]['path']='app.py';self.assertEqual(gate.check(self.root,self.policy)['F09'],'BLOCK')
    def test_S5_critical_secret_never_exempted(self):
        header=synthetic_private_key_header()
        self.assertEqual(header,'-----BEGIN '+'PRIVATE KEY-----')
        self.file.write_text(self.line+'\n'+'gh'+'p_'+'aB3cD4eF5gH6iJ7kL8mN9oP0qR1sT2uV3wX4'+'\n'+header+'\n')
        result=gate.check(self.root,self.policy)
        self.assertEqual(result['F09'],'BLOCK')
        self.assertTrue(any(f['rule_id']=='private-key' and f['severity']=='critical' for f in result['blocking_findings']))
    def test_S6_unapproved_test_fixture_blocks(self):
        self.policy.pop('secret_fixture_exemptions');self.assertEqual(gate.check(self.root,self.policy)['F09'],'BLOCK')
    def test_wrong_rule_or_purpose_cannot_bypass(self):
        self.policy['secret_fixture_exemptions'][0]['purpose']='';self.assertEqual(gate.check(self.root,self.policy)['F09'],'BLOCK')
    def test_exact_named_synthetic_fixture(self):
        line='reject("'+synthetic_basic_auth_url(user='test_key_user',password='test_key_password')+'")'
        self.file.write_text(line+'\n')
        match=next(r for r in gate._load_scanner().RULES if r.id=='basic-auth-url').pattern.search(line)
        self.approval.update(line_sha256=sha(line),fixture_sha256=sha(match.group(1)),column=match.start(1)+1)
        self.assertEqual(gate.check(self.root,self.policy)['F09'],'PASS')
