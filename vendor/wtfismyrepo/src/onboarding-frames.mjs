/**
 * Onboarding-specific cognitive frames — adapted from the ADHD framework
 * (github.com/UditAkhourii/adhd, MIT) for the codebase-explanation problem.
 *
 * ADHD frames push an LLM generator into corners it wouldn't naturally go.
 * Here each frame is a *vantage point* for explaining a codebase — a different
 * role / concern / angle that surfaces different aspects of the system.
 *
 * The skill uses these frames in ADHD's diverge→score→cluster→deepen loop:
 * instead of one linear walkthrough, N parallel explanations are generated
 * (one per frame), scored for fit to this developer's situation, and the
 * best angle is deepened into a full onboarding walkthrough.
 *
 * MIT attribution: engine design from ADHD by Udit Akhouri.
 */

export const ONBOARDING_FRAMES = [
  {
    id: "day-one-grad",
    label: "New grad, day one",
    prompt: `You are explaining this codebase to someone on their literal first day.
They know how to code but have never seen this system. Prioritize: the 5-word
mental model, the single entry point to open first, and the one concept that
unlocks everything else. Ignore depth — optimize for first foothold.`,
    tags: ["onboarding", "beginner"],
  },
  {
    id: "archeologist",
    label: "Archeologist reading ruins",
    prompt: `The code is a ruin. You are an archeologist. Read the git history, the
closed PRs, the old issues. What decisions were made and then unmade? What's
load-bearing vs. left over from a rewrite? The goal is not to understand the
code as it is but the *sequence of decisions* that produced it.`,
    tags: ["onboarding", "history"],
  },
  {
    id: "security-researcher",
    label: "Security researcher",
    prompt: `You are mapping the attack surface. Where is trust established? Where is
user input deserialized, rendered, or executed? What are the permission
boundaries? What breaks if an internal service is compromised? Explain the
codebase as a set of trust boundaries and data flows, not a feature list.`,
    tags: ["onboarding", "code"],
  },
  {
    id: "cto-due-diligence",
    label: "CTO doing due diligence",
    prompt: `You are evaluating this codebase for acquisition. What is the blast radius
of the top 3 modules? Where is the technical debt? What would break under 10x
load? What are the single points of failure? Explain what makes this system
fragile and what makes it resilient.`,
    tags: ["onboarding", "design"],
  },
  {
    id: "oncall-3am",
    label: "On-call at 3am",
    prompt: `The pager went off. You have never seen this repo. Where do you look first?
What are the runbooks? What are the most common failure modes? Where are the
logs, the metrics, the circuit breakers? Explain the system as a set of
failure scenarios and their diagnostic entry points.`,
    tags: ["onboarding", "code"],
  },
  {
    id: "product-manager",
    label: "Product manager tracing value",
    prompt: `Ignore the code structure. Trace how user value is delivered. What does a
user do? Where does their request enter the system, transform, and produce an
outcome? Map the code to the user journey, not to the directory tree.`,
    tags: ["onboarding", "design"],
  },
  {
    id: "refactorer",
    label: "Engineer planning a safe refactor",
    prompt: `You need to safely extract one module. Before touching anything, you need
to know: what depends on what? What is the coupling graph? What are the hidden
globals, the shared state, the side-effecting initializers? Explain the system
as a dependency map with the dangerous edges highlighted.`,
    tags: ["onboarding", "code"],
  },
  {
    id: "data-engineer",
    label: "Data engineer mapping flows",
    prompt: `Where does data come in? How does it transform? Where does it leave?
What is mutable, what is immutable? What is the source of truth for each
entity? Explain the codebase as a data-flow diagram: sources, transforms,
sinks, and state stores.`,
    tags: ["onboarding", "design"],
  },
  {
    id: "performance-engineer",
    label: "Performance engineer",
    prompt: `Where are the hot paths? What is the latency budget for the main operation?
Where are the N+1 queries, the unbounded loops, the blocking I/O? Which files
are on the critical path and which are off it? Explain the system as a
performance profile: fast parts, slow parts, and why.`,
    tags: ["onboarding", "code"],
  },
  {
    id: "inversion",
    label: "Inversion: how to break this",
    prompt: `To understand a system, understand how to destroy it. What are the
assumptions that, if violated, cascade into total failure? What would a chaos
monkey target? Explain the system by working backwards from its failure modes —
what the failure modes are tells you what the system actually is.`,
    tags: ["onboarding", "wild"],
  },
  {
    id: "domain-expert",
    label: "Domain expert ignoring implementation",
    prompt: `Forget the language, the framework, the cloud provider. What *problem domain*
does this code represent? What are the business entities, the rules, the
invariants — the things that would still exist even if you rewrote this in a
completely different stack? Explain the domain model, not the implementation.`,
    tags: ["onboarding", "design"],
  },
  {
    id: "contrarian",
    label: "Contrarian: what's wrong here",
    prompt: `What are the decisions in this codebase that a reasonable engineer would
disagree with? What conventions are broken, what patterns are mis-applied,
what is over-engineered and what is dangerously under-engineered? Understanding
where the code is wrong or weird is often faster than understanding where it's right.`,
    tags: ["onboarding", "wild"],
  },
];

/** Tags that indicate engineering-focused frames. */
const CODE_TAGS = new Set(["code", "design"]);

/**
 * Select N frames for an onboarding run.
 * Always includes at least one wild/non-obvious frame so divergence stays broad.
 *
 * Adapted from ADHD's selectFrames() by Udit Akhouri (MIT).
 *
 * @param {number} n
 * @param {boolean} [codeFirst=true] bias toward code/design frames
 * @returns {typeof ONBOARDING_FRAMES}
 */
export function selectOnboardingFrames(n, codeFirst = true) {
  const pool = codeFirst
    ? ONBOARDING_FRAMES.filter((f) => f.tags.some((t) => CODE_TAGS.has(t)))
    : [...ONBOARDING_FRAMES];
  const wild = ONBOARDING_FRAMES.filter((f) => f.tags.includes("wild"));

  const shuffled = [...pool].sort(() => Math.random() - 0.5);
  const picked = shuffled.slice(0, Math.max(1, n - 1));
  const wildPick = wild[Math.floor(Math.random() * wild.length)];
  if (!picked.find((f) => f.id === wildPick.id)) picked.push(wildPick);
  return picked.slice(0, n);
}
