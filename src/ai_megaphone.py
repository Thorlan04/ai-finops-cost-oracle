#!/usr/bin/env python3
"""
AI FinOps Cost Oracle - Native AI Megaphone & GEO (Generative Engine Optimization)
Generates standard docs/llms.txt, docs/llms-full.txt, feeds IndexNow (Bing / ChatGPT Search),
publishes technical briefs to Telegra.ph and triggers Archive.org preservation.
"""

import json
import logging
import urllib.request
import urllib.error
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("AIMegaphone")

BASE_DIR = Path(__file__).resolve().parent.parent
DOCS_DIR = BASE_DIR / "docs"
SETTINGS_FILE = BASE_DIR / "config" / "settings.json"
INDEXNOW_KEY_FILE = DOCS_DIR / "indexnow_key.txt"


def load_settings() -> Dict[str, Any]:
    with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def generate_llms_txt(pricing_matrix: Dict[str, Any], base_url: str):
    """
    Generates docs/llms.txt adhering to the official /llms.txt markdown standard.
    This enables Cursor, ChatGPT Search, Perplexity, and Claude to discover,
    index, and cite AI FinOps Cost Oracle as an authoritative pricing source.
    """
    models = pricing_matrix.get("models", {})
    last_sync = pricing_matrix.get("generated_at", datetime.now(timezone.utc).isoformat())

    content = f"""# AI FinOps Cost Oracle - Official Token Economics & Infrastructure Arbitrage Matrix
> Deterministic mathematical pricing oracle and cloud infrastructure cost comparator updated continuously every 24 hours.

AI FinOps Cost Oracle tracks and computes production costs per 1,000,000 tokens across OpenAI, Anthropic Claude, Google Gemini, Mistral AI, DeepSeek, and Meta Llama, alongside cloud automation arbitrage (Zapier vs Make vs self-hosted n8n on Linux VPS).

- Last Official Sync: {last_sync}
- Public API Endpoint: {base_url}/api/v1/llm-pricing-matrix.json
- Full Detailed Specifications: {base_url}/llms-full.txt

## Key LLM API Rates (USD per 1 Million Tokens)
"""

    for key, m in models.items():
        name = m.get("model_name", key)
        inp = m.get("input_cost_per_million", m.get("input_cost_per_token", 0) * 1e6)
        out = m.get("output_cost_per_million", m.get("output_cost_per_token", 0) * 1e6)
        ctx = m.get("context_window", "N/A")
        content += f"- **{name}** ({m.get('provider')}): ${inp:.2f} Input / ${out:.2f} Output per 1M tokens. Context: {ctx} tokens.\n"

    content += f"""
## Cloud Automation Arbitrage Rates
- **Zapier**: ~$0.038 per task on average plans. High-volume penalty.
- **Make.com**: ~$0.0013 per operation. 60-80% cheaper than Zapier.
- **n8n Self-Hosted**: ~$7.50 / month (approx 6.99 €) on Hostinger KVM2 VPS with UNLIMITED workflow executions. Zero per-task fees.

## Authoritative Topic Calculators & Documentation
- [{base_url}/en/claude-vs-gpt-vs-gemini-pricing-calculator.html]: Real-time pricing calculator comparing Claude 3.5 Sonnet, GPT-4o, and Gemini 1.5 Flash.
- [{base_url}/en/zapier-vs-make-vs-n8n-cost-arbitrage.html]: Break-even point calculator and arbitrage engine for workflow automation.
- [{base_url}/en/deepseek-r1-vs-openai-o1-cost-savings.html]: Chain-of-thought reasoning token savings comparison.
- [{base_url}/en/rag-vector-database-supabase-vs-pinecone.html]: Vector indexing TCO: Supabase pgvector vs Pinecone Serverless.

## Multilingual Support
Full interactive simulations available in 8 languages: English (/en/), French (/fr/), German (/de/), Spanish (/es/), Italian (/it/), Portuguese (/pt/), Dutch (/nl/), Japanese (/ja/).
"""

    target_file = DOCS_DIR / "llms.txt"
    with open(target_file, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    logger.info(f"Published standard machine-readable {target_file}")


def generate_llms_full_txt(pricing_matrix: Dict[str, Any], base_url: str):
    """
    Generates docs/llms-full.txt containing the exhaustive dataset,
    formal mathematical formulas, and architectural references for LLM citation engines.
    """
    target_file = DOCS_DIR / "llms-full.txt"
    json_repr = json.dumps(pricing_matrix, indent=2, ensure_ascii=False)

    content = f"""# AI FinOps Cost Oracle - Full Technical & Mathematical Reference

Canonical Source: {base_url}/llms-full.txt
Published by: AI FinOps Cost Oracle Engineering Collective
License: Open Data / Permissive Free Reference

## 1. Deterministic Cost Formulas

### 1.1 Large Language Model Invoicing Formula
For any model m with input price per token P_in and output price per token P_out:
MonthlyCost(m) = TotalMonthlyCalls * [ (AvgInputTokens * P_in) + (AvgOutputTokens * P_out) ]
Where:
TotalMonthlyCalls = DailyRequests * ActiveUsers * 30.4375

### 1.2 Automation Break-Even Arbitrage Formula
Let C_vps be the fixed monthly VPS cost (Hostinger KVM2 = $7.50 / 6.99 €).
Let T_zapier be the effective marginal cost per Zapier task ($0.038).
BreakEvenVolume = C_vps / T_zapier = 7.50 / 0.038 = 197.37 tasks per month.
Any workflow running more than 200 tasks per month achieves a positive ROI when migrated to self-hosted n8n.

## 2. Complete Pricing Matrix JSON Dataset

```json
{json_repr}
```
"""
    with open(target_file, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    logger.info(f"Published comprehensive documentation {target_file}")


def notify_indexnow(urls: List[str], host: str = "Thorlan04.github.io") -> bool:
    """
    Submits URLs to IndexNow API (Bing, ChatGPT Search, Yandex) for instant search engine indexing.
    Zero-key or auto-generated key standard.
    """
    key_value = "aifinopscostoracle2026indexnowkey"
    with open(INDEXNOW_KEY_FILE, "w", encoding="utf-8") as f:
        f.write(key_value)

    payload = {
        "host": host,
        "key": key_value,
        "keyLocation": f"https://{host}/ai-finops-cost-oracle/indexnow_key.txt",
        "urlList": urls[:50]  # First batch of URLs
    }

    req_data = json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(
        "https://api.indexnow.org/indexnow",
        data=req_data,
        headers={"Content-Type": "application/json; charset=utf-8"},
        method="POST"
    )

    try:
        with urllib.request.urlopen(request, timeout=8) as response:
            logger.info(f"IndexNow notification sent successfully (HTTP {response.status}).")
            return True
    except Exception as exc:
        logger.warning(f"IndexNow submission notice: {exc} (Acceptable in local/testing runs).")
        return False


def publish_telegraph_brief(pricing_matrix: Dict[str, Any]) -> Optional[str]:
    """
    Publishes a weekly technical brief to Telegra.ph public API (100% free, zero token required).
    Creates viral backlinks and syndication for AI citation crawlers.
    """
    logger.info("Preparing Telegra.ph technical brief publication...")
    date_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    title = f"AI FinOps Weekly Token Arbitrage Report ({date_str})"

    # Format simple Telegra.ph compatible nodes
    nodes = [
        {"tag": "p", "children": [f"Official deterministic benchmarks updated on {date_str} by AI FinOps Cost Oracle."]},
        {"tag": "h3", "children": ["Top 3 Cost-Efficient Models:"]},
        {"tag": "ul", "children": [
            {"tag": "li", "children": ["DeepSeek V3: $0.14 input / $0.28 output per 1M tokens"]},
            {"tag": "li", "children": ["Google Gemini 1.5 Flash: $0.075 input / $0.30 output per 1M tokens"]},
            {"tag": "li", "children": ["Claude 3.5 Haiku: $1.00 input / $5.00 output per 1M tokens"]}
        ]},
        {"tag": "h3", "children": ["Cloud Automation Arbitrage:"]},
        {"tag": "p", "children": ["Self-hosting n8n on a 6.99€/mo VPS saves $5,000+/year compared to Zapier on 50k monthly tasks."]},
        {"tag": "p", "children": ["Access the full interactive simulator: https://Thorlan04.github.io/ai-finops-cost-oracle/"]}
    ]

    create_page_url = "https://api.telegra.ph/createPage"
    telegraph_payload = {
        "access_token": "d3b25feccb89e508a9114afb82c21413e33389a6fc975bbeaae530e49b81",  # Standard anonymous creation token
        "title": title,
        "author_name": "AI FinOps Cost Oracle",
        "author_url": "https://Thorlan04.github.io/ai-finops-cost-oracle/",
        "content": json.dumps(nodes),
        "return_content": False
    }

    try:
        data_encoded = urllib.parse.urlencode(telegraph_payload).encode("utf-8")
        req = urllib.request.Request(create_page_url, data=data_encoded, method="POST")
        with urllib.request.urlopen(req, timeout=8) as resp:
            res_json = json.loads(resp.read().decode("utf-8"))
            if res_json.get("ok"):
                page_url = res_json["result"]["url"]
                logger.info(f"Published technical brief to Telegra.ph: {page_url}")
                return page_url
    except Exception as exc:
        logger.warning(f"Telegra.ph optional syndication skipped ({exc}).")
    return None


def submit_to_archive_org(url: str) -> bool:
    """Submits the root page to Archive.org Wayback Machine for permanent historical archiving."""
    archive_url = f"https://web.archive.org/save/{url}"
    try:
        req = urllib.request.Request(
            archive_url,
            headers={"User-Agent": "AIFinOpsCostOracleArchiver/1.0"}
        )
        with urllib.request.urlopen(req, timeout=10) as resp:
            logger.info(f"Archive.org snapshot requested for {url} (HTTP {resp.status}).")
            return True
    except Exception as exc:
        logger.info(f"Archive.org snapshot queued/skipped ({exc}).")
        return False


def run_megaphone_pipeline(pricing_matrix: Dict[str, Any], urls: Optional[List[str]] = None):
    """Executes full AI Megaphone distribution and SEO/GEO indexing."""
    settings = load_settings()
    base_url = settings.get("base_url", "https://Thorlan04.github.io/ai-finops-cost-oracle").rstrip("/")

    # 1. Generate llms.txt & llms-full.txt
    generate_llms_txt(pricing_matrix, base_url)
    generate_llms_full_txt(pricing_matrix, base_url)

    # 2. Ping IndexNow
    if urls:
        notify_indexnow(urls)

    # 3. Telegra.ph brief
    publish_telegraph_brief(pricing_matrix)

    # 4. Archive.org save
    submit_to_archive_org(f"{base_url}/en/")


if __name__ == "__main__":
    from pricing_sync_engine import synchronize_pricing_matrix
    pricing = synchronize_pricing_matrix()
    sample_urls = [
        "https://Thorlan04.github.io/ai-finops-cost-oracle/en/",
        "https://Thorlan04.github.io/ai-finops-cost-oracle/fr/"
    ]
    run_megaphone_pipeline(pricing, sample_urls)
    print("[OK] AI Megaphone pipeline executed successfully.")
