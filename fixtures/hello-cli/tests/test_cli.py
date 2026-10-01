from pathlib import Path
import subprocess
import sys
import unittest

APP=Path(__file__).resolve().parents[1]/'app.py'

class CliBehavior(unittest.TestCase):
    def run_cli(self,*args):
        return subprocess.run([sys.executable,str(APP),*args],capture_output=True,text=True)

    def test_default_greeting(self):
        result=self.run_cli()
        self.assertEqual(result.returncode,0)
        self.assertEqual(result.stdout.strip(),'Hello, world!')

    def test_custom_name(self):
        self.assertEqual(self.run_cli('Ada').stdout.strip(),'Hello, Ada!')

    def test_empty_name_is_rejected(self):
        self.assertNotEqual(self.run_cli(' ').returncode,0)

    def test_startup_check(self):
        result=self.run_cli('--check')
        self.assertEqual(result.returncode,0)
        self.assertIn('configuration OK',result.stdout)

if __name__=='__main__':
    unittest.main()
