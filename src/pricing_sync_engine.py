#!/usr/bin/env python3
"""
AI FinOps Cost Oracle - Pricing Sync Engine (0 € & Zero API Keys Required)
Fetches official live token costs from the open-source LiteLLM repository
and merges with verified automation and cloud hosting benchmarks.
"""

import json
import logging
import os
import sys
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Optional

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("PricingSyncEngine")

LITELLM_PRICING_URL = "https://raw.githubusercontent.com/BerriAI/litellm/main/model_prices_and_context_window.json"
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_FALLBACK_FILE = BASE_DIR / "data" / "Verified_AI_And_Cloud_Pricing.json"
DOCS_API_DIR = BASE_DIR / "docs" / "api" / "v1"
OUTPUT_MATRIX_FILE = DOCS_API_DIR / "llm-pricing-matrix.json"

# Key models to map and normalize from LiteLLM database
MONITORED_MODELS_MAPPING = {
    "gpt-4o": {
        "canonical_key": "openai/gpt-4o",
        "provider": "OpenAI",
        "name": "GPT-4o (Omni)",
        "category": "flagship"
    },
    "gpt-4o-mini": {
        "canonical_key": "openai/gpt-4o-mini",
        "provider": "OpenAI",
        "name": "GPT-4o Mini",
        "category": "cost_optimized"
    },
    "o1-preview": {
        "canonical_key": "openai/o1-preview",
        "provider": "OpenAI",
        "name": "OpenAI o1-preview",
        "category": "reasoning"
    },
    "o1-mini": {
        "canonical_key": "openai/o1-mini",
        "provider": "OpenAI",
        "name": "OpenAI o1-mini",
        "category": "reasoning_light"
    },
    "claude-3-5-sonnet-20241022": {
        "canonical_key": "anthropic/claude-3-5-sonnet",
        "provider": "Anthropic",
        "name": "Claude 3.5 Sonnet",
        "category": "flagship"
    },
    "claude-3-5-haiku-20241022": {
        "canonical_key": "anthropic/claude-3-5-haiku",
        "provider": "Anthropic",
        "name": "Claude 3.5 Haiku",
        "category": "cost_optimized"
    },
    "claude-3-opus-20240229": {
        "canonical_key": "anthropic/claude-3-opus",
        "provider": "Anthropic",
        "name": "Claude 3 Opus",
        "category": "frontier_deep"
    },
    "gemini/gemini-1.5-pro": {
        "canonical_key": "google/gemini-1.5-pro",
        "provider": "Google",
        "name": "Gemini 1.5 Pro",
        "category": "flagship"
    },
    "gemini/gemini-1.5-flash": {
        "canonical_key": "google/gemini-1.5-flash",
        "provider": "Google",
        "name": "Gemini 1.5 Flash",
        "category": "cost_optimized"
    },
    "deepseek/deepseek-chat": {
        "canonical_key": "deepseek/deepseek-chat",
        "provider": "DeepSeek",
        "name": "DeepSeek V3 (Chat)",
        "category": "hyper_efficient"
    },
    "deepseek/deepseek-reasoner": {
        "canonical_key": "deepseek/deepseek-reasoner",
        "provider": "DeepSeek",
        "name": "DeepSeek R1 (Reasoner)",
        "category": "reasoning_open"
    },
    "mistral/mistral-large-2407": {
        "canonical_key": "mistral/mistral-large",
        "provider": "Mistral AI",
        "name": "Mistral Large 2",
        "category": "flagship"
    },
    "mistral/codestral-2405": {
        "canonical_key": "mistral/codestral",
        "provider": "Mistral AI",
        "name": "Codestral",
        "category": "code_specialist"
    },
    "groq/llama-3.3-70b-versatile": {
        "canonical_key": "meta/llama-3.3-70b-instruct",
        "provider": "Meta (via Groq/Cloud)",
        "name": "Llama 3.3 70B Instruct",
        "category": "open_source_cloud"
    },
    "command-r-plus": {
        "canonical_key": "cohere/command-r-plus",
        "provider": "Cohere",
        "name": "Command R+",
        "category": "rag_specialist"
    }
}


