# Generated Icons: Exploration Plan

**Status**: Draft, 2026-10-15
**Owner**: scott2b
**Scope**: How Reifire should approach icons that are generated rather than retrieved, what we already know, and what has to be built so the question can be answered with evidence instead of opinion.

---

## 1. Why this exists

Reifire turns a prompt into persistent visual objects. Every concept that `reify()` extracts
(nouns, verbs, adjectives, multi-word objects such as "baby Cthulhu") needs a small icon, and
the vocabulary is open: it is whatever people type. Retrieval from icon libraries covers the
common nouns. It does not cover verbs, abstract modifiers, domain concepts, or invented
compounds, and that tail is exactly the part of a prompt a user most needs to see reified,
because it is the part they are least likely to have words for.

Generation is the only route that is open-vocabulary. It is also the route we understand
least. Three model families can produce an icon from text today, and each fails in a
different way (section 3). We do not know which one, or which combination, gives acceptable
icons for Reifire's vocabulary at acceptable cost and latency. Nobody does; the published
benchmarks measure other things.

So this is an exploration, and the plan treats it as one. The deliverable of the first phase
is not a generator. It is the harness that lets us run a term list through any backend,
look at the candidates, record what a person accepts, and compare routes on the same terms.
Backends are expected to come and go. The harness, the term corpus, the provenance records,
and the acceptance data are what accumulate.

Two constraints are fixed from the outset:

- **Local and service backends are peers.** A local LLM through Ollama, a hosted LLM, a
  local diffusion model through Draw Things, and a hosted vector model like Recraft all sit
  behind the same interface and are selected by configuration. Exploration needs to compare
  them; production users will have different tolerances for cost, privacy and latency.
- **A person stays in the loop until the data says otherwise.** Automatic selection among
  candidates is the unsolved problem (section 10). Until a judge is shown to agree with
  human acceptance, candidates are reviewed, and the review is what the experiment records.
- **Size and style are settings.** Target render size and style family (line or filled
  glyph) are configuration on the style object, with bounded defaults for development.
  Nothing in the harness or the providers hard-codes either; both are expected to be
  revised as the reified view evolves.

## 2. What has already been done

The idea of generated visuals has been in the project since the visualization spec, but
only one concrete move has been made toward generated icons.

| When | Where | What it did | Status |
|---|---|---|---|
| 2025 | `VISUALIZATION_SPEC.md` §3.3 | Reserved an `"openai"` visualization source for generated raster images, with `model` and `prompt` properties. | Spec only. `IconManager` treats the source as a fallback and never generates. |
| 2025-11-18 | `RECOMMENDATIONS.md`, `PROJECT_PLAN.md` weeks 6 and 8 | Planned emoji, Font Awesome and user-upload providers, a configurable provider priority order, and LLM cost tracking for reification. | Not built. No generation was planned; the LLM budget was for parsing prompts, not drawing icons. |
| 2026-03-24 | commit `c9b8f07` | Pluggable `IconProvider` protocol and `ProviderChain`; 403 bundled Lucide and Octicons SVGs with a 431-term index; adapters for Material, Noun Project and an `LLMSVGProvider` built on Pydantic AI. | Shipped. The LLM provider is the first generated-icon code in the repo. |
| `ROADMAP.md` | Visualization section | "Implement icon preference system", "Create local icon cache", "Add SVG optimization". | Open. All three are prerequisites for this plan and are absorbed by it. |

What `LLMSVGProvider` does today, read from `src/reifire/visualization/providers/llm_svg.py`:

- Priority 80, so it is consulted only when every retrieval provider returns nothing.
- One hosted LLM call per term through Pydantic AI, structured output of `{svg, name, tags}`,
  with a system prompt that enforces a 24-unit viewBox, stroke-based Lucide-like style, and
  at most three shapes.
- Returns a single candidate as a base64 data URI. Caches it in `~/.reifire/llm_icons/` keyed
  by a hash of the lowercased term only.
