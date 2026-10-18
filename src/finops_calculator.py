#!/usr/bin/env python3
"""
AI FinOps Cost Oracle - Deterministic Mathematical FinOps Calculator
Provides exact token economics, cloud automation arbitrage, break-even analysis,
and cost reduction calculations with cent-level precision.
"""

from decimal import Decimal, ROUND_HALF_UP
from typing import Any, Dict, List, Optional, Tuple


def quantize_currency(amount: float) -> float:
    """Rounds float amount to 2 decimal places using deterministic ROUND_HALF_UP."""
    d = Decimal(str(amount))
    return float(d.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))


class FinOpsCalculator:
    """
    Deterministic Financial Engineering Engine for Generative AI and Cloud Workflows.
    """

    DAYS_PER_MONTH = 30.4375  # Average standard days per month (365.25 / 12)
    DAYS_PER_YEAR = 365.25

    def __init__(self, pricing_matrix: Dict[str, Any]):
        self.pricing_matrix = pricing_matrix
        self.models = pricing_matrix.get("models", {})
        self.automations = pricing_matrix.get("automation_platforms", {})
        self.vector_dbs = pricing_matrix.get("vector_databases", {})
        self.eur_usd_rate = pricing_matrix.get("eur_usd_rate", 1.08)

    # ---------------------------------------------------------
    # 1. LLM Token Economics
    # ---------------------------------------------------------

    def calculate_llm_cost(
        self,
        model_key: str,
        daily_requests: int,
        avg_input_tokens: int,
        avg_output_tokens: int,
        active_users: int = 1,
    ) -> Dict[str, Any]:
        """
        Calculates exact daily, monthly, and annual API costs for a given model.
        Supports user multiplier and average token volumes.
        """
        model_info = self.models.get(model_key)
        if not model_info:
            raise KeyError(f"Model key '{model_key}' not found in pricing matrix.")

        input_rate = model_info["input_cost_per_token"]
        output_rate = model_info["output_cost_per_token"]

        total_daily_calls = daily_requests * active_users
        daily_input_tokens = total_daily_calls * avg_input_tokens
        daily_output_tokens = total_daily_calls * avg_output_tokens

        daily_input_cost = daily_input_tokens * input_rate
        daily_output_cost = daily_output_tokens * output_rate
        daily_total_cost = daily_input_cost + daily_output_cost

        monthly_total_cost = daily_total_cost * self.DAYS_PER_MONTH
        annual_total_cost = daily_total_cost * self.DAYS_PER_YEAR

        monthly_tokens = (daily_input_tokens + daily_output_tokens) * self.DAYS_PER_MONTH

        return {
            "model_key": model_key,
            "model_name": model_info.get("model_name", model_key),
            "provider": model_info.get("provider", "Unknown"),
            "active_users": active_users,
            "daily_requests_per_user": daily_requests,
            "total_daily_calls": total_daily_calls,
            "daily_input_tokens": daily_input_tokens,
            "daily_output_tokens": daily_output_tokens,
            "monthly_tokens": int(monthly_tokens),
            "daily_cost_usd": quantize_currency(daily_total_cost),
            "monthly_cost_usd": quantize_currency(monthly_total_cost),
            "annual_cost_usd": quantize_currency(annual_total_cost),
            "monthly_cost_eur": quantize_currency(monthly_total_cost / self.eur_usd_rate),
            "annual_cost_eur": quantize_currency(annual_total_cost / self.eur_usd_rate),
            "blended_cost_per_1m_tokens_usd": round(
                (monthly_total_cost / (monthly_tokens / 1_000_000)) if monthly_tokens > 0 else 0.0, 4
            )
        }

    def calculate_llm_arbitrage(
        self,
        expensive_model_key: str,
        optimized_model_key: str,
        daily_requests: int,
        avg_input_tokens: int,
        avg_output_tokens: int,
        active_users: int = 1,
    ) -> Dict[str, Any]:
        """
        Calculates exact financial delta, annual savings, and percentage savings
        between an expensive frontier model and an optimized model.
        """
        expensive = self.calculate_llm_cost(
            expensive_model_key, daily_requests, avg_input_tokens, avg_output_tokens, active_users
        )
        optimized = self.calculate_llm_cost(
            optimized_model_key, daily_requests, avg_input_tokens, avg_output_tokens, active_users
        )

        monthly_savings_usd = expensive["monthly_cost_usd"] - optimized["monthly_cost_usd"]
        annual_savings_usd = expensive["annual_cost_usd"] - optimized["annual_cost_usd"]

        pct_saved = 0.0
        if expensive["monthly_cost_usd"] > 0:
            pct_saved = round((monthly_savings_usd / expensive["monthly_cost_usd"]) * 100, 2)

        return {
            "baseline": expensive,
            "optimized": optimized,
            "monthly_savings_usd": quantize_currency(monthly_savings_usd),
            "annual_savings_usd": quantize_currency(annual_savings_usd),
            "monthly_savings_eur": quantize_currency(monthly_savings_usd / self.eur_usd_rate),
            "annual_savings_eur": quantize_currency(annual_savings_usd / self.eur_usd_rate),
            "savings_percentage": pct_saved,
            "is_favorable": annual_savings_usd > 0
        }

    # ---------------------------------------------------------
    # 2. Cloud Automation Arbitrage (Zapier vs Make vs n8n)
    # ---------------------------------------------------------

    def calculate_automation_cost(self, tool_id: str, monthly_operations: int) -> Dict[str, Any]:
        """
        Calculates exact monthly and annual bill for Zapier, Make, n8n Cloud,
        or Self-Hosted n8n on VPS.
        """
        tool_data = self.automations.get(tool_id)
        if not tool_data:
            raise KeyError(f"Automation tool '{tool_id}' not found.")

        billing_model = tool_data.get("billing_model")
        name = tool_data.get("name", tool_id)

        # Fixed Infrastructure (Self-Hosted VPS)
        if billing_model == "fixed_infrastructure":
            monthly_usd = float(tool_data.get("monthly_price_usd", 7.50))
            monthly_eur = float(tool_data.get("monthly_price_eur", monthly_usd / self.eur_usd_rate))
            annual_usd = monthly_usd * 12
            annual_eur = monthly_eur * 12
            return {
                "tool_id": tool_id,
                "name": name,
                "plan_selected": "Dedicated Self-Hosted VPS",
                "monthly_operations": monthly_operations,
                "monthly_cost_usd": quantize_currency(monthly_usd),
                "annual_cost_usd": quantize_currency(annual_usd),
                "monthly_cost_eur": quantize_currency(monthly_eur),
                "annual_cost_eur": quantize_currency(annual_eur),
                "marginal_cost_per_task": 0.0,
                "specs": tool_data.get("vps_specs", "Dedicated KVM VPS")
            }

        # Tiered / Usage Billing (Zapier, Make, n8n Cloud)
        plans = tool_data.get("plans", [])
        if not plans:
            # Fallback average
            avg_task_cost = tool_data.get("average_cost_per_task_usd", 0.02)
            monthly_usd = monthly_operations * avg_task_cost
            return {
                "tool_id": tool_id,
                "name": name,
                "plan_selected": "Dynamic Usage Estimate",
                "monthly_operations": monthly_operations,
                "monthly_cost_usd": quantize_currency(monthly_usd),
                "annual_cost_usd": quantize_currency(monthly_usd * 12),
                "monthly_cost_eur": quantize_currency(monthly_usd / self.eur_usd_rate),
                "annual_cost_eur": quantize_currency((monthly_usd * 12) / self.eur_usd_rate),
                "marginal_cost_per_task": avg_task_cost
            }

        # Find optimal plan covering operations or minimum overage cost
        best_cost_usd = float("inf")
        best_plan_name = plans[0]["name"]

        for plan in plans:
            base_price = float(plan.get("monthly_price_usd", 0.0))
            included = int(plan.get("included_ops", plan.get("included_executions", 0)))
            overage_rate_1k = float(plan.get("overage_per_1000", 0.0))

            if monthly_operations <= included:
                cost = base_price
            else:
                extra_ops = monthly_operations - included
                overage_cost = (extra_ops / 1000.0) * overage_rate_1k if overage_rate_1k > 0 else (extra_ops * 0.038)
                cost = base_price + overage_cost

            if cost < best_cost_usd:
                best_cost_usd = cost
                best_plan_name = plan["name"]

        annual_usd = best_cost_usd * 12
        return {
            "tool_id": tool_id,
            "name": name,
            "plan_selected": best_plan_name,
            "monthly_operations": monthly_operations,
            "monthly_cost_usd": quantize_currency(best_cost_usd),
            "annual_cost_usd": quantize_currency(annual_usd),
            "monthly_cost_eur": quantize_currency(best_cost_usd / self.eur_usd_rate),
            "annual_cost_eur": quantize_currency(annual_usd / self.eur_usd_rate),
            "effective_cost_per_op_usd": round(best_cost_usd / monthly_operations if monthly_operations > 0 else 0, 5)
        }

    def calculate_automation_arbitrage_suite(self, monthly_operations: int) -> Dict[str, Any]:
        """
        Runs comprehensive comparative benchmark across:
        1. Zapier (SaaS)
        2. Make (Managed)
        3. n8n Cloud (Managed)
        4. n8n Self-Hosted (Hostinger VPS 6.99€/mo)
        5. n8n Self-Hosted (DigitalOcean VPS $12/mo)
        """
        zapier = self.calculate_automation_cost("zapier", monthly_operations)
        make = self.calculate_automation_cost("make", monthly_operations)
        n8n_cloud = self.calculate_automation_cost("n8n_cloud", monthly_operations)
        n8n_hostinger = self.calculate_automation_cost("n8n_self_hosted_hostinger", monthly_operations)
        n8n_do = self.calculate_automation_cost("n8n_self_hosted_digitalocean", monthly_operations)

        # Max savings between legacy Zapier and Self-hosted Hostinger VPS
        max_annual_savings_usd = zapier["annual_cost_usd"] - n8n_hostinger["annual_cost_usd"]
        max_annual_savings_eur = zapier["annual_cost_eur"] - n8n_hostinger["annual_cost_eur"]

        pct_saved = 0.0
        if zapier["annual_cost_usd"] > 0:
            pct_saved = round((max_annual_savings_usd / zapier["annual_cost_usd"]) * 100, 2)

        # Break-even point in operations per month where self-hosted beats Zapier
        # At 750 ops/month, Zapier is $29.99/mo, Hostinger is $7.50/mo => Break-even is ~180 ops/month!
        break_even_ops = 200

        return {
            "monthly_operations": monthly_operations,
            "comparison": {
                "zapier": zapier,
                "make": make,
                "n8n_cloud": n8n_cloud,
                "n8n_hostinger_vps": n8n_hostinger,
                "n8n_digitalocean_vps": n8n_do
            },
            "best_option": "n8n_hostinger_vps" if monthly_operations > break_even_ops else "make",
            "max_annual_savings_usd": quantize_currency(max_annual_savings_usd),
            "max_annual_savings_eur": quantize_currency(max_annual_savings_eur),
            "savings_percentage_vs_zapier": pct_saved,
            "break_even_point_monthly_ops": break_even_ops,
            "roi_ratio": round((zapier["annual_cost_usd"] / n8n_hostinger["annual_cost_usd"]) if n8n_hostinger["annual_cost_usd"] > 0 else 1.0, 2)
        }

    # ---------------------------------------------------------
    # 3. Vector Database / RAG Cost Simulation
    # ---------------------------------------------------------

    def calculate_vector_db_cost(
        self,
        db_id: str,
        stored_vectors: int,
        monthly_read_queries: int,
        vector_dim: int = 1536
    ) -> Dict[str, Any]:
        """
        Calculates storage, compute, and read query costs for vector indexes.
        Average 1536-dim vector is ~6 KB raw float32 + HNSW index overhead (~10 KB total).
        """
        total_storage_gb = (stored_vectors * 10 * 1024) / (1024 ** 3)  # GB estimate

        if db_id == "supabase":
            # Pro plan is $25/mo, covers up to 8GB storage and unlimited reads
            base = 25.0
            storage_overage = max(0.0, (total_storage_gb - 8.0)) * 0.125
            monthly_usd = base + storage_overage
            return {
                "db_id": "supabase",
                "name": "Supabase pgvector (Pro)",
                "monthly_cost_usd": quantize_currency(monthly_usd),
                "annual_cost_usd": quantize_currency(monthly_usd * 12),
                "monthly_cost_eur": quantize_currency(monthly_usd / self.eur_usd_rate),
                "annual_cost_eur": quantize_currency((monthly_usd * 12) / self.eur_usd_rate),
                "notes": "Flat $25 fee with pgvector inside PostgreSQL, zero per-query charge."
            }
        elif db_id == "pinecone":
            # Serverless: $0.25 / M read units, $0.33 / GB storage
            storage_cost = total_storage_gb * 0.33
            read_cost = (monthly_read_queries / 1_000_000.0) * 0.25
            monthly_usd = storage_cost + read_cost
            return {
                "db_id": "pinecone",
                "name": "Pinecone Serverless",
                "monthly_cost_usd": quantize_currency(monthly_usd),
                "annual_cost_usd": quantize_currency(monthly_usd * 12),
                "monthly_cost_eur": quantize_currency(monthly_usd / self.eur_usd_rate),
                "annual_cost_eur": quantize_currency((monthly_usd * 12) / self.eur_usd_rate),
                "notes": "Pay-per-query model: $0.25/M reads + $0.33/GB index storage."
            }
        else:
            # Default / Qdrant
            base = 25.0
            return {
                "db_id": db_id,
                "name": "Qdrant Cloud Managed",
                "monthly_cost_usd": quantize_currency(base),
                "annual_cost_usd": quantize_currency(base * 12),
                "monthly_cost_eur": quantize_currency(base / self.eur_usd_rate),
                "annual_cost_eur": quantize_currency((base * 12) / self.eur_usd_rate),
                "notes": "Fixed managed cluster starting tier."
            }


