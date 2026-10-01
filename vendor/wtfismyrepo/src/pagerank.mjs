/**
 * PageRank over a directed import graph.
 *
 * Nodes = files. An edge A -> B means "A imports B", so B accumulates rank
 * from everything that depends on it. High rank = structurally central file
 * (the thing that, if you break it, breaks everything).
 *
 * Standard power-iteration PageRank with a damping factor and dangling-node
 * handling, so it converges reliably on any graph shape.
 *
 * @param {Map<string, Set<string>>} graph  adjacency: node -> set of nodes it points to
 * @param {object} [opts]
 * @param {number} [opts.damping=0.85]
 * @param {number} [opts.epsilon=1e-8]    convergence threshold (L1 delta)
 * @param {number} [opts.maxIter=200]
 * @returns {Map<string, number>} node -> rank (sums to ~1)
 */
export function pageRank(graph, opts = {}) {
  const damping = opts.damping ?? 0.85;
  const epsilon = opts.epsilon ?? 1e-8;
  const maxIter = opts.maxIter ?? 200;

  // Collect the full node set (sources AND targets, since a target may never
  // appear as a source key).
  const nodes = new Set(graph.keys());
  for (const targets of graph.values()) {
    for (const t of targets) nodes.add(t);
  }
  const N = nodes.size;
  if (N === 0) return new Map();

  const nodeList = [...nodes];
  const init = 1 / N;
  let rank = new Map(nodeList.map((n) => [n, init]));

  // Pre-compute out-degree for each node.
  const outDeg = new Map(nodeList.map((n) => [n, (graph.get(n)?.size) ?? 0]));

  for (let iter = 0; iter < maxIter; iter++) {
    const next = new Map(nodeList.map((n) => [n, 0]));

    // Dangling mass: nodes with no outgoing edges distribute their rank
    // evenly across all nodes (otherwise rank leaks out of the system).
    let dangling = 0;
    for (const n of nodeList) {
      if (outDeg.get(n) === 0) dangling += rank.get(n);
    }
    const danglingShare = (damping * dangling) / N;
    const teleport = (1 - damping) / N;

    for (const n of nodeList) {
      next.set(n, teleport + danglingShare);
    }

    for (const [src, targets] of graph) {
      const deg = outDeg.get(src);
      if (!deg) continue;
      const share = (damping * rank.get(src)) / deg;
      for (const t of targets) {
        next.set(t, next.get(t) + share);
      }
    }

    // Check convergence (L1 norm of the change).
    let delta = 0;
    for (const n of nodeList) delta += Math.abs(next.get(n) - rank.get(n));
    rank = next;
    if (delta < epsilon) break;
  }

  return rank;
}