- No validation that the SVG parses or renders, no record of the model or prompt version, no
  cost accounting, and no local-model path (Pydantic AI can target an OpenAI-compatible local
  server, but nothing in the provider or docs exercises that).

It is a reasonable first probe. It is not an instrument for finding out whether generation works.

Outside the repo, two threads of manual experimentation were run in October 2026 and are
summarized in the next section: image diffusion through Draw Things, and native SVG
generation with IconShop.

## 3. What the October 2026 experiments taught us

These are observations from a few dozen manual runs, not measurements. They are recorded
here so the first experiments test them rather than rediscover them.

**Image diffusion, then trace.** Models tried in Draw Things on a Mac: Stable Diffusion 1.5
with a "pictogram" checkpoint, SDXL Turbo, and FLUX.2 Klein 4B.

- FLUX produced usable monochrome pictograms for simple scenes. "Person climbing a ladder"
  came back with a figure in a genuine climbing pose, hands on rungs, clean parallel rails.
  A late lighthouse run was clean enough to ship.
- Failures split into two kinds. Semantic drift, when the prompt was stuffed with SVG
  requirements the image model cannot act on (viewBox sizes, stroke widths) and the model
  responded with an illustration instead of a pictogram. Raster artifacts: background
  speckle in silhouettes, a window frame invented around a lighthouse, the usual diffusion
  anatomy errors on figures.
- Tracing was done with VTracer at 1024 pixels and produced a 9 KB SVG for the lighthouse
  that included the background rectangle and thousands of control points. That is a cleanup
  pipeline problem, not a generation problem: threshold, remove small components, trace
  with Potrace, simplify, normalize the viewBox.
- Latency on the Mac: roughly 60 to 90 seconds per FLUX image, about 30 for SDXL Turbo.
  Best-of-four is therefore around five minutes per term. Fine for a batch, not for a
  request.

**Native SVG generation.** IconShop's downloadable FIGR checkpoint, run on CPU, produced a
hit-or-miss set for its own demo prompts and lost most of the concept on compound prompts
("robot gardener", "underwater library"). The repository states the checkpoint is not the
paper's model, so this characterizes one old checkpoint, not the approach. OmniSVG 1.1
(4B and 8B, Apache 2.0, December 2025) is the current open-weight model of this kind and has
not been tried. Its inference code is CUDA-oriented.

**LLM writes SVG directly.** A local Qwen model asked for a dog produced valid SVG describing
a bad dog. Hosted models do better on single concrete nouns and worse as the concept gets
compositional. No systematic run has been done; this is the cheapest route to measure and
the existing provider already implements it.

**Composition of library icons** was proposed and rejected. It works for object-plus-modifier
concepts (locked folder, cloud with a warning badge) and fails for agent-action-object
concepts, where the pose of the figure encodes the verb. A standing figure pasted onto a
ladder is not climbing. We expect most of what retrieval misses to be in the second
class; E1 measures that.

**Evolutionary search over SVG with an LLM mutator and a model judge** was examined as a
research direction. The conclusion was that the judge is the bottleneck: no local evaluator
has been shown to agree with human recognition of icons at small sizes, and a search driven
by a misaligned judge converges on what the judge likes. This is parked (section 10), with
the specific result that would unpark it.

## 4. What blocks exploration in the current code

The provider system was built for retrieval and has assumptions that make generation hard
to study. Each of these is a defect for the purpose of this plan, not a preference.

1. **The chain stops at the first non-empty result.** `ProviderChain.search` returns the
   first provider's results, and the bundled matcher's fourth tier is a substring match on
   tags. So "sit" matches something, retrieval "succeeds", and generation never runs. There
   is no relevance score, so the chain cannot tell a good match from a junk one, and no way
   to ask for candidates from several providers at once in the main path.
2. **One candidate, no choice, no memory of rejection.** Every provider returns results and
   the first one is used. There is no place for a person to pick among candidates, and a
   rejected candidate leaves no trace. For exploration, the rejections are half the data.
