# Python API

The public API is everything importable from `fastbrain`,
`fastbrain.providers`, `fastbrain.llm`, `fastbrain.tracing`,
`fastbrain.shadow`, `fastbrain.integrations` and `fastbrain.server`. Anything
with a leading underscore is internal and may change.

## Engine

::: fastbrain.Engine

::: fastbrain.Run

## Questions

::: fastbrain.Choice

::: fastbrain.Score

::: fastbrain.YesNo

::: fastbrain.Extract

::: fastbrain.questions.question_from_spec

## Results

::: fastbrain.Decision

::: fastbrain.Attempt

::: fastbrain.Status

::: fastbrain.Plane

## Limits

::: fastbrain.SpendLimit

::: fastbrain.SpendLimitError

## Shadow mode

::: fastbrain.shadow.Shadow

::: fastbrain.shadow.ShadowStats

::: fastbrain.shadow.build_report

::: fastbrain.shadow.ShadowReport

::: fastbrain.shadow.QuestionReport

::: fastbrain.shadow.export_labels

::: fastbrain.shadow.agree

## Integrations

::: fastbrain.integrations.Router

::: fastbrain.integrations.route

::: fastbrain.integrations.gate

::: fastbrain.integrations.ToolBlockedError

::: fastbrain.integrations.last_user_text

::: fastbrain.integrations.langgraph.router

::: fastbrain.integrations.langgraph.decision_node

::: fastbrain.integrations.langgraph.adecision_node

::: fastbrain.integrations.openai_agents.input_guardrail

::: fastbrain.integrations.openai_agents.tool_input_guardrail

::: fastbrain.integrations.openai_agents.route_agent

## Serving

::: fastbrain.server.app.create_app

::: fastbrain.server.mcp.create_mcp_server

## Providers

::: fastbrain.providers.DecisionProvider

::: fastbrain.providers.ProviderResult

::: fastbrain.providers.Rules

::: fastbrain.providers.gliner.GLiNER

::: fastbrain.providers.laya.Laya

::: fastbrain.providers.SystemOne

::: fastbrain.providers.LLMDecider

## LLM backends

::: fastbrain.llm.LLM

::: fastbrain.llm.Completion

::: fastbrain.llm.local.TransformersLLM

::: fastbrain.llm.openai_compat.OpenAICompatibleLLM

::: fastbrain.llm.anthropic.AnthropicLLM

::: fastbrain.llm.ScriptedLLM

::: fastbrain.llm.from_spec

## Tracing

::: fastbrain.Tracer

::: fastbrain.tracing.Span

::: fastbrain.tracing.TraceSummary

::: fastbrain.tracing.summarize

::: fastbrain.tracing.JSONLSink

::: fastbrain.tracing.MemorySink

::: fastbrain.tracing.ConsoleSink

::: fastbrain.tracing.otel.OTelSink

::: fastbrain.tool

::: fastbrain.tracing.export.iter_decisions

::: fastbrain.tracing.export.export_trace_labels

::: fastbrain.tracing.export.drift_report

## Confidence and pricing

::: fastbrain.confidence

::: fastbrain.pricing.PriceTable
