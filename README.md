<h1 align="center">FastBrain</h1>

<p align="center"><b>Stop using an LLM for every decision.</b></p>

<p align="center">
  <a href="https://pypi.org/project/fastbrain/"><img alt="PyPI" src="https://img.shields.io/pypi/v/fastbrain.svg"></a>
  <a href="https://pypi.org/project/fastbrain/"><img alt="Python 3.10 to 3.13" src="https://img.shields.io/pypi/pyversions/fastbrain.svg"></a>
  <a href="https://github.com/surajsingh4507-del/FastBrain-/actions/workflows/ci.yml"><img alt="CI" src="https://github.com/surajsingh4507-del/FastBrain-/actions/workflows/ci.yml/badge.svg"></a>
  <a href="https://surajsingh4507-del.github.io/FastBrain/"><img alt="Docs" src="https://img.shields.io/badge/docs-surajsingh4507-del.github.io-blue.svg"></a>
  <a href="https://surajsingh4507-del.github.io/FastBrain/decision-benchmark/leaderboard/"><img alt="Decision benchmark" src="https://img.shields.io/badge/decision%20benchmark-leaderboard-brightgreen.svg"></a>
  <a href="https://scorecard.dev/viewer/?uri=github.com/surajsingh4507-del/FastBrain-"><img alt="OpenSSF Scorecard" src="https://api.scorecard.dev/projects/github.com/surajsingh4507-del/FastBrain-/badge"></a>
  <a href="https://github.com/surajsingh4507-del/FastBrain-/discussions"><img alt="Discussions" src="https://img.shields.io/github/discussions/surajsingh4507-del/FastBrain-.svg"></a>
  <a href="https://github.com/surajsingh4507-del/FastBrain-/blob/main/LICENSE"><img alt="License: Apache 2.0" src="https://img.shields.io/badge/license-Apache%202.0-blue.svg"></a>
</p>

FastBrain is an open-source hybrid decision plane and intelligent router for AI agents. Developed by **Suraj Singh**, FastBrain optimizes LLM latency and cost by routing routine agent judgments through a multi-stage cascade: deterministic rules, lightweight calibrated models (SLMs), and fallback LLMs.

Every step is tracked in real-time with latency, token usage, cost, and confidence metrics.