3. **No provenance.** A generated icon does not record the backend, model, prompt version,
   seed, latency or cost that produced it. The cache key is the term alone, so changing the
   model or the style prompt silently serves stale icons.
4. **No validation.** A generated SVG is wrapped in a data URI without being parsed,
   rendered, bounds-checked, or checked against the style rules the prompt asked for.
5. **No spend control.** Service backends can be called without a cap or a ledger. Tests
   that touch the LLM provider would spend money if the package were installed with
   credentials present.
6. **No local backend, no raster backend.** The only generator is a hosted LLM writing SVG.
   Diffusion models return rasters and need a shared post-processing pipeline that does not
   exist in the repo.
7. **Synchronous, per-term interface.** Generation takes seconds to minutes. The chain is
   called once per keyword inside `reify()`, so a prompt with eight keywords and a diffusion
   backend would block for forty minutes.
8. **Style is implicit.** Bundled icons are 24-unit Lucide-style strokes. The LLM prompt
   asks for the same. A diffusion pictogram is a filled silhouette. Nothing names the target
   style as data, so candidates from different routes cannot be normalized or compared.

## 5. Principles for the exploration

1. **Generation is a provider, not a special case.** A generator implements the same
   `IconProvider` protocol as the bundled set. What differs is exposed as data on the
   result (kind, provenance, score, cost), not as a different call path. `reify()` does
   not know or care which route produced an icon.
2. **Backends are configuration.** Each generator provider is parameterized by a backend
   object: an Ollama or LM Studio endpoint, a hosted LLM, Draw Things, Replicate. Swapping
   local for service is a constructor argument or an environment variable, never a code
   change. The experiment harness runs the same terms through several backends by looping
   over configurations.
3. **Record everything, especially rejections.** Every candidate produced during an
   experiment is written to disk with full provenance before anyone looks at it. Acceptance
   and rejection are appended to the same record. The analysis is a query over these files.
4. **A person reviews until a judge earns the right not to.** Candidate selection is
   manual, through a gallery, and the picks are stored. Any future automatic judge is
   evaluated against this pick history before it is allowed to select on its own.
5. **Style is explicit data.** An `IconStyle` object (viewBox, stroke or fill, stroke
   width, line caps, allowed elements) is passed to every generator and checked by the
   validator. The default matches the bundled Lucide family so generated icons sit beside
   retrieved ones without looking foreign.
6. **Raster routes share one deterministic cleanup.** Any backend that returns pixels goes
   through the same threshold, despeckle, trace, simplify and normalize pipeline. Tracing
   quality is a property of the pipeline, not of the model, and it is tested on fixtures.
7. **Service calls are capped and metered.** Every service backend runs under a spend cap
   checked before the call and writes to a cost ledger after it. A backend with no known
   price raises rather than being assumed free. Tests never call a paid service; integration
   tests are marked and gated on an explicit environment variable.
8. **Retrieval is improved before generation is trusted.** Every term that retrieval can
   cover well is a term generation never has to handle. Expanding and scoring retrieval is
   experiment one, and its result sizes the problem generation has to solve.

## 6. Architecture changes

All paths are under `src/reifire/visualization/providers/` unless noted. Nothing here
preserves the current result shape; the project is pre-production and the shape is wrong
for the purpose.

### 6.1 Result record

Every provider returns a list of `IconCandidate` records (a dataclass, serializable to
the existing dict shape for the visualization layer):

| Field | Meaning |
|---|---|
| `id`, `name`, `source`, `tags` | As today. |
| `kind` | `retrieved` or `generated`. |
| `svg` | Raw SVG markup when the icon is vector; the data URI is derived, not stored. |
| `image` | Data URI or path, for the HTML renderer. |
| `score` | Provider's own relevance estimate in [0, 1]. Retrieval tiers map to fixed scores; generated candidates start at `None` until reviewed. |
| `style` | The `IconStyle` the candidate conforms to, after validation. |
| `provenance` | Backend name, model id, prompt template version, seed, parameters, latency in seconds, cost in USD, timestamp. Empty for bundled icons. |
| `review` | `None`, `accepted` or `rejected`, plus reviewer and time. Written by the review tool, never by providers. |

