// Pinned Mermaid CLI entry. Browser and npm caches stay in the checkout.
import { spawnSync } from 'node:child_process';
import { readFileSync } from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const directory=path.join(root,'node_modules/@mermaid-js/mermaid-cli');
try {
  if (JSON.parse(readFileSync(path.join(directory,'package.json'),'utf8')).version!=='11.17.0') throw new Error('expected mermaid-cli 11.17.0');
} catch(error) {
  process.stderr.write(`BLOCKED: ${error.message}; npm ci, then install the project-local Puppeteer browser.\n`);
  process.exit(2);
}
const result=spawnSync(process.execPath,[path.join(directory,'src/cli.js'),...process.argv.slice(2)],{
  stdio:'inherit',env:{...process.env,PUPPETEER_CACHE_DIR:path.join(root,'.cache/puppeteer')}
});
process.exit(result.status??2);