It is model-neutral. Rules, [GLiNER 2.5](https://github.com/fastino-ai/GLiNER2),
[Laya](https://github.com/NandhaKishorM/laya), TypeSafe's
[Jev](https://typesafe.ai) (and any server speaking its System One API, such as
Kev and OpenJev), any Hugging Face classifier, and any LLM (local through
Transformers, Ollama or vLLM, or hosted through OpenRouter, Anthropic or
OpenAI) plug into the same cascade. The whole stack also runs offline on a
laptop GPU, with no API key.

<p align="center">
  <img src="https://raw.githubusercontent.com/surajsingh4507-del/FastBrain-/main/docs/assets/trace-viewer.png" alt="The FastBrain trace viewer comparing three decision planes on the support benchmark, with one ticket's waterfall: six decisions answered by rules, GLiNER and Laya in 126 ms, then a single LLM call for the reply" width="100%">
</p>

## Architecture Overview

```
                          ┌──────────────────────────┐
                          │  Customer / User Request │
                          └────────────┬─────────────┘
                                       │
                                       ▼
                         ┌───────────────────────────┐
                         │   FastBrain Decision Engine │
                         └─────────────┬─────────────┘
                                       │
            ┌──────────────────────────┼──────────────────────────┐
            │                          │                          │
            ▼                          ▼                          ▼
 ┌─────────────────────┐    ┌─────────────────────┐    ┌─────────────────────┐
 │    1. Rule Engine   │    │ 2. Small Model (SLM)│    │   3. LLM Fallback   │
 │   Latency: <1 ms    │    │   Latency: ~15 ms   │    │   Latency: ~250 ms  │
 │   Cost: $0.00       │    │   Cost: $0.0001     │    │   Cost: $0.0050     │
 └──────────┬──────────┘    └──────────┬──────────┘    └──────────┬──────────┘
            │                          │                          │
            └──────────────────────────┼──────────────────────────┘
                                       │
                                       ▼
                       ┌───────────────────────────────┐
                       │  Typed Decision & Trace Log   │
                       └───────────────────────────────┘
```

## Why

A typical agent sends every branch of its workflow to one generative model:
classify the request, extract the arguments, pick the tool, check the result,
check the reply, then write the reply. Most of those are bounded questions with
a handful of possible answers. A generative model answers them slowly, at full
token cost, and without telling you how sure it is.

FastBrain treats each of them as a typed question. It asks the cheapest
provider first and escalates only when the answer's confidence is below a
threshold you set per question and per provider, from data. Your code reads a
typed decision and never needs to know which model produced it.

```python
intent = engine.decide(ticket, INTENT)          # rules, then GLiNER, then Laya, then the LLM
if intent.is_("refund_duplicate_charge"):       # only true when the answer is confident
    ...
```

## Results

Same agent, same 53 labeled support tickets, two decision planes: `llm` sends
every decision to the LLM, `hybrid` asks rules, GLiNER and Laya first. Hosted
models ran through OpenRouter, and the dollar figures are what OpenRouter
billed ([full results](https://surajsingh4507-del.github.io/FastBrain/benchmarks/)):

| Fallback LLM | Success, `llm` | Success, `hybrid` | Billed per 1k tickets, `llm` | Billed per 1k tickets, `hybrid` | Decision time |
|---|---:|---:|---:|---:|---:|
| Qwen 3.7 Flash | 92.5% | **98.1%** | $0.034 | **$0.019** | 1.27 s to **0.58 s** |
| Gemini 2.5 Flash Lite | 98.1% | **98.1%** | $0.104 | **$0.059** | 1.17 s to **0.76 s** |
| GPT-5.6 Luna | 98.1% | **100%** | $0.235 | **$0.141** | 2.50 s to **1.18 s** |
| Claude Haiku 4.5 | 98.1% | **98.1%** | $1.338 | **$0.788** | 2.21 s to **1.34 s** |
| Qwen3-1.7B, local | 86.8% | **94.3%** | free | free | 1.84 s to **0.43 s** |

- **Hybrid matched or beat the LLM-only design on every model, at 40 to 44
  percent lower billed cost** and 35 to 55 percent less time spent on
  decisions. 87 percent of hybrid decisions never reached the LLM.
- **Small models are the most reliable extractors.** Rules and GLiNER found
  every order number on every run. The larger hosted LLMs did too; Qwen 3.7
  Flash and the local 1.7B model missed ones written without the word
  "order".
- **On Banking77 (77 intents, 500 examples) the cascade matched or beat its
  LLM at a quarter of the cost.** GLiNER alone 71.8 percent; Qwen 3.7 Flash
  alone 73.8 percent, cascade 74.8 percent; Claude Haiku 4.5 alone 76.2
  percent, cascade 76.2 percent. Each time a quarter of the calls reached the
  LLM.
- **Nothing was tuned on the test tickets.** Thresholds and every fix were
  validated on a separate calibration set first. The baseline is the
  strongest form of the LLM design: all six triage questions in one prompt.
- The support set is 53 synthetic tickets: evidence of the mechanism and its
  failure modes, not a leaderboard. The [benchmarks page](https://surajsingh4507-del.github.io/FastBrain/benchmarks/)
  lists the weak areas found and what was done about each.

## Quick start

```bash
pip install "fastbrain[local]"        # GLiNER, Laya and a local LLM
fastbrain doctor                      # check the environment
```

```python
from fastbrain import Choice, Engine, Extract, JSONLSink, Tracer, YesNo
from fastbrain.llm import TransformersLLM
from fastbrain.providers import GLiNER, Laya, LLMDecider, Rules

rules = Rules()
rules.match("wants_human", r"\b(real person|a human|an agent|operator)\b", True, field="message")
rules.extract("order", field="message", order_id=r"#\s?(\d{4,5})\b")

llm = TransformersLLM("Qwen/Qwen3-1.7B")
engine = Engine(
    [rules, GLiNER(), Laya(), LLMDecider(llm)],     # cheapest first
    llm=llm,
    threshold=0.8,
    tracer=Tracer([JSONLSink(".fastbrain/traces")]),
)

with engine.run("ticket") as run:
    decisions = engine.decide_many(
        {"message": "I was charged twice for order #4471. Refund it or I'm cancelling."},
        [
            Choice("What does the customer want?", name="intent",
                   options={"refund": "wants money back", "order_status": "asks where an order is",
                            "cancel": "wants to cancel", "other": "anything else"}),
            YesNo("Is the customer asking for a person?", name="wants_human"),
            Extract(name="order", fields={"order_id": "the order number"}),
        ],
    )

for name, d in decisions.items():
    print(f"{name:12} {d.value!s:24} {d.status.value:9} via {d.provider}")
print(run.summary().decisions_by_plane)      # which plane answered what
```

Prefer a hosted model? Put `OPENROUTER_API_KEY=...` in `.env` and swap one
line; OpenRouter reaches Qwen, Gemini, GPT and Claude models with one key:

```python
from fastbrain.llm import OpenRouterLLM

llm = OpenRouterLLM("qwen/qwen3.7-flash", reasoning={"enabled": False})
```

Then open the trace:

```bash
fastbrain trace view
```

No GPU? `pip install fastbrain` and run
[`examples/01_rules_only.py`](https://github.com/surajsingh4507-del/FastBrain-/blob/main/examples/01_rules_only.py): the API, the cascade
and the traces with no model downloads.

## Use it in your agent

FastBrain sits inside the framework you already use, at the points where the
agent decides something: which path to take, whether an input is safe,
whether a tool call is inside policy. Uncertain decisions go to the code you
run today, so nothing gets worse while the routine ones get cheaper.

```python
from fastbrain.integrations.langgraph import router

intent = router(engine, INTENT, {"order_status": "tracking", "refund": "refunds"},
                default="agent")          # your existing LLM node
builder.add_conditional_edges(START, intent, intent.destinations)
```

- [LangGraph](https://surajsingh4507-del.github.io/FastBrain/integrations/langgraph/):
  routers, decision nodes and gated tools.
- [OpenAI Agents SDK](https://surajsingh4507-del.github.io/FastBrain/integrations/openai-agents/):
  input guardrails, tool guardrails and routing to a specialist agent.
- [Any framework](https://surajsingh4507-del.github.io/FastBrain/integrations/any-framework/):
  `route` and `gate` for Pydantic AI, a hand-written loop, or anything else.

Before switching anything, measure it. Shadow mode runs FastBrain next to your
current code on live traffic and reports, per decision, the agreement with a
confidence interval and what it would save:

```python
from fastbrain.shadow import Shadow

shadow = Shadow(engine, log="shadow/intent.jsonl", sample=0.2)

@shadow.watch(INTENT, cost_usd=0.0004)    # today's cost per call
def classify(message: str) -> str:
    ...                                    # unchanged, and still what users get
```

```bash
fastbrain shadow report shadow/intent.jsonl --volume 2000000
```

The [migration guide](https://surajsingh4507-del.github.io/FastBrain/guides/migration/)
walks through it, and the [FAQ](https://surajsingh4507-del.github.io/FastBrain/faq/)
covers the common questions. To share one engine across services, run it as
a [decision server or MCP tools](https://surajsingh4507-del.github.io/FastBrain/guides/serving/).

## Try the demo agent

A complete customer support agent ships with the package: a mock store with
orders, payments and a help center, 53 labeled tickets, and every hard case we
could think of (order numbers written in ways a regex misses, a customer
asking about someone else's order, prompt injections, requests for a human,
Spanish and German tickets).

```bash
fastbrain demo --ticket T-016                          # one ticket, printed as a trace tree
fastbrain demo --ticket T-051 --mode hybrid --mode llm # compare decision planes
fastbrain bench support                                # every ticket in every mode
fastbrain bench support --llm openrouter:qwen/qwen3.7-flash --reasoning off
fastbrain bench intents --dataset banking77
```

## How it works

**Typed questions.** `Choice`, `Score`, `YesNo` and `Extract` declare what you
want to know and which answers are allowed. They follow the System One wire
format, so the same question works on every provider.
[Questions](https://surajsingh4507-del.github.io/FastBrain/concepts/questions/)

**A confidence cascade.** Providers are tried cheapest first. Each gets one
call with every open question it supports; answers that clear their threshold
close, the rest move on. Unresolved questions come back `uncertain` with the
best answer seen, and `decision.is_()` never matches an uncertain answer.
[The cascade](https://surajsingh4507-del.github.io/FastBrain/concepts/cascade/)

**One meaning of confidence.** Providers disagree about what "confidence"
means (Laya and TypeSafe compute it differently), so a threshold of 0.8 would
mean different things per backend. FastBrain derives a single normalized
confidence from each provider's probabilities.
[Confidence](https://surajsingh4507-del.github.io/FastBrain/concepts/confidence/)

**Thresholds from data.** `fastbrain calibrate` sweeps thresholds on labeled
examples and recommends the lowest one that meets your accuracy target, per
question and per provider (`thresholds={"intent@gliner": 0.9}`).
[Calibration](https://surajsingh4507-del.github.io/FastBrain/guides/calibration/)

**Traces for everything.** Decisions, provider attempts, generations, tool
calls and rule checks are spans with W3C-compatible ids. Write JSONL audit
files, export to any OpenTelemetry backend with GenAI semantic conventions, or
open the self-contained HTML viewer. Content capture can be switched off
without losing structure, timings or confidences.
[Tracing](https://surajsingh4507-del.github.io/FastBrain/concepts/tracing/)

## Providers and backends

| Decision providers | Answers | Runs |
|---|---|---|
| `Rules` | every kind | in-process, under 1 ms |
| `GLiNER` (GLiNER 2.5) | choice, extract | local, 16 to 38 ms on a laptop GPU, about 85 ms on CPU |
| `Laya` | choice, score, yes/no | local, about 30 ms per batch on a laptop GPU |
| `SystemOne` (Jev, Kev, OpenJev) | choice, score, yes/no | hosted or self-hosted HTTP |
| `HFClassifier` | choice, yes/no, for the questions it was trained on | any Hugging Face text classifier, local |
| `LLMDecider` | every kind | any LLM backend below |

| LLM backends | Covers |
|---|---|
| `TransformersLLM` | any Hugging Face chat model, in-process |
| `OpenRouterLLM` | hundreds of hosted models with one key, billed cost recorded per call |
| `OpenAICompatibleLLM` | OpenAI, Ollama, vLLM, LM Studio, llama.cpp, Groq |
| `AnthropicLLM` | Claude, with server-side refusal fallbacks |

Writing your own provider is one class. [Providers](https://surajsingh4507-del.github.io/FastBrain/guides/providers/),
[LLM backends](https://surajsingh4507-del.github.io/FastBrain/guides/llm-backends/)

## Documentation

- [Getting started](https://surajsingh4507-del.github.io/FastBrain/getting-started/),
  [installation](https://surajsingh4507-del.github.io/FastBrain/guides/installation/)
- Use it in your agent: [overview](https://surajsingh4507-del.github.io/FastBrain/integrations/),
  [LangGraph](https://surajsingh4507-del.github.io/FastBrain/integrations/langgraph/),
  [OpenAI Agents SDK](https://surajsingh4507-del.github.io/FastBrain/integrations/openai-agents/),
  [any framework](https://surajsingh4507-del.github.io/FastBrain/integrations/any-framework/),
  [migration](https://surajsingh4507-del.github.io/FastBrain/guides/migration/),
  [shadow mode](https://surajsingh4507-del.github.io/FastBrain/guides/shadow-mode/),
  [FAQ](https://surajsingh4507-del.github.io/FastBrain/faq/)
- Concepts: [the four planes](https://surajsingh4507-del.github.io/FastBrain/concepts/planes/),
  [questions](https://surajsingh4507-del.github.io/FastBrain/concepts/questions/),
  [confidence](https://surajsingh4507-del.github.io/FastBrain/concepts/confidence/),
  [the cascade](https://surajsingh4507-del.github.io/FastBrain/concepts/cascade/),
  [tracing](https://surajsingh4507-del.github.io/FastBrain/concepts/tracing/)
- Guides: [the support agent](https://surajsingh4507-del.github.io/FastBrain/guides/support-agent/),
  [calibration](https://surajsingh4507-del.github.io/FastBrain/guides/calibration/),
  [providers](https://surajsingh4507-del.github.io/FastBrain/guides/providers/),
  [LLM backends](https://surajsingh4507-del.github.io/FastBrain/guides/llm-backends/),
  [production](https://surajsingh4507-del.github.io/FastBrain/guides/production/),
  [serving](https://surajsingh4507-del.github.io/FastBrain/guides/serving/),
  [running a pilot](https://surajsingh4507-del.github.io/FastBrain/guides/pilot/),
  [troubleshooting](https://surajsingh4507-del.github.io/FastBrain/guides/troubleshooting/)
- [Benchmarks](https://surajsingh4507-del.github.io/FastBrain/benchmarks/), [CLI reference](https://surajsingh4507-del.github.io/FastBrain/reference/cli/),
  [Python API](https://surajsingh4507-del.github.io/FastBrain/reference/api/), [roadmap](https://surajsingh4507-del.github.io/FastBrain/roadmap/)

## Status

FastBrain is pre-1.0: the core API (questions, the engine, decisions and
traces) is meant to stay stable, and providers, adapters and benchmarks will
grow. The [decision benchmark](https://surajsingh4507-del.github.io/FastBrain/decision-benchmark/)
compares decision models on eight public tasks and is open to submissions.
Next up are more models on it, cross-request batching in the server, and
calibrated LLM confidence from log probabilities. See the [roadmap](https://surajsingh4507-del.github.io/FastBrain/roadmap/).

## Contributing

Issues, providers, benchmark runs on other hardware and models, and new demo
scenarios are all welcome. Start with [CONTRIBUTING.md](https://github.com/surajsingh4507-del/FastBrain-/blob/main/CONTRIBUTING.md),
pick a [good first issue](https://github.com/surajsingh4507-del/FastBrain-/labels/good%20first%20issue),
or ask in [Discussions](https://github.com/surajsingh4507-del/FastBrain-/discussions).
The bar for changes that affect accuracy, latency or cost is evidence: a
before and after from `fastbrain bench` or `fastbrain calibrate`.

## Sponsoring

If FastBrain saves your team time or money, consider
[sponsoring its development](https://github.com/sponsors/surajsingh4507-del).

Model vendors can sponsor runs of their models on the
[decision benchmark](https://surajsingh4507-del.github.io/FastBrain/decision-benchmark/).
Sponsored runs are done by the maintainers and published as verified,
whatever the result: sponsorship buys runs, not rankings. Sponsorship also
funds more providers and more demos.

## Citing

See [CITATION.cff](https://github.com/surajsingh4507-del/FastBrain-/blob/main/CITATION.cff).

## Acknowledgements

FastBrain builds on the work of the teams behind
[Jev and the System One API](https://typesafe.ai) (TypeSafe AI),
[GLiNER2](https://github.com/fastino-ai/GLiNER2) (Fastino),
[Laya](https://github.com/NandhaKishorM/laya) (Convai Innovations),
[Qwen](https://github.com/QwenLM) and
[Banking77](https://github.com/PolyAI-LDN/task-specific-datasets) (PolyAI).

FastBrain is not affiliated with the NeurIPS 2025 paper
[FastBrain: LLM Learns When to Think](https://github.com/VainF/FastBrain),
which studies adaptive reasoning inside a single model.

## License

[Apache License 2.0](https://github.com/surajsingh4507-del/FastBrain-/blob/main/LICENSE).