### 6.2 Chain resolution

`ProviderChain` gains a `resolve(term, *, strategy, limit)` method and keeps `search` as
the `first` strategy for callers that want the old behaviour.

- `first`: stop at the first provider with results. Current behaviour.
- `all`: collect candidates from every available provider, sort by score. Used by the
  experiment harness.
- `threshold`: walk providers in priority order and stop as soon as a candidate scores at
  or above a configurable confidence. Generation providers get consulted only when
  retrieval scores low. This is the intended production strategy.

The bundled matcher's tiers become scores: exact 1.0, word 0.8, plural 0.7, substring 0.3.
Nothing else about matching changes in this plan; an embedding-based matcher is an
experiment (E1), not a rewrite.

### 6.3 Generation package

New package `generated/`:

- `style.py`: `IconStyle` dataclass: viewBox, stroke or fill rules, stroke width, line
  caps, allowed elements, and the list of render sizes the validator checks. Two presets,
  `LINE` (Lucide-compatible) and `GLYPH` (filled silhouette, for pictogram-style diffusion
  output). The default preset and the render sizes are read from configuration; the
  initial defaults are `LINE` at 24 and 32 pixels, chosen to match the bundled set and to
  keep development runs small. Larger sizes are added to the list when the reified view
  needs them.
- `backends/base.py`: two small protocols. `TextToSVGBackend.generate(term, style, n,
  seed) -> list[SVGResult]` and `TextToRasterBackend.generate(term, style, n, seed) ->
  list[RasterResult]`. Each result carries the provenance fields.
- `backends/llm.py`: wraps Pydantic AI. One class, configured with a model string. Covers
  hosted Anthropic and OpenAI models and any OpenAI-compatible local server (Ollama, LM
  Studio). Replaces the agent setup currently inside `LLMSVGProvider`.
- `backends/drawthings.py`: Draw Things exposes an HTTP API compatible with the
  AUTOMATIC1111 `txt2img` endpoint when its API server is enabled. Local raster backend
  for the Mac.
- `backends/replicate.py`: hosted raster and vector models, Recraft V3 SVG first.
- `backends/omnisvg.py`: deferred until E5 decides whether it runs on this hardware.
- `postprocess.py`: raster to SVG. Threshold to binary, drop connected components below a
  size, trace with Potrace, simplify, fit to the style's viewBox. Pure functions over
  bytes, tested on fixture images.
- `validate.py`: parse the SVG, reject disallowed elements, render at each of the style's
  configured sizes, check that the drawing covers a sane fraction of the viewBox, check
  stroke and fill rules against the style. Returns a normalized SVG or a reason.
- `provider.py`: `GeneratedIconProvider(backend, style, n, cache)`. Implements
  `IconProvider`. Calls the backend, runs post-processing for raster backends, validates,
  caches by a key of (term, backend id, model, style id, prompt version), returns
  candidates. Replaces `llm_svg.py`.
- `spend.py`: `SpendCap` with a per-run and per-day limit, and a JSONL ledger at
  `~/.reifire/spend.jsonl`. Every service backend takes one. A price table lives next to
  the backends; a backend without an entry raises at construction.

### 6.4 Experiment harness

New top-level package `src/reifire/experiments/` with a console script `reifire-icons`:

- `run --terms FILE --backend NAME [--backend NAME ...] --n 4 --style line --out DIR`:
  resolves every term with every backend, writes one JSONL line per candidate under
  `DIR/candidates.jsonl` and the SVG or PNG beside it, and renders `DIR/gallery.html`.
