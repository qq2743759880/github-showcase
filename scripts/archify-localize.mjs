// Preserve the selected built-in locale when authoring reader terminology.
import fs from 'node:fs';
import {catalogKeys,translateMessage,validateTranslations} from '../vendor/archify/renderers/shared/i18n.mjs';
const input=process.argv[2];
if(!input) throw new Error('Usage: node scripts/archify-localize.mjs <candidate.json>');
const raw=JSON.parse(fs.readFileSync(input,'utf8'));
const locale=raw.meta?.locale;
if(!['en','zh-CN'].includes(locale)) throw new Error('Supply a complete catalog for non-built-in locales');
const overrides=raw.meta.translations||{};
const checked=validateTranslations(overrides);
if(checked.unknownKeys.length||checked.placeholderMismatches.length) throw new Error('Invalid native translation keys or placeholders');
raw.meta.translations={...Object.fromEntries(catalogKeys().map(key=>[key,translateMessage(locale,key)])),...overrides};
fs.writeFileSync(input,JSON.stringify(raw,null,2)+'\n');
console.log(JSON.stringify({status:'PASS',locale,keys:Object.keys(raw.meta.translations).length}));
