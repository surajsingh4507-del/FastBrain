"""FastBrain e-commerce order routing agent.

Demonstrates how FastBrain routes customer inquiries for an e-commerce
platform using three decision planes: deterministic rules, a keyword
classifier, and a scripted LLM stand-in as the final fallback.

    pip install fastbrain
    python examples/10_ecommerce_agent_router.py
"""

from __future__ import annotations

from fastbrain import Choice, Engine, YesNo
from fastbrain.llm import ScriptedLLM
from fastbrain.providers import LLMDecider, Rules

INTENT = Choice(
    "What does the customer want?",
    name="intent",
    options={
        "refund": "wants money back or a refund",
        "order_status": "asks where an order is or about tracking",
        "cancel_order": "wants to cancel a pending order",
        "technical_issue": "reports a product defect or app problem",
        "general_inquiry": "anything else",
    },
)

WANTS_ESCALATION = YesNo(
    "Is the issue urgent and does it need a human agent?",
    name="wants_escalation",
)

rules = Rules()
rules.match("intent", r"\b(refund|money back|charged twice)\b", "refund", field="message")
rules.match(
    "intent", r"\b(where is|tracking|order status|arrive)\b", "order_status", field="message"
)
rules.match("intent", r"\bcancel\b", "cancel_order", field="message")
rules.match("wants_escalation", r"\b(urgent|stolen|unauthorized|fraud)\b", True, field="message")
rules.match("wants_escalation", r".*", False, field="message")

fallback = ScriptedLLM(
    ['{"intent": "general_inquiry", "wants_escalation": false}'],
    model="stand-in",
)
engine = Engine([rules, LLMDecider(fallback)], llm=fallback, threshold=0.85)

TICKETS = [
    "Where is my order #88419? I haven't received any tracking update.",
    "I was charged twice on my credit card for order #4412, I want a refund.",
    "Please cancel my pending order #7731 before it ships.",
    "The app keeps crashing on my phone every time I open it.",
    "Do you ship to international addresses?",
    "Someone made an unauthorized purchase on my account, this is urgent!",
]

print("FastBrain E-Commerce Order Routing Agent")
print("=" * 60)

for idx, message in enumerate(TICKETS, 1):
    state = {"message": message}
    with engine.run(f"ticket-{idx}", mode="hybrid", input=message):
        intent = engine.decide(state, INTENT)
        escalate = engine.decide(state, WANTS_ESCALATION)

    conf = "n/a" if intent.confidence is None else f"{intent.confidence:.2f}"
    esc_label = "ESCALATE" if escalate.value else "auto"
    print(
        f"\n[{idx}] {message[:60]!r}"
        f"\n    intent={intent.value:<18} conf={conf} via={intent.provider}"
        f"\n    routing={esc_label}"
    )