- `review DIR`: serves the gallery on localhost with accept and reject buttons per
  candidate. Picks are appended to `DIR/reviews.jsonl`. An accepted candidate can be
  pinned into the per-user icon registry so `reify()` uses it from then on.
- `export DIR --to SET`: copies accepted candidates, with their provenance, into a named
  icon set under the package's bundled icons directory and regenerates that set's
  manifest. Generated sets sit beside `lucide/` and `octicons/` and are served by the same
  `BundledIconProvider`. This is how accepted icons become part of the project rather than
  one machine's cache.
- `report DIR [DIR ...]`: coverage, acceptance rate, latency and cost per backend and per
  term bucket, as a Markdown table.

The gallery reuses the existing HTML renderer where it can. The review server is a few
dozen lines of the standard library; it does not need a framework.

### 6.5 Project layout for experiment data

```
experiments/icons/
  terms.json            # the corpus, versioned, committed
  runs/<run-id>/        # candidates.jsonl, reviews.jsonl, gallery.html, SVG/PNG files
  reports/<run-id>.md   # committed summaries; runs/ is gitignored except reports
src/reifire/visualization/providers/icons/
  lucide/  octicons/    # curated retrieval sets, as today
  generated/<set>/      # accepted generated icons exported from reviews, with provenance
  manifest.json         # covers every set; records license and origin per set
```

Terms are extracted from the example prompts in `examples/*.json` plus a curated list,
each tagged with a bucket: `concrete-noun`, `verb`, `abstract`, `multiword`, `domain`.
Around 150 terms to start. The corpus is a fixture: every experiment runs against the same
list so results compare, and the run record names the corpus version it used.

### 6.6 Async and batching

`reify()` stays synchronous and uses the `threshold` strategy with generation providers
present only when configured. Batch generation is the harness's job. An async chain is
not needed until a UI wants progressive results, and that is outside this plan.

## 7. Experiment sequence

Each experiment has a question, a cost line, and a decision it feeds. They run in order
because each one sizes the next. Costs are per run on the 150-term corpus.

### E0: Baseline coverage

- **Question**: with the current bundled set and the `threshold` strategy, what fraction
  of the corpus gets an acceptable icon, and how often does the substring tier return junk?
- **Runs**: bundled provider only, `all` strategy, limit 3. Reviewed through the gallery.
- **Cost**: no model calls. Half a day including the review.
- **Decides**: the real size of the tail, by bucket. Also calibrates the threshold score.

### E1: Retrieval expansion

- **Question**: how much of the tail closes if retrieval is wider and smarter?
- **Runs**: add an Iconify-backed provider over three or four larger monochrome sets
  (Tabler, Phosphor, Material Symbols, and a pictogram set such as Health Icons) with the
  existing tag matcher; then the same with a local sentence-embedding matcher over tags.
  Iconify aggregates about 300,000 icons across 200 sets, so this is a licensing and
  curation choice, not a search for data.
- **Cost**: no paid calls. Local embedding model, a few hundred megabytes. Two days.
- **Decides**: whether generation is needed for a quarter of terms or for a twentieth.
  Also whether embedding retrieval is worth keeping as the default matcher.

### E2: LLM writes SVG, hosted versus local

- **Question**: for the terms that still miss after E1, how often does an LLM produce an
  acceptable line-style icon in four tries, and does a local coder model get close to a
  hosted one?
- **Runs**: `GeneratedIconProvider` with the LLM backend, n=4, `LINE` style. Backends:
  one small hosted model and one mid-sized hosted model; Qwen2.5-Coder 14B or similar via
  Ollama. Every candidate validated and rendered before review.
- **Cost**: about 60 terms × 4 candidates × 2 hosted models, under a few dollars. Cap at
  $10. Local run is free and takes a couple of hours.
- **Decides**: whether direct LLM generation covers concrete nouns and simple verbs, which
  is the expectation, and whether local is good enough to be the default for them.

### E3: Local diffusion plus trace

