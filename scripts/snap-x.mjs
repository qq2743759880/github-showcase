// Invoke the pinned local CLI and keep font/emoji caches inside this checkout.
import { spawnSync } from 'node:child_process';
import { readFileSync } from 'node:fs';
import path from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';

const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const pkg=path.join(root, 'node_modules/@snap-x/cli/package.json');
try {
  const version=JSON.parse(readFileSync(pkg, 'utf8')).version;
  if(version!=='0.2.1') throw new Error(`expected @snap-x/cli 0.2.1, found ${version}`);
} catch(error) {
  process.stderr.write(`BLOCKED: ${error.message}. Install with npm ci in the Skill checkout.\n`);
  process.exit(2);
}
const result=spawnSync(process.execPath,['--import',pathToFileURL(path.join(root,'scripts/windows-esm.mjs')).href,path.join(root,'node_modules/@snap-x/cli/bin.mjs'),...process.argv.slice(2)],{
  stdio:'inherit',
  env:{...process.env,SNAP_X_CACHE_DIR:path.join(root,'.cache/snap-x')}
});
if(result.error) {
  process.stderr.write(`BLOCKED: ${result.error.message}\n`);
  process.exit(2);
}
process.exit(result.status??2);
