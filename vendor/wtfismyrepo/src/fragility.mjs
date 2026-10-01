/**
 * Combine structural centrality (PageRank) with change frequency (churn) into
 * a single "fragility" score, plus an "importance" score.
 *
 * - importance = centrality. Read these first; they hold the system together.
 * - fragility  = centrality * churn. Central AND frequently changed = the
 *   files most likely to bite you. Touch with care.
 *
 * Both inputs are min-max normalized to [0,1] so the product is comparable
 * across repos of any size.
 */

function normalize(map) {
  const vals = [...map.values()];
  if (vals.length === 0) return new Map();
  const min = Math.min(...vals);
  const max = Math.max(...vals);
  const span = max - min || 1;
  return new Map([...map].map(([k, v]) => [k, (v - min) / span]));
}

/**
 * @param {Map<string,number>} rank   PageRank per file
 * @param {Map<string,number>} churn  commit-touch count per file
 * @returns {{importance: Array, fragility: Array}} sorted desc, [{file,score,...}]
 */
export function scoreFiles(rank, churn) {
  const nRank = normalize(rank);
  const nChurn = normalize(churn);

  const importance = [...nRank]
    .map(([file, score]) => ({ file, score, rank: rank.get(file) ?? 0 }))
    .sort((a, b) => b.score - a.score);

  const fragility = [...nRank]
    .map(([file, c]) => {
      const ch = nChurn.get(file) ?? 0;
      return {
        file,
        score: c * ch,
        centrality: c,
        churn: churn.get(file) ?? 0,
      };
    })
    .filter((x) => x.score > 0)
    .sort((a, b) => b.score - a.score);

  return { importance, fragility };
}