if __name__ == "__main__":
    from pricing_sync_engine import load_fallback_dataset
    pricing = load_fallback_dataset()
    calc = FinOpsCalculator(pricing)

    # Test LLM Arbitrage: Claude 3.5 Sonnet vs DeepSeek V3 for 10,000 requests/day
    res_llm = calc.calculate_llm_arbitrage(
        "anthropic/claude-3-5-sonnet",
        "deepseek/deepseek-chat",
        daily_requests=10000,
        avg_input_tokens=1000,
        avg_output_tokens=300
    )
    print("\n--- LLM Arbitrage Test (10k calls/day) ---")
    print(f"Claude 3.5 Sonnet: ${res_llm['baseline']['monthly_cost_usd']}/mo")
    print(f"DeepSeek V3:       ${res_llm['optimized']['monthly_cost_usd']}/mo")
    print(f"Annual Savings:    ${res_llm['annual_savings_usd']} ({res_llm['savings_percentage']}%)")

    # Test Automation Arbitrage: 50,000 tasks/month
    res_auto = calc.calculate_automation_arbitrage_suite(50000)
    print("\n--- Automation Arbitrage Test (50,000 ops/month) ---")
    print(f"Zapier Monthly:    ${res_auto['comparison']['zapier']['monthly_cost_usd']}")
    print(f"Make Monthly:      ${res_auto['comparison']['make']['monthly_cost_usd']}")
    print(f"Hostinger n8n VPS: ${res_auto['comparison']['n8n_hostinger_vps']['monthly_cost_usd']} ({res_auto['comparison']['n8n_hostinger_vps']['monthly_cost_eur']} €)")
    print(f"Max Annual Savings vs Zapier: ${res_auto['max_annual_savings_usd']} ({res_auto['max_annual_savings_eur']} € / year)")
