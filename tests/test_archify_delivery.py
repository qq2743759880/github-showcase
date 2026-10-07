import importlib.util,json,tempfile,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('archify_gate',ROOT/'scripts/release-gate.py')
gate=importlib.util.module_from_spec(spec);spec.loader.exec_module(gate)
class ArchifyDelivery(unittest.TestCase):
    def test_routed_workflow_requires_native_delivery(self):
        with tempfile.TemporaryDirectory() as d:
            self.assertTrue(gate.check_archify_deliveries(Path(d),{'routed_assets':{'F04':'flow.png'}}))
    def test_finalized_source_and_html_are_content_bound(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);source=root/'flow.json';html=root/'flow.html';receipt=root/'native.json'
            source.write_text('{}');html.write_text('<html/>')
            receipt.write_text(json.dumps({'schemaVersion':1,'command':'finalize','status':'pass','ok':True,'quality':'showcase','diagnostics':[], 'gates':{k:'pass' for k in ['validate','deliver','check','browser-check']},'specification':{'path':str(source),'sha256':gate.evidence.sha256(source),'bytes':source.stat().st_size},'artifact':{'path':str(html),'sha256':gate.evidence.sha256(html),'bytes':html.stat().st_size}}))
            policy={'routed_assets':{'F04':'flow.html'},'archify_deliveries':[{'source':'flow.json','html':'flow.html','finalize_summary':str(receipt)}]}
            self.assertEqual(gate.check_archify_deliveries(root,policy),[])
            html.write_text('<html>changed</html>')
            self.assertTrue(gate.check_archify_deliveries(root,policy))
            html.write_text('<html/>');source.write_text('{"changed":true}')
            self.assertTrue(gate.check_archify_deliveries(root,policy))
