"""
FastBrain E-Commerce Intelligent Support & Order Routing Agent
Author: Suraj Singh (surajsingh4507-del)

This example demonstrates how FastBrain routes customer inquiries for an e-commerce platform:
1. Fast rule evaluation (e.g. tracking numbers, standard refunds)
2. Small Local Model (SLM) fallback for intent and sentiment
3. Hosted LLM only when confidence threshold is unmet or deep reasoning is required.
"""

import os
from fastbrain import Choice, Engine, Question
from fastbrain.providers import Rules, LLMDecider
from fastbrain.llm import ScriptedLLM

# Define domain-specific questions for E-Commerce Routing
INTENT_QUESTION = Choice(
    name="customer_intent",
    question="What is the primary intent of the customer message?",
    options=["order_status", "refund_request", "cancel_order", "technical_issue", "general_inquiry"],
)

PRIORITY_QUESTION = Choice(
    name="issue_priority",
    question="What is the priority level of this inquiry?",
    options=["low", "medium", "high", "urgent"],
)

def run_ecommerce_router():
    print("=" * 60)
    print("  FastBrain E-Commerce Intelligent Routing Agent")
    print("  Author: Suraj Singh")
    print("=" * 60)

    # 1. Setup Rule Engine for deterministic patterns
    rules = Rules()
    rules.add("customer_intent", lambda msg: "order_status" if "track" in msg.lower() or "where is my order" in msg.lower() else None)
    rules.add("customer_intent", lambda msg: "refund_request" if "charged twice" in msg.lower() or "money back" in msg.lower() else None)
    rules.add("issue_priority", lambda msg: "urgent" if "unauthorized" in msg.lower() or "stolen" in msg.lower() else None)

    # 2. Setup LLM Decider as fallback for complex queries
    mock_llm_answers = {
        "customer_intent": "refund_request",
        "issue_priority": "high",
    }
    llm = ScriptedLLM(responses=mock_llm_answers)
    
    # 3. Create FastBrain Engine with threshold cascading
    engine = Engine(providers=[rules, LLMDecider(llm)], llm=llm, threshold=0.85)

    # Sample Test Customer Messages
    test_messages = [
        "Where is my order #88419? I haven't received any tracking update.",
        "I was charged twice on my credit card for transaction #4412, need money back immediately!",
        "My item arrived damaged and the package box was crushed.",
    ]

    for idx, msg in enumerate(test_messages, 1):
        print(f"\n[Ticket #{idx}]: '{msg}'")
        intent_decision = engine.decide(msg, INTENT_QUESTION)
        priority_decision = engine.decide(msg, PRIORITY_QUESTION)

        print(f"  └─ Intent:   {intent_decision.value:<18} (Confidence: {intent_decision.confidence:.2f}, Provider: {intent_decision.provider})")
        print(f"  └─ Priority: {priority_decision.value:<18} (Confidence: {priority_decision.confidence:.2f}, Provider: {priority_decision.provider})")

if __name__ == "__main__":
    run_ecommerce_router()
