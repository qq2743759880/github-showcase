// Pinned Mermaid CLI entry. Browser and npm caches stay in the checkout.
import { spawnSync } from 'node:child_process';
import { readFileSync, existsSync, mkdirSync, writeFileSync } from 'node:fs';
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
const candidates=[process.env.PUPPETEER_EXECUTABLE_PATH];
for(const base of [process.env.ProgramFiles,process.env['ProgramFiles(x86)'],process.env.LOCALAPPDATA]) {
  if(base) candidates.push(path.join(base,'Google/Chrome/Application/chrome.exe'),path.join(base,'Microsoft/Edge/Application/msedge.exe'));
}
const browser=candidates.find(p=>p&&existsSync(p));
const cache=path.join(root,'.cache/puppeteer');
mkdirSync(path.join(cache,'tmp'),{recursive:true});
const config=path.join(cache,'launch.json');
writeFileSync(config,JSON.stringify({headless:true,...(browser?{executablePath:browser}:{})}));
const result=spawnSync(process.execPath,[path.join(directory,'src/cli.js'),'-p',config,...process.argv.slice(2)],{
  stdio:'inherit',env:{...process.env,PUPPETEER_CACHE_DIR:cache,PUPPETEER_TMP_DIR:path.join(cache,'tmp')}
});
process.exit(result.status??2);
