# Installation

FastBrain needs Python 3.10 or newer and runs on Linux, macOS and Windows.

## Pick what you need

The core install is small: `pydantic`, `httpx`, `rich` and `typer`. Everything
that brings in heavy dependencies is an extra.

| You want | Install | Pulls in |
|---|---|---|
| Rules, tracing, the CLI, Jev or any System One server | `pip install fastbrain` | nothing heavy |
| Hosted LLMs through OpenRouter, OpenAI, Ollama or vLLM | `pip install "fastbrain[openai]"` | `openai` |
| Claude through the Anthropic SDK | `pip install "fastbrain[anthropic]"` | `anthropic` |
| GLiNER 2.5 | `pip install "fastbrain[gliner]"` | `gliner2`, `transformers<5`, `torch` |
| Laya | `pip install "fastbrain[laya]"` | `laya`, `transformers<5`, `torch` |
| A local LLM or any Hugging Face classifier | `pip install "fastbrain[local-llm]"` | `transformers<5`, `accelerate`, `torch` |
| All local models | `pip install "fastbrain[local]"` | the three above |
| OpenTelemetry export | `pip install "fastbrain[otel]"` | `opentelemetry-sdk` and the OTLP exporter |
| The public dataset benchmarks | `pip install "fastbrain[bench]"` | `datasets` |
| The LangGraph adapter | `pip install "fastbrain[langgraph]"` | `langgraph` |
| The OpenAI Agents SDK adapter | `pip install "fastbrain[openai-agents]"` | `openai-agents` |
| The decision server (`fastbrain serve`) | `pip install "fastbrain[server]"` | `fastapi`, `uvicorn` |
| MCP tools (`fastbrain mcp`) | `pip install "fastbrain[mcp]"` | `mcp` |
| Everything | `pip install "fastbrain[all]"` | all of the above |

Extras combine: `pip install "fastbrain[gliner,laya,openai]"`.

## Local models: install PyTorch first

pip cannot choose the right PyTorch build for your GPU, so the local extras
take whatever `torch` it finds, and on Windows and macOS that is the CPU build.
Everything still works, only slower. For a GPU, install PyTorch first from
its own index, then FastBrain:

**NVIDIA GPU (Linux or Windows).** CUDA 13.0 wheels cover current cards,
including the RTX 50 series:

```bash
pip install torch --index-url https://download.pytorch.org/whl/cu130
pip install "fastbrain[local]"
```

For older drivers, pick the matching CUDA version on
[pytorch.org](https://pytorch.org/get-started/locally/).

**Apple Silicon.** The default PyPI build includes Metal (MPS) support:

```bash
pip install "fastbrain[local]"
```

**CPU only.**

```bash
pip install torch --index-url https://download.pytorch.org/whl/cpu
pip install "fastbrain[local]"
```

Then check what you got:

```bash
fastbrain doctor
```

`doctor` prints the accelerator torch can see. If an NVIDIA GPU is present but
torch is a CPU build, it says so and prints the command to fix it.

## Conda

`environment.yml` creates an environment with everything, including the CUDA
13.0 build of PyTorch:

```bash
conda env create -f environment.yml
conda activate fastbrain
```

It installs FastBrain from the checkout in editable mode, for development. To
use the released package in a conda environment, create the environment with
Python 3.12, install PyTorch as above, then `pip install "fastbrain[local]"`.

## Where files go

| What | Where | Change it with |
|---|---|---|
| Model weights | the Hugging Face cache, `~/.cache/huggingface` | `HF_HOME` |
| Banking77 test file for the benchmarks | `~/.cache/fastbrain/datasets` | |
| Traces written by the CLI | `./.fastbrain/traces` | `FASTBRAIN_TRACE_DIR` |
| Shadow logs | wherever `Shadow(log=...)` points | |
| Benchmark output | `./.fastbrain/bench/<run>` | `--out` |
| API keys | environment variables, or `./.env` for the CLI | |

Models download on first use: about 0.8 GB for GLiNER base, 0.9 GB for Laya
and 3.4 GB for Qwen3-1.7B. `fastbrain doctor` shows which ones are already
cached.

## Offline and air-gapped machines

Download the weights once on a connected machine (running `fastbrain demo`
does it), copy the Hugging Face cache directory, and set `HF_HUB_OFFLINE=1` on
the offline machine. Providers also accept a local directory in place of a
model id, for example `GLiNER("/models/gliner2.5-base-v1")`.

## Windows notes

- On Windows, FastBrain downloads models one file at a time. That avoids a
  race in the Hugging Face cache's symlink handling (`WinError 1314`).
  Enabling Developer Mode lets the cache use symlinks and saves disk space.
- If a console shows garbled characters in tables, use Windows Terminal or
  set `PYTHONIOENCODING=utf-8`.

## Checking an install

```bash
fastbrain --version
fastbrain doctor
python -c "import fastbrain; print(fastbrain.__version__)"
```

A run that needs no downloads, for a quick end-to-end check:

```bash
python -m fastbrain demo --help
```
