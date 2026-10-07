import importlib.util,json,subprocess,sys,tempfile,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def load(name):
    p=ROOT/'scripts'/name
    if not p.is_file():return None
    spec=importlib.util.spec_from_file_location(name,p);module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module);return module
class PortableBehavior(unittest.TestCase):
    def test_manifest_classifies_consumers_without_dropping_native_examples(self):
        portable=load('portable-runtime.py')
        classify=getattr(portable,'classify',None)
        self.assertTrue(callable(classify),'consumer classification missing')
        paths=portable.inventory(ROOT);classes={p:classify(p) for p in paths}
        self.assertEqual(classes['tests/test_release_gate.py']['classification'],'VERIFICATION_ONLY')
        self.assertEqual(classes['vendor/archify/LICENSE']['classification'],'LEGAL_ONLY')
        self.assertEqual(classes['vendor/archify/examples/web-app.architecture.json']['classification'],'NATIVE_EXAMPLE_REQUIRED')
        self.assertEqual(classes['scripts/export-visual-runtime.py']['classification'],'PHASE_RUNTIME')
        self.assertTrue(all(c['consumer'] for c in classes.values()))
    def test_local_doctor_reports_optional_github_without_blocking(self):
        with tempfile.TemporaryDirectory() as d:
            plan=Path(d)/'plan.json';plan.write_text(json.dumps({'phases':[{'phase':'F09','runtime_dependencies':['python']}]}))
            result=subprocess.run([sys.executable,str(ROOT/'scripts/doctor.py'),'--plan',str(plan)],capture_output=True)
            self.assertEqual(result.returncode,0)
            data=json.loads(result.stdout)
            self.assertIn('github-backend',data['probes'])
            self.assertEqual(data['probes']['github-backend']['classification'],'Optional')
            self.assertEqual(data['probes']['python']['classification'],'Required')
            self.assertIn('archify',data['probes'])
            self.assertEqual(data['probes']['archify']['classification'],'Phase-specific')
    def test_portable_inventory_excludes_history_caches_and_own_showcase(self):
        portable=load('portable-runtime.py');self.assertIsNotNone(portable,'portable closure builder missing')
        paths=portable.inventory(ROOT)
        self.assertIn('SKILL.md',paths)
        self.assertIn('scripts/doctor.py',paths)
        self.assertIn('vendor/archify/SKILL.md',paths)
        self.assertNotIn('README.md',paths)
        self.assertFalse(any(set(Path(p).parts)&{'vNext','research','usage','.git','.mimosa','node_modules','.cache'} for p in paths))
    def test_missing_selected_browser_blocks_only_its_phase(self):
        doctor=load('doctor.py');self.assertTrue(callable(getattr(doctor,'diagnose',None)),'capability diagnosis missing')
        plan={'phases':[{'phase':'F04','runtime_dependencies':['node','chrome-or-chromium']},{'phase':'F09','runtime_dependencies':['python']}]}
        result=doctor.diagnose(ROOT,plan,{'tools':{'browser':'not-an-installed-browser'}})
        self.assertEqual(result['phases']['F04']['status'],'BLOCKED')
        self.assertEqual(result['phases']['F09']['status'],'AVAILABLE')