def load_fallback_dataset() -> Dict[str, Any]:
    """Loads the verified local backup dataset."""
    if not DATA_FALLBACK_FILE.exists():
        logger.error(f"Critical: Local fallback file {DATA_FALLBACK_FILE} missing!")
        raise FileNotFoundError(f"Missing fallback pricing data at {DATA_FALLBACK_FILE}")

    with open(DATA_FALLBACK_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    logger.info("Loaded local verified fallback dataset successfully.")
    return data


def fetch_remote_litellm_pricing(timeout: int = 12) -> Optional[Dict[str, Any]]:
    """Fetches live public token pricing from LiteLLM GitHub repository without any API key."""
    logger.info(f"Connecting to LiteLLM pricing repo: {LITELLM_PRICING_URL}...")
    req = urllib.request.Request(
        LITELLM_PRICING_URL,
        headers={"User-Agent": "AIFinOpsCostOracle/1.0 (+https://github.com/ai-finops-cost-oracle)"}
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as response:
            if response.status == 200:
                raw_bytes = response.read()
                data = json.loads(raw_bytes.decode("utf-8"))
                logger.info(f"Successfully downloaded LiteLLM database ({len(data)} model definitions).")
                return data
            else:
                logger.warning(f"Remote server returned HTTP {response.status}.")
                return None
    except Exception as exc:
        logger.warning(f"Unable to fetch live LiteLLM dataset ({exc}). Engaging local fallback.")
        return None


def synchronize_pricing_matrix() -> Dict[str, Any]:
    """
    Main synchronization pipeline:
    1. Loads local verified foundation.
    2. Enriches with fresh remote token metrics if available.
    3. Normalizes input/output rates per token and per 1 Million tokens.
    4. Saves public static API artifact to docs/api/v1/llm-pricing-matrix.json.
    """
    local_data = load_fallback_dataset()
    remote_data = fetch_remote_litellm_pricing()

    synced_models = dict(local_data.get("models", {}))

    if remote_data and isinstance(remote_data, dict):
        updates_applied = 0
        for remote_key, meta in MONITORED_MODELS_MAPPING.items():
            canonical_key = meta["canonical_key"]
            raw_entry = remote_data.get(remote_key) or remote_data.get(remote_key.replace("groq/", ""))

            if raw_entry and isinstance(raw_entry, dict):
                inp_cost = raw_entry.get("input_cost_per_token")
                out_cost = raw_entry.get("output_cost_per_token")
                ctx_window = raw_entry.get("max_input_tokens") or raw_entry.get("context_window")

                if inp_cost is not None and out_cost is not None:
                    existing = synced_models.get(canonical_key, {})
                    existing["input_cost_per_token"] = float(inp_cost)
                    existing["output_cost_per_token"] = float(out_cost)
                    existing["input_cost_per_million"] = round(float(inp_cost) * 1_000_000, 4)
                    existing["output_cost_per_million"] = round(float(out_cost) * 1_000_000, 4)
                    if ctx_window:
                        existing["context_window"] = int(ctx_window)
                    existing["last_synced_from"] = "LiteLLM-Live"
                    synced_models[canonical_key] = existing
                    updates_applied += 1

        logger.info(f"Synchronized {updates_applied} model pricing points from remote LiteLLM benchmark.")
    else:
        logger.info("Using 100% verified local baseline figures.")

    # Assemble finalized consolidated payload
    consolidated = {
        "schema_version": "1.0.0",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "source": "AI FinOps Cost Oracle Automated Multi-Cloud Engine",
        "base_currency": "USD",
        "eur_usd_rate": 1.08,
        "models": synced_models,
        "automation_platforms": local_data.get("automation_platforms", {}),
        "vector_databases": local_data.get("vector_databases", {})
    }

    # Ensure output directories exist
    DOCS_API_DIR.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_MATRIX_FILE, "w", encoding="utf-8") as out_f:
        json.dump(consolidated, out_f, indent=2, ensure_ascii=False)

    logger.info(f"Published static public API to: {OUTPUT_MATRIX_FILE}")
    return consolidated


if __name__ == "__main__":
    matrix = synchronize_pricing_matrix()
    print(f"[OK] Pricing sync completed successfully. Models tracked: {len(matrix['models'])}")