- **Question**: does FLUX through Draw Things, with the shared cleanup pipeline and a
  `GLYPH` style, produce acceptable pictograms for the action and abstract terms E2 fails?
- **Runs**: Draw Things backend, n=4, fixed pictogram prompt template, overnight batch.
- **Cost**: no paid calls. About five minutes per term, so a night for sixty terms.
- **Decides**: whether the raster route earns a place for the hard buckets, and whether
  mixing `GLYPH` icons with `LINE` icons is visually acceptable in the reified view, or
  whether a glyph-to-line normalization is needed.

### E4: Hosted vector generation

- **Question**: what is the ceiling? On the terms that E2 and E3 both miss, does a hosted
  vector model succeed?
- **Runs**: Recraft V3 SVG through Replicate, n=2, on the residue only.
- **Cost**: about $0.25 per image. Residue of 30 terms × 2 is $15. Cap at $25.
- **Decides**: whether a paid tail is worth offering as an opt-in provider, and how far
  local routes are from the best available.

### E5: Native local SVG model (conditional)

- **Question**: does OmniSVG 1.1 4B run on this hardware, and if so, does it beat E2's
  local LLM on the same terms?
- **Runs**: time-boxed to one day of setup. If it does not run on Metal, stop and record
  that.
- **Cost**: no paid calls. Weights are about 8 GB.
- **Decides**: whether a native SVG model belongs in the backend list at all.

After E4 the data supports a decision about the default provider chain for `reify()`:
which routes are on by default, which are opt-in, and which are dropped.

## 8. Features required, in build order

Build order follows experiment order. Each item lists the experiment that first needs it.
Every item ships with unit tests using fake backends; nothing in `tests/` calls a model.

| # | Feature | Needed by | Notes |
|---|---|---|---|
| 1 | `IconCandidate` record with `kind`, `score`, `provenance`, `review` | E0 | Replaces the result dict. Visualization layer reads the same keys as today. |
| 2 | Scored bundled matcher | E0 | Tier to score mapping; substring tier scored low. |
| 3 | `ProviderChain.resolve` with `first`, `all`, `threshold` | E0 | `reify()` moves to `threshold`. |
| 4 | Term corpus fixture with buckets | E0 | `experiments/icons/terms.json`. |
| 5 | `reifire-icons run` and `report` | E0 | Candidates to JSONL, gallery HTML, summary tables. |
| 6 | `reifire-icons review` with picks to JSONL and pin-to-registry | E0 | Local server, standard library only. |
| 7 | `reifire-icons export` to a generated bundled set with provenance in the manifest | E0 | Accepted icons become part of the package, not a per-user cache. |
| 8 | Iconify-backed provider with set curation script | E1 | Extends `scripts/curate_icons.py`; license per set recorded in the manifest. |
| 9 | Embedding matcher (optional dependency) | E1 | Behind an extra; falls back to tag matching when absent. |
| 10 | `IconStyle` and `validate.py` with render check | E2 | Rendering via a small rasterizer dependency; fixtures for pass and fail cases. |
| 11 | LLM backend covering hosted and OpenAI-compatible local servers | E2 | Replaces the agent code in `llm_svg.py`. |
| 12 | `SpendCap`, ledger, price table | E2 | Construction fails for unpriced service backends. |
| 13 | `GeneratedIconProvider` with provenance-keyed cache | E2 | Removes `llm_svg.py`. |
| 14 | `postprocess.py` raster to SVG | E3 | Potrace as a subprocess or binding; fixture PNGs from the October runs. |
| 15 | Draw Things backend | E3 | Probe the real endpoint first and record what it returns. |
| 16 | Replicate backend | E4 | Priced; under the cap. |
| 17 | OmniSVG backend | E5 | Only if E5's setup day succeeds. |

Documentation lands with each item: the provider docs page gains a "Generated icons"
section when item 13 lands, and the README's provider list is updated at the same time.

## 9. Decision criteria

