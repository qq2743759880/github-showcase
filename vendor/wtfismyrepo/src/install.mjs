/**
 * `wtfismyrepo install` — drop the skill into a coding agent so it loads
 * automatically. Defaults to Claude Code's personal skills directory; supports
 * project-local install and a generic "print the path" mode for other agents.
 */
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { fileURLToPath } from "node:url";

const HERE = path.dirname(fileURLToPath(import.meta.url));
const PKG_ROOT = path.resolve(HERE, "..");
const SKILL_SRC = path.join(PKG_ROOT, "SKILL.md");

const SKILL_NAME = "wtfismyrepo";

/** Resolve the destination skills dir for the chosen target. */
function destDir(target, cwd) {
  if (target === "project") {
    return path.join(cwd, ".claude", "skills", SKILL_NAME);
  }
  // global (default): the user's personal Claude Code skills dir
  return path.join(os.homedir(), ".claude", "skills", SKILL_NAME);
}

/**
 * @param {object} opts
 * @param {"global"|"project"} [opts.target="global"]
 * @param {string} [opts.cwd=process.cwd()]
 * @param {boolean} [opts.force=false]
 * @returns {{installed:boolean, dest:string, message:string}}
 */
export function installSkill(opts = {}) {
  const target = opts.target ?? "global";
  const cwd = opts.cwd ?? process.cwd();
  const force = opts.force ?? false;

  if (!fs.existsSync(SKILL_SRC)) {
    return { installed: false, dest: "", message: `Could not find SKILL.md at ${SKILL_SRC}` };
  }

  const dir = destDir(target, cwd);
  const dest = path.join(dir, "SKILL.md");

  if (fs.existsSync(dest) && !force) {
    return {
      installed: false,
      dest,
      message: `Skill already installed at ${dest}\n   Re-run with --force to overwrite.`,
    };
  }

  fs.mkdirSync(dir, { recursive: true });
  fs.copyFileSync(SKILL_SRC, dest);

  return {
    installed: true,
    dest,
    message: skillSuccessMessage(target, dest),
  };
}

function skillSuccessMessage(target, dest) {
  const scope = target === "project" ? "this project" : "all your projects (personal)";
  return [
    `✅  wtfismyrepo skill installed for ${scope}.`,
    `   → ${dest}`,
    ``,
    `Restart your Claude Code session, then just ask:`,
    `   "wtf is this repo"  ·  "I'm new here, where do I start?"`,
    ``,
    `Tip: run the analysis engine anytime with  npx wtfismyrepo .`,
  ].join("\n");
}

/** Print guidance for agents that don't use the Claude skills dir. */
export function manualHelp() {
  return [
    `To use wtfismyrepo with any agent that reads a context file, add this line`,
    `to your CLAUDE.md / AGENTS.md / .cursorrules:`,
    ``,
    `   @${SKILL_SRC}`,
    ``,
    `or copy ${SKILL_SRC} into your agent's skills/instructions directory.`,
  ].join("\n");
}
