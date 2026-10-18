#!/usr/bin/env python3
"""
AI FinOps Cost Oracle - Master Build Orchestrator
Executes full autonomous pipeline:
1. Pricing synchronization (LiteLLM 0€ benchmark + local fallback).
2. Multilingual static site generation across 8 languages.
3. Native AI Megaphone publishing (llms.txt, llms-full.txt, IndexNow, Telegra.ph, Archive.org).
4. Micro-BNC Tax summary generation.
"""

import logging
import sys
import time
from pathlib import Path

# Add project root to path
BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))

from src.pricing_sync_engine import synchronize_pricing_matrix
from src.agent_generator import generate_static_site, load_settings
from src.ai_megaphone import run_megaphone_pipeline
from compta_impots.livre_recettes import load_recettes_data, compute_fiscal_summary

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("BuildMaster")


def execute_master_build():
    start_time = time.time()
    logger.info("=" * 65)
    logger.info(">>> STARTING AI FINOPS COST ORACLE 100% AUTONOMOUS BUILD")
    logger.info("=" * 65)

    # Step 1: Pricing Sync
    logger.info("STEP 1: Synchronizing official AI API and cloud automation pricing...")
    pricing_matrix = synchronize_pricing_matrix()
    tracked_models_count = len(pricing_matrix.get("models", {}))
    logger.info(f"   -> Tracked {tracked_models_count} AI models and {len(pricing_matrix.get('automation_platforms', {}))} automation platforms.")

    # Step 2: Multilingual Static Generation
    logger.info("STEP 2: Generating autonomous multilingual static sites (8 languages)...")
    total_pages = generate_static_site(pricing_matrix)
    logger.info(f"   -> Successfully generated {total_pages} canonical pages in docs/")

    # Step 3: Native AI Megaphone
    logger.info("STEP 3: Launching AI Megaphone, llms.txt standard, and IndexNow broadcast...")
    settings = load_settings()
    base_url = settings.get("base_url", "https://Thorlan04.github.io/ai-finops-cost-oracle").rstrip("/")
    sample_broadcast_urls = [
        f"{base_url}/en/",
        f"{base_url}/fr/",
        f"{base_url}/en/claude-vs-gpt-vs-gemini-pricing-calculator.html",
        f"{base_url}/en/zapier-vs-make-vs-n8n-cost-arbitrage.html",
        f"{base_url}/en/deepseek-r1-vs-openai-o1-cost-savings.html",
        f"{base_url}/en/rag-vector-database-supabase-vs-pinecone.html"
    ]
    run_megaphone_pipeline(pricing_matrix, sample_broadcast_urls)
    logger.info("   -> llms.txt, llms-full.txt and indexing signals generated.")

    # Step 4: Micro-BNC Tax Audit
    logger.info("STEP 4: Auditing Micro-BNC fiscal status...")
    tax_data = load_recettes_data()
    tax_summary = compute_fiscal_summary(tax_data)
    logger.info(f"   -> CA Encaissé: {tax_summary['total_ca_encaisse_eur']:,.2f} € | Case 5HQ: {tax_summary['case_5hq_ca_brut_a_declarer_eur']:,.2f} € | Statut TVA: OK")

    duration = round(time.time() - start_time, 2)
    logger.info("=" * 65)
    logger.info(f">>> MASTER BUILD COMPLETED IN {duration} SECONDS")
    logger.info(f">>> Artifacts ready for zero-cost GitHub Pages hosting in docs/")
    logger.info("=" * 65)


if __name__ == "__main__":
    execute_master_build()