These are the measures the harness reports. The targets are starting hypotheses, written
down so the first run can prove them wrong. They are not commitments.

| Measure | Definition | Starting target |
|---|---|---|
| Coverage | Fraction of corpus terms with at least one accepted icon from any route. | 90% after E3, by route mix. |
| Acceptance rate | Accepted candidates divided by candidates produced, per backend and bucket. | Above 25% for a route to stay in the default chain; above 10% to stay as opt-in. |
| Junk rate | Retrieved candidates that a reviewer rejects as unrelated. | Under 5% for the `threshold` strategy. |
| Time to accept | Wall-clock from request to the first accepted candidate, per backend. | Under 10 seconds for the default chain; batch routes reported but not gated. |
| Cost per accepted icon | Ledger spend divided by accepted icons, service backends only. | Under $0.05 for a default route; under $0.50 for an opt-in tail route. |
| Style conformance | Candidates passing `validate.py` without normalization. | Above 80% for LLM routes; reported for raster routes. |

A route is "on by default" when it clears acceptance, junk, time and cost together. A
route that clears acceptance but not time or cost is opt-in. A route below the opt-in
floor is dropped from the backend list and the reason is recorded here.

## 10. Parked ideas and why

Each of these was considered and set aside. The trigger says what would bring it back.

**Evolutionary search over SVG (LLM mutator, model judge).** A legitimate research
program, and one with close prior art: Feedback Descent, IntroSVG, Mind Evolution, and
2021 work evolving shapes against CLIP that produced textures rather than icons. The
bottleneck is the judge. No local evaluator has been shown to agree with human recognition
of icons at 16 to 32 pixels, and a search driven by a misaligned judge converges on what
the judge rewards. Trigger: the review data from E2 to E4 gives a few hundred human
accept and reject decisions; if a local vision model's blind-recognition score agrees with
those decisions at a usable rate, a judge exists and a search loop becomes worth building.

**Composition of library icons.** Works for object-plus-modifier concepts and fails for
agent-action-object concepts, which we expect to be most of the tail. Trigger: E1's
bucket analysis shows the tail is mostly modifiers after all.

**Rigged pictogram figure.** A parametric human with joint angles and attachment points,
objects with contact points, an LLM choosing a pose. This is the correct solution for the
"person doing X with Y" class and a substantial build. Trigger: E3 and E4 both fail that
class and it matters enough to Reifire's users to justify weeks of work.

**Fine-tuning a diffusion model on an icon set.** The Modal Heroicons experiment showed
style consistency improves and structural errors do not. Trigger: E3 shows that FLUX's
failures are stylistic rather than structural, which the October runs suggest is not the
case.

**Automatic selection in `reify()`.** Same trigger as the judge above.

## 11. Risks

- **Style inconsistency across routes.** A glyph beside a line icon looks wrong. E3
  reports it; the fallback is a glyph-to-line normalization pass or confining raster
  routes to a separate style family that the visualization renders consistently.
- **Local setup friction.** Draw Things, Ollama and OmniSVG each have their own install
  story, and OmniSVG assumes CUDA. Each backend's docs page must carry a tested setup
  procedure for the Mac, and an unavailable backend must report itself as unavailable
  rather than fail inside the chain.
- **The review burden.** Every experiment ends with someone looking at several hundred
  candidates. The gallery has to make that fast: keyboard accept and reject, one row per
  term, candidates side by side at the configured render sizes.
- **Licensing.** Iconify sets carry different licenses; a few forbid redistribution in
  derived works. Each curated set's license is recorded in the manifest and surfaced in
  the candidate's attribution. Hosted generation services have their own terms for output
  ownership; the provider docs state them.
- **Drift in the corpus.** If the term list changes between experiments the results stop
  comparing. The corpus is versioned and a run records which version it used.
- **Scope creep toward the research program.** The harness is a measuring instrument. If
  it starts growing search loops or judges before E4's data exists, that is the parked
  item escaping. The trigger in section 10 is the gate.
