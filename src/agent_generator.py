#!/usr/bin/env python3
"""
AI FinOps Cost Oracle - Autonomous Multilingual Static Site Generator
Generates high-intent B2B FinOps landing pages and interactive calculators
across 8 languages (en, fr, de, es, it, pt, nl, ja) into the docs/ directory.
"""

import json
import logging
import os
import shutil
from pathlib import Path
from typing import Any, Dict, List

import jinja2

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("AgentGenerator")

BASE_DIR = Path(__file__).resolve().parent.parent
CONFIG_DIR = BASE_DIR / "config"
TEMPLATES_DIR = BASE_DIR / "templates"
DOCS_DIR = BASE_DIR / "docs"
PARTNERS_FILE = CONFIG_DIR / "partners.json"
SETTINGS_FILE = CONFIG_DIR / "settings.json"

LANGUAGES = ["en", "fr", "de", "es", "it", "pt", "nl", "ja"]

# Full, comprehensive i18n translation dictionary for all 8 languages
I18N_STRINGS = {
    "en": {
        "nav_llm_calc": "LLM Cost Calculator",
        "nav_automation_calc": "Automation Arbitrage",
        "nav_rag_calc": "Vector DB / RAG",
        "t_nav_calculators": "Calculators & Arbitrage",
        "t_footer_tagline": "Continuous mathematical monitoring of cloud AI APIs, token economics, and automated workflow infrastructure.",
        "t_live_engine": "LIVE DETERMINISTIC ARBITRAGE ENGINE",
        "t_sim_title": "Interactive FinOps Token & Workflow Simulator",
        "t_sim_desc": "Adjust production traffic parameters below. The engine calculates exact daily, monthly, and annual run-rates with arbitrage delta in real-time.",
        "t_currency": "Currency",
        "t_presets": "Production Presets",
        "t_preset_startup": "MVP / Startup",
        "t_preset_growth": "Scaling SaaS",
        "t_preset_scale": "Enterprise Core",
        "t_daily_requests": "Daily API Requests",
        "t_avg_input_tokens": "Avg Input Tokens / Call",
        "t_avg_output_tokens": "Avg Output Tokens / Call",
        "t_monthly_ops": "Monthly Workflow Operations",
        "t_annual_savings_title": "Calculated Annual Arbitrage Savings",
        "t_savings_subtext": "Switching from unoptimized proprietary SaaS to modern open-weights or self-hosted automation infrastructure.",
        "t_arbitrage_cta": "Execute Infrastructure Arbitrage",
        "t_year": "yr",
        "t_saved": "saved",
        "t_tab_llm": "LLM Model Cost Matrix",
        "t_tab_automation": "Automation Stack (Zapier vs n8n / Make)",
        "t_col_model": "Model & Specs",
        "t_col_provider": "Provider",
        "t_col_input_m": "Input / 1M",
        "t_col_output_m": "Output / 1M",
        "t_col_monthly_cost": "Monthly Cost",
        "t_col_annual_cost": "Annual Cost",
        "t_col_arbitrage": "Arbitrage vs Top",
        "t_col_solution": "Platform Solution",
        "t_col_type": "Deployment Architecture",
        "t_col_delta": "Cost Delta vs Zapier",
        "t_col_action": "Deployment",
        "t_open_calculator": "Launch Calculator",
        "t_calculators_hub_title": "Enterprise FinOps Specialized Calculators"
    },
    "fr": {
        "nav_llm_calc": "Calculateur Coûts LLM",
        "nav_automation_calc": "Arbitrage Automatisation",
        "nav_rag_calc": "Bases Vectorielles / RAG",
        "t_nav_calculators": "Calculateurs & Arbitrages",
        "t_footer_tagline": "Veille mathématique continue des coûts des API IA, token economics et infrastructures d'automatisation cloud.",
        "t_live_engine": "MOTEUR D'ARBITRAGE DÉTERMINISTE TEMPS RÉEL",
        "t_sim_title": "Simulateur FinOps Interactif : Tokens & Workflows",
        "t_sim_desc": "Ajustez vos volumes de production. Le moteur calcule instantanément vos coûts mensuels, annuels et l'économie exacte au centime près.",
        "t_currency": "Devise",
        "t_presets": "Profils Types",
        "t_preset_startup": "Startup / MVP",
        "t_preset_growth": "SaaS en Croissance",
        "t_preset_scale": "Grand Compte",
        "t_daily_requests": "Requêtes API / Jour",
        "t_avg_input_tokens": "Tokens Entrée Moyens / Appel",
        "t_avg_output_tokens": "Tokens Sortie Moyens / Appel",
        "t_monthly_ops": "Opérations d'Automatisation / Mois",
        "t_annual_savings_title": "Économie Annuelle Calculée",
        "t_savings_subtext": "Gain réalisé en basculant des SaaS propriétaires coûteux vers des modèles optimisés et n8n auto-hébergé sur VPS.",
        "t_arbitrage_cta": "Activer l'Arbitrage Financier",
        "t_year": "an",
        "t_saved": "d'économie",
        "t_tab_llm": "Matrice des Coûts LLM",
        "t_tab_automation": "Automatisation (Zapier vs n8n / Make)",
        "t_col_model": "Modèle & Specs",
        "t_col_provider": "Fournisseur",
        "t_col_input_m": "Entrée / 1M",
        "t_col_output_m": "Sortie / 1M",
        "t_col_monthly_cost": "Coût Mensuel",
        "t_col_annual_cost": "Coût Annuel",
        "t_col_arbitrage": "Écart vs Flagship",
        "t_col_solution": "Solution d'Automatisation",
        "t_col_type": "Architecture de Déploiement",
        "t_col_delta": "Économie vs Zapier",
        "t_col_action": "Déploiement",
        "t_open_calculator": "Ouvrir le Simulateur",
        "t_calculators_hub_title": "Calculateurs FinOps Spécialisés Haute Décision"
    },
    "de": {
        "nav_llm_calc": "LLM-Kostenrechner",
        "nav_automation_calc": "Automatisierungs-Arbitrage",
        "nav_rag_calc": "Vektordatenbanken / RAG",
        "t_nav_calculators": "Rechner & Arbitrage",
        "t_footer_tagline": "Kontinuierliche mathematische Überwachung von KI-API-Kosten, Token-Ökonomie und Cloud-Infrastruktur.",
        "t_live_engine": "ECHTZEIT-ARBITRAGE-ENGINE",
        "t_sim_title": "Interaktiver FinOps-Simulator: Token & Workflows",
        "t_sim_desc": "Passen Sie Ihre Produktionsparameter an. Berechnen Sie monatliche und jährliche Kosten sowie exakte Einsparpotenziale.",
        "t_currency": "Währung",
        "t_presets": "Presets",
        "t_preset_startup": "Startup",
        "t_preset_growth": "Wachstum",
        "t_preset_scale": "Enterprise",
        "t_daily_requests": "Tägliche API-Anfragen",
        "t_avg_input_tokens": "Durchschn. Input-Tokens",
        "t_avg_output_tokens": "Durchschn. Output-Tokens",
        "t_monthly_ops": "Monatliche Automatisierungen",
        "t_annual_savings_title": "Berechnete jährliche Ersparnis",
        "t_savings_subtext": "Wechsel von proprietärem SaaS zu optimierten Modellen und selbstgehostetem n8n.",
        "t_arbitrage_cta": "Arbitrage jetzt umsetzen",
        "t_year": "Jahr",
        "t_saved": "gespart",
        "t_tab_llm": "LLM-Kostenmatrix",
        "t_tab_automation": "Automatisierung (Zapier vs n8n / Make)",
        "t_col_model": "Modell",
        "t_col_provider": "Anbieter",
        "t_col_input_m": "Input / 1M",
        "t_col_output_m": "Output / 1M",
        "t_col_monthly_cost": "Monatliche Kosten",
        "t_col_annual_cost": "Jährliche Kosten",
        "t_col_arbitrage": "Ersparnis vs. Top",
        "t_col_solution": "Lösung",
        "t_col_type": "Bereitstellung",
        "t_col_delta": "Delta vs. Zapier",
        "t_col_action": "Aktion",
        "t_open_calculator": "Rechner starten",
        "t_calculators_hub_title": "Spezialisierte B2B-FinOps-Rechner"
    },
    "es": {
        "nav_llm_calc": "Calculadora Costes LLM",
        "nav_automation_calc": "Arbitraje Automatización",
        "nav_rag_calc": "Bases Vectoriales / RAG",
        "t_nav_calculators": "Calculadoras y Arbitraje",
        "t_footer_tagline": "Monitorización matemática continua de costes de API de IA, economía de tokens e infraestructura cloud.",
        "t_live_engine": "MOTOR DETERMINISTA DE ARBITRAJE EN TIEMPO REAL",
        "t_sim_title": "Simulador FinOps Interactivo: Tokens y Flujos",
        "t_sim_desc": "Ajuste el volumen de tráfico. Calcule con precisión el coste mensual, anual y el ahorro financiero inmediato.",
        "t_currency": "Moneda",
        "t_presets": "Perfiles",
        "t_preset_startup": "Startup",
        "t_preset_growth": "Crecimiento",
        "t_preset_scale": "Empresarial",
        "t_daily_requests": "Peticiones API / Día",
        "t_avg_input_tokens": "Tokens Entrada Medios",
        "t_avg_output_tokens": "Tokens Salida Medios",
        "t_monthly_ops": "Operaciones Mensuales",
        "t_annual_savings_title": "Ahorro Anual Calculado",
        "t_savings_subtext": "Migración de SaaS propietarios caros hacia modelos optimizados y n8n autoalojado en VPS.",
        "t_arbitrage_cta": "Activar Arbitraje de Costes",
        "t_year": "año",
        "t_saved": "ahorrado",
        "t_tab_llm": "Matriz de Costes LLM",
        "t_tab_automation": "Automatización (Zapier vs n8n / Make)",
        "t_col_model": "Modelo",
        "t_col_provider": "Proveedor",
        "t_col_input_m": "Entrada / 1M",
        "t_col_output_m": "Salida / 1M",
        "t_col_monthly_cost": "Coste Mensual",
        "t_col_annual_cost": "Coste Anual",
        "t_col_arbitrage": "Ahorro vs Máximo",
        "t_col_solution": "Plataforma",
        "t_col_type": "Arquitectura",
        "t_col_delta": "Diferencial vs Zapier",
        "t_col_action": "Despliegue",
        "t_open_calculator": "Abrir Calculadora",
        "t_calculators_hub_title": "Calculadoras FinOps para Decisiones de Alto Impacto"
    },
    "it": {
        "nav_llm_calc": "Calcolatore Costi LLM",
        "nav_automation_calc": "Arbitraggio Automazione",
        "nav_rag_calc": "Database Vettoriali / RAG",
        "t_nav_calculators": "Calcolatori & Arbitraggio",
        "t_footer_tagline": "Monitoraggio matematico continuo dei costi API AI, token economics e flussi cloud.",
        "t_live_engine": "MOTORE DETERMINISTICO DI ARBITRAGGIO IN TEMPO REALE",
        "t_sim_title": "Simulatore FinOps Interattivo: Token & Workflow",
        "t_sim_desc": "Configura i volumi di traffico e calcola subito i costi mensili, annuali e il risparmio al centesimo.",
        "t_currency": "Valuta",
        "t_presets": "Profili",
        "t_preset_startup": "Startup",
        "t_preset_growth": "Crescita",
        "t_preset_scale": "Enterprise",
        "t_daily_requests": "Richieste API / Giorno",
        "t_avg_input_tokens": "Token Input Medi",
        "t_avg_output_tokens": "Token Output Medi",
        "t_monthly_ops": "Operazioni Mensili",
        "t_annual_savings_title": "Risparmio Annuale Calcolato",
        "t_savings_subtext": "Transizione da SaaS costosi a modelli open/ottimizzati e n8n self-hosted su VPS.",
        "t_arbitrage_cta": "Attiva Arbitraggio Infrastruttura",
        "t_year": "anno",
        "t_saved": "risparmiato",
        "t_tab_llm": "Matrice Costi LLM",
        "t_tab_automation": "Automazione (Zapier vs n8n / Make)",
        "t_col_model": "Modello",
        "t_col_provider": "Fornitore",
        "t_col_input_m": "Input / 1M",
        "t_col_output_m": "Output / 1M",
        "t_col_monthly_cost": "Costo Mensile",
        "t_col_annual_cost": "Costo Annuale",
        "t_col_arbitrage": "Delta vs Top",
        "t_col_solution": "Soluzione",
        "t_col_type": "Infrastruttura",
        "t_col_delta": "Risparmio vs Zapier",
        "t_col_action": "Deploy",
        "t_open_calculator": "Apri Calcolatore",
        "t_calculators_hub_title": "Calcolatori FinOps B2B ad Alta Precisione"
    },
    "pt": {
        "nav_llm_calc": "Calculadora Custos LLM",
        "nav_automation_calc": "Arbitragem Automação",
        "nav_rag_calc": "Banco Vetorial / RAG",
        "t_nav_calculators": "Calculadoras & Arbitragem",
        "t_footer_tagline": "Monitoramento matemático contínuo de custos de APIs de IA, token economics e automação na nuvem.",
        "t_live_engine": "MOTOR DETERMINÍSTICO DE ARBITRAGEM EM TEMPO REAL",
        "t_sim_title": "Simulador FinOps Interativo: Tokens & Workflows",
        "t_sim_desc": "Ajuste os parâmetros de tráfego para calcular custos mensais e anuais exatos com projeção de economia.",
        "t_currency": "Moeda",
        "t_presets": "Cenários",
        "t_preset_startup": "Startup",
        "t_preset_growth": "Escala",
        "t_preset_scale": "Corporativo",
        "t_daily_requests": "Chamadas API / Dia",
        "t_avg_input_tokens": "Tokens de Entrada Médios",
        "t_avg_output_tokens": "Tokens de Saída Médios",
        "t_monthly_ops": "Operações Mensais",
        "t_annual_savings_title": "Economia Anual Calculada",
        "t_savings_subtext": "Redução de custos ao migrar de SaaS proprietários para modelos eficientes e n8n em VPS próprio.",
        "t_arbitrage_cta": "Executar Arbitragem de Custos",
        "t_year": "ano",
        "t_saved": "economizado",
        "t_tab_llm": "Matriz de Custos de LLM",
        "t_tab_automation": "Automação (Zapier vs n8n / Make)",
        "t_col_model": "Modelo",
        "t_col_provider": "Provedor",
        "t_col_input_m": "Entrada / 1M",
        "t_col_output_m": "Saída / 1M",
        "t_col_monthly_cost": "Custo Mensal",
        "t_col_annual_cost": "Custo Anual",
        "t_col_arbitrage": "Economia vs Top",
        "t_col_solution": "Plataforma",
        "t_col_type": "Arquitetura",
        "t_col_delta": "Diferença vs Zapier",
        "t_col_action": "Implantar",
        "t_open_calculator": "Abrir Calculadora",
        "t_calculators_hub_title": "Calculadoras FinOps B2B de Alta Decisão"
    },
    "nl": {
        "nav_llm_calc": "LLM Kosten Calculator",
        "nav_automation_calc": "Automatisering Arbitrage",
        "nav_rag_calc": "Vector Database / RAG",
        "t_nav_calculators": "Calculators & Arbitrage",
        "t_footer_tagline": "Continue wiskundige monitoring van AI API-kosten, token economics en cloud automation.",
        "t_live_engine": "REAL-TIME DETERMINISTISCHE ARBITRAGE ENGINE",
        "t_sim_title": "Interactieve FinOps Simulator: Tokens & Workflows",
        "t_sim_desc": "Pas verkeersvolumes aan om directe maand- en jaarkosten inclusief nauwkeurige besparing te berekenen.",
        "t_currency": "Valuta",
        "t_presets": "Profielen",
        "t_preset_startup": "Startup",
        "t_preset_growth": "Groei",
        "t_preset_scale": "Enterprise",
        "t_daily_requests": "API-verzoeken / Dag",
        "t_avg_input_tokens": "Gem. Input Tokens",
        "t_avg_output_tokens": "Gem. Output Tokens",
        "t_monthly_ops": "Maandelijkse Operaties",
        "t_annual_savings_title": "Berekende Jaarlijkse Besparing",
        "t_savings_subtext": "Besparing door overstap van dure SaaS naar geoptimaliseerde modellen en self-hosted n8n.",
        "t_arbitrage_cta": "Start FinOps Arbitrage",
        "t_year": "jr",
        "t_saved": "bespaard",
        "t_tab_llm": "LLM Kostenmatrix",
        "t_tab_automation": "Automatisering (Zapier vs n8n / Make)",
        "t_col_model": "Model",
        "t_col_provider": "Leverancier",
        "t_col_input_m": "Input / 1M",
        "t_col_output_m": "Output / 1M",
        "t_col_monthly_cost": "Maandelijkse Kosten",
        "t_col_annual_cost": "Jaarlijkse Kosten",
        "t_col_arbitrage": "Besparing vs Top",
        "t_col_solution": "Oplossing",
        "t_col_type": "Architectuur",
        "t_col_delta": "Verschil vs Zapier",
        "t_col_action": "Deploy",
        "t_open_calculator": "Start Calculator",
        "t_calculators_hub_title": "Gespecialiseerde B2B FinOps Calculators"
    },
    "ja": {
        "nav_llm_calc": "LLMコスト計算機",
        "nav_automation_calc": "自動化コスト比較",
        "nav_rag_calc": "ベクトルDB / RAG",
        "t_nav_calculators": "計算機とアービトラージ",
        "t_footer_tagline": "AI API費用、トークン経済学、自動化インフラのリアルタイム決定論的計算エンジン。",
        "t_live_engine": "リアルタイム決定論的アービトラージエンジン",
        "t_sim_title": "対話型FinOpsトークン＆ワークフローシミュレータ",
        "t_sim_desc": "本番環境のリクエスト数とトークン数を設定すると、月次・年次のAPIコストと削減可能額を即座に計算します。",
        "t_currency": "通貨",
        "t_presets": "プリセット",
        "t_preset_startup": "スタートアップ",
        "t_preset_growth": "成長フェーズ",
        "t_preset_scale": "大規模エンタープライズ",
        "t_daily_requests": "日次APIリクエスト数",
        "t_avg_input_tokens": "平均入力トークン数",
        "t_avg_output_tokens": "平均出力トークン数",
        "t_monthly_ops": "月間ワークフロー実行数",
        "t_annual_savings_title": "計算された年間削減可能額",
        "t_savings_subtext": "高額なプロプライエタリSaaSから最適化モデルおよびVPSセルフホスト型n8nへの移行による年間コスト削減効果。",
        "t_arbitrage_cta": "コスト最適化を実行する",
        "t_year": "年",
        "t_saved": "削減",
        "t_tab_llm": "LLMモデル別コスト比較",
        "t_tab_automation": "自動化ツール比較 (Zapier vs n8n / Make)",
        "t_col_model": "モデルと仕様",
        "t_col_provider": "提供企業",
        "t_col_input_m": "入力 / 100万トークン",
        "t_col_output_m": "出力 / 100万トークン",
        "t_col_monthly_cost": "月額費用",
        "t_col_annual_cost": "年額費用",
        "t_col_arbitrage": "最上位モデルとの差額",
        "t_col_solution": "プラットフォーム",
        "t_col_type": "デプロイ形態",
        "t_col_delta": "Zapier比の削減額",
        "t_col_action": "構築・導入",
        "t_open_calculator": "シミュレータを開く",
        "t_calculators_hub_title": "高意思決定向け特化型FinOps計算エンジン"
    }
}

# Specialized Topics Metadata per language
TOPIC_PAGES = [
    {
        "slug": "claude-vs-gpt-vs-gemini-pricing-calculator",
        "category": "llm",
        "titles": {
            "en": "Claude 3.5 vs GPT-4o vs Gemini 1.5 API Cost Calculator",
            "fr": "Calculateur Coûts API Claude 3.5 vs GPT-4o vs Gemini 1.5",
            "de": "Claude 3.5 vs GPT-4o vs Gemini 1.5 API-Kostenrechner",
            "es": "Calculadora de Costes API Claude 3.5 vs GPT-4o vs Gemini 1.5",
            "it": "Calcolatore Costi API Claude 3.5 vs GPT-4o vs Gemini 1.5",
            "pt": "Calculadora de Custos API Claude 3.5 vs GPT-4o vs Gemini 1.5",
            "nl": "Claude 3.5 vs GPT-4o vs Gemini 1.5 API Kosten Calculator",
            "ja": "Claude 3.5 vs GPT-4o vs Gemini 1.5 APIコスト計算機"
        },
        "highlight": {
            "en": "Token Economics for 10k Calls/Day",
            "fr": "Token Economics pour 10 000 Appels/Jour",
            "de": "Token-Ökonomie für 10.000 Anfragen/Tag",
            "es": "Economía de Tokens para 10k Peticiones/Día",
            "it": "Economia dei Token per 10k Chiamate/Giorno",
            "pt": "Economia de Tokens para 10k Chamadas/Dia",
            "nl": "Token Economics voor 10k Verzoeken/Dag",
            "ja": "1日1万リクエストにおけるトークン経済学"
        },
        "meta_desc": {
            "en": "Compare production API pricing between Claude 3.5 Sonnet, OpenAI GPT-4o, and Gemini 1.5 Flash. Real-time cost simulation at cent-level accuracy.",
            "fr": "Comparez les coûts de production entre Claude 3.5 Sonnet, GPT-4o et Gemini 1.5. Simulation en temps réel au centime près selon votre volume de tokens.",
            "de": "Vergleichen Sie Produktions-API-Kosten zwischen Claude 3.5 Sonnet, GPT-4o und Gemini 1.5 Flash in Echtzeit.",
            "es": "Compare los precios de API de producción entre Claude 3.5 Sonnet, GPT-4o y Gemini 1.5 Flash con precisión matemática.",
            "it": "Confronta i costi di produzione tra Claude 3.5 Sonnet, GPT-4o e Gemini 1.5 con simulazione in tempo reale.",
            "pt": "Compare custos reais de API entre Claude 3.5 Sonnet, GPT-4o e Gemini 1.5 Flash com precisão ao centavo.",
            "nl": "Vergelijk productie API-kosten tussen Claude 3.5 Sonnet, GPT-4o en Gemini 1.5 Flash in real-time.",
            "ja": "Claude 3.5 Sonnet、OpenAI GPT-4o、Gemini 1.5の本番APIコストを比較。トークン量に応じたリアルタイム計算。"
        },
        "primary_cta_partner": "hostinger",
        "secondary_cta_partner": "n8n"
    },
    {
        "slug": "zapier-vs-make-vs-n8n-cost-arbitrage",
        "category": "automation",
        "titles": {
            "en": "Zapier vs Make vs Self-Hosted n8n Real Monthly Cost Arbitrage",
            "fr": "Arbitrage Financier Réel : Zapier vs Make vs n8n Auto-Hébergé",
            "de": "Kosten-Arbitrage: Zapier vs Make vs n8n Self-Hosted",
            "es": "Arbitraje de Costes Reales: Zapier vs Make vs n8n Autoalojado",
            "it": "Arbitraggio Costi Mensili: Zapier vs Make vs n8n Self-Hosted",
            "pt": "Arbitragem de Custos: Zapier vs Make vs n8n Auto-Hospedado",
            "nl": "Zapier vs Make vs Self-Hosted n8n Echte Kosten Arbitrage",
            "ja": "Zapier vs Make vs セルフホスト型n8n 実際の月額費用アービトラージ"
        },
        "highlight": {
            "en": "Save up to $5,000+ / Year on Workflow Tasks",
            "fr": "Économisez jusqu'à 5 000 €+ / An sur vos Workflows",
            "de": "Sparen Sie bis zu 5.000 € / Jahr bei Automatisierungen",
            "es": "Ahorre hasta 5.000 € / Año en Tareas de Automatización",
            "it": "Risparmia fino a 5.000 € / Anno sui Workflow",
            "pt": "Poupe até $5.000+ / Ano em Tarefas de Automação",
            "nl": "Bespaar tot $5.000+ / Jaar op Workflowtaken",
            "ja": "ワークフロー実行コストを年間最大5,000ドル以上削減"
        },
        "meta_desc": {
            "en": "Stop paying 3.8 cents per task on Zapier. Calculate the exact break-even point of migrating to Make or running n8n on a $6.99/mo Hostinger VPS.",
            "fr": "Cessez de payer 0,038 $ par tâche sur Zapier. Calculez le seuil exact de bascule vers Make ou n8n sur VPS Hostinger à 6,99 €/mois.",
            "de": "Zahlen Sie nicht mehr 0,038 $ pro Task bei Zapier. Berechnen Sie den Break-Even-Point beim Wechsel zu Make oder n8n auf Hostinger VPS.",
            "es": "Deje de pagar tarifas abusivas por tarea en Zapier. Calcule el punto de equilibrio para migrar a Make o n8n en un VPS Hostinger.",
            "it": "Smetti di pagare a consumo su Zapier. Calcola il break-even point migrando a Make o n8n su VPS Hostinger.",
            "pt": "Pare de pagar caro por tarefa no Zapier. Calcule o ponto de equilíbrio exato ao migrar para Make ou n8n em VPS Hostinger.",
            "nl": "Stop met het betalen van hoge taakkosten op Zapier. Bereken het break-even punt bij overstap naar Make of n8n op een Hostinger VPS.",
            "ja": "Zapierのタスク従量課金を見直し。Makeや月額6.99ユーロのHostinger VPS上n8nセルフホストへの損益分岐点を計算。"
        },
        "primary_cta_partner": "hostinger",
        "secondary_cta_partner": "make"
    },
    {
        "slug": "deepseek-r1-vs-openai-o1-cost-savings",
        "category": "reasoning",
        "titles": {
            "en": "DeepSeek R1 vs OpenAI o1 Reasoning API Cost Arbitrage",
            "fr": "DeepSeek R1 vs OpenAI o1 : Économie Réelle sur les Modèles de Raisonnement",
            "de": "DeepSeek R1 vs OpenAI o1: Reasoning-Kostenvergleich",
            "es": "DeepSeek R1 vs OpenAI o1: Ahorro en Modelos de Razonamiento",
            "it": "DeepSeek R1 vs OpenAI o1: Confronto Costi Modelli di Ragionamento",
            "pt": "DeepSeek R1 vs OpenAI o1: Economia em Modelos de Raciocínio",
            "nl": "DeepSeek R1 vs OpenAI o1: Reasoning API Kostenvergelijking",
            "ja": "DeepSeek R1 vs OpenAI o1 推論モデルのAPIコスト削減比較"
        },
        "highlight": {
            "en": "90%+ Cost Reduction on Chain-of-Thought",
            "fr": "Réduction de 90%+ sur les Tokens de Raisonnement",
            "de": "Über 90% Kostenersparnis bei Chain-of-Thought",
            "es": "Más del 90% de Ahorro en Razonamiento IA",
            "it": "Oltre il 90% di Risparmio sui Token di Ragionamento",
            "pt": "Mais de 90% de Redução em Raciocínio Profundo",
            "nl": "Meer dan 90% Kostenreductie op Reasoning Tokens",
            "ja": "思考プロセス（Chain-of-Thought）トークンを90%以上コストカット"
        },
        "meta_desc": {
            "en": "DeepSeek R1 costs $0.55 / $2.19 per million tokens compared to OpenAI o1 at $15 / $60. Discover exact annual enterprise savings.",
            "fr": "DeepSeek R1 coûte 0,55 $ / 2,19 $ par million de tokens contre 15 $ / 60 $ pour OpenAI o1. Mesurez l'économie annuelle pour votre entreprise.",
            "de": "DeepSeek R1 kostet 0,55 $ / 2,19 $ pro Million Token im Vergleich zu OpenAI o1 (15 $ / 60 $). Berechnen Sie die jährliche Ersparnis.",
            "es": "DeepSeek R1 cuesta 0,55 $ / 2,19 $ por millón frente a OpenAI o1 (15 $ / 60 $). Descubra el ahorro empresarial exacto.",
            "it": "DeepSeek R1 costa 0,55 $ / 2,19 $ per milione contro i 15 $ / 60 $ di OpenAI o1. Scopri il risparmio annuo aziendale.",
            "pt": "DeepSeek R1 custa 0,55 $ / 2,19 $ por milhão contra 15 $ / 60 $ do OpenAI o1. Veja a economia anual real.",
            "nl": "DeepSeek R1 kost $0,55 / $2,19 per miljoen tokens tegenover OpenAI o1 ($15 / $60). Bereken enterprise besparingen.",
            "ja": "OpenAI o1（15ドル/60ドル）に対してDeepSeek R1は0.55ドル/2.19ドル。企業における年間コスト差を精密試算。"
        },
        "primary_cta_partner": "deepseek",
        "secondary_cta_partner": "digitalocean"
    },
    {
        "slug": "rag-vector-database-supabase-vs-pinecone",
        "category": "database",
        "titles": {
            "en": "RAG Vector Database Cost Comparison: Supabase vs Pinecone",
            "fr": "Comparatif Coût Base Vectorielle RAG : Supabase pgvector vs Pinecone",
            "de": "RAG-Vektordatenbank Kostenvergleich: Supabase vs Pinecone",
            "es": "Comparativa de Costes de Bases Vectoriales RAG: Supabase vs Pinecone",
            "it": "Confronto Costi Database Vettoriali RAG: Supabase vs Pinecone",
            "pt": "Comparativo de Custos de Banco Vetorial RAG: Supabase vs Pinecone",
            "nl": "RAG Vector Database Kostenvergelijking: Supabase vs Pinecone",
            "ja": "RAGベクトルデータベース費用比較：Supabase pgvector vs Pinecone"
        },
        "highlight": {
            "en": "Flat $25 Compute vs Per-Query Read Units",
            "fr": "Forfait 25 $ Fixe vs Facturation à la Requête",
            "de": "Feste 25 $ Compute vs. Abfrage-Mikrogebühren",
            "es": "Tarifa Plana de 25 $ vs Facturación por Consulta",
            "it": "Tariffa Fissa 25 $ vs Costo a Query",
            "pt": "Custo Fixo de $25 vs Cobrança por Consulta",
            "nl": "Vaste $25 Compute vs Per-Query Kosten",
            "ja": "定額25ドルコンピュート vs クエリ単位の従量課金"
        },
        "meta_desc": {
            "en": "Should you store vectors in Supabase pgvector or use Pinecone Serverless? Calculate storage, compute, and read query TCO at scale.",
            "fr": "Faut-il stocker vos embeddings dans Supabase pgvector ou Pinecone Serverless ? Calculez le TCO exact selon vos lectures mensuelles.",
            "de": "Supabase pgvector oder Pinecone Serverless für RAG? Berechnen Sie Speicher-, Compute- und Abfragekosten im Maßstab.",
            "es": "¿Conviene usar Supabase pgvector o Pinecone Serverless? Calcule el TCO exacto de almacenamiento y lectura a escala.",
            "it": "Meglio archiviare i vettori in Supabase pgvector o Pinecone Serverless? Calcola il TCO esatto tra storage e query.",
            "pt": "Vale mais a pena usar Supabase pgvector ou Pinecone Serverless? Calcule o custo total de posse (TCO) para sua carga de busca.",
            "nl": "Kies voor Supabase pgvector of Pinecone Serverless. Bereken storage, compute en zoekquery TCO op schaal.",
            "ja": "RAG構築においてSupabase pgvectorかPinecone Serverlessか。ストレージとクエリ回数による総所有コスト（TCO）を算出。"
        },
        "primary_cta_partner": "supabase",
        "secondary_cta_partner": "pinecone"
    }
]


def load_partners() -> Dict[str, Any]:
    with open(PARTNERS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def load_settings() -> Dict[str, Any]:
    with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def build_sitemap_xml(base_url: str, urls: List[str]) -> str:
    """Generates standard compliant XML sitemap."""
    lines = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for u in urls:
        lines.append("  <url>")
        lines.append(f"    <loc>{u}</loc>")
        lines.append("    <changefreq>daily</changefreq>")
        lines.append("    <priority>0.8</priority>")
        lines.append("  </url>")
    lines.append("</urlset>")
    return "\n".join(lines)


def build_robots_txt(base_url: str) -> str:
    """Generates robots.txt with sitemap reference."""
    return f"""User-agent: *
Allow: /

Sitemap: {base_url}/sitemap.xml
"""


def generate_static_site(pricing_matrix: Dict[str, Any]):
    """
    Main autonomous generator loop:
    - Loads templates from templates/
    - Renders index and specialized pages across all 8 languages
    - Embeds live synced JSON matrix directly in every page for offline speed
    - Generates sitemap.xml and robots.txt in docs/
    """
    partners = load_partners()
    settings = load_settings()
    base_url = settings.get("base_url", "https://Thorlan04.github.io/ai-finops-cost-oracle").rstrip("/")

    env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(str(TEMPLATES_DIR)),
        autoescape=jinja2.select_autoescape(["html", "xml"])
    )

    DOCS_DIR.mkdir(parents=True, exist_ok=True)
    generated_urls = []

    pricing_json_str = json.dumps(pricing_matrix, ensure_ascii=False)
    partners_json_str = json.dumps(partners, ensure_ascii=False)

    for lang in LANGUAGES:
        lang_dir = DOCS_DIR / lang
        lang_dir.mkdir(parents=True, exist_ok=True)
        i18n = I18N_STRINGS.get(lang, I18N_STRINGS["en"])
        i18n_json_str = json.dumps(i18n, ensure_ascii=False)

        # -----------------------------------------------------------------
        # 1. Render Language Homepage (docs/{lang}/index.html)
        # -----------------------------------------------------------------
        index_template = env.get_template("index.html")
        canonical_index = f"{base_url}/{lang}/"
        generated_urls.append(canonical_index)

        home_rendered = index_template.render(
            lang=lang,
            base_url=base_url,
            canonical_url=canonical_index,
            page_title=f"AI FinOps Cost Oracle | {i18n['t_sim_title']}",
            meta_description=f"{i18n['t_footer_tagline']} {i18n['t_sim_desc']}",
            hero_badge_text=i18n["t_live_engine"],
            hero_h1_prefix="Zero-Waste" if lang == "en" else "Arbitrage",
            hero_h1_highlight="Token Economics & Cloud VPS",
            hero_h1_suffix="Real-time Financial Oracle",
            hero_p_text=i18n["t_sim_desc"],
            pricing_json_inline=pricing_json_str,
            partners_json_inline=partners_json_str,
            i18n_json_inline=i18n_json_str,
            card_llm_desc="Calculate Claude 3.5 Sonnet, GPT-4o, and Gemini 1.5 costs with millicent accuracy per 1M tokens.",
            card_automation_desc="Break-even analysis: Zapier per-task fees vs Make and self-hosted n8n on a 6.99€/mo VPS.",
            card_reasoning_desc="Arbitrage deep reasoning tokens: DeepSeek R1 open weights vs OpenAI o1 chain-of-thought.",
            card_rag_desc="Vector indexing TCO: Supabase pgvector flat tiers vs Pinecone Serverless query units.",
            section_methodology_title="FinOps Mathematical Architecture & Independence",
            section_methodology_body="This oracle operates on 100% deterministic mathematical calculations refreshed every 6 hours from LiteLLM's public repository. No sponsored rankings, no proprietary lock-in.",
            meth_bullet_1="Zero API Keys needed. Ingests raw open-source GitHub benchmarks directly.",
            meth_bullet_2="Accurate token calculation factoring in prompt-to-completion ratios and active user concurrency.",
            meth_bullet_3="Hosted free on GitHub Pages with continuous GitHub Actions automation.",
            meth_bullet_4="Standard compliant llms.txt and public static API for transparent algorithmic evaluation.",
            partner_n8n_url=partners["partners"]["n8n"]["affiliate_url"],
            partner_hostinger_url=partners["partners"]["hostinger"]["affiliate_url"],
            partner_make_url=partners["partners"]["make"]["affiliate_url"],
            partner_digitalocean_url=partners["partners"]["digitalocean"]["affiliate_url"],
            partner_supabase_url=partners["partners"]["supabase"]["affiliate_url"],
            partner_n8n_hostinger_url=partners["partners"]["hostinger"]["affiliate_url"],
            **i18n
        )

        with open(lang_dir / "index.html", "w", encoding="utf-8") as f:
            f.write(home_rendered)

        # -----------------------------------------------------------------
        # 2. Render Specialized Topic Pages (docs/{lang}/{slug}.html)
        # -----------------------------------------------------------------
        comparison_template = env.get_template("comparison_page.html")
        for topic in TOPIC_PAGES:
            slug = topic["slug"]
            target_file = lang_dir / f"{slug}.html"
            canonical_topic = f"{base_url}/{lang}/{slug}.html"
            generated_urls.append(canonical_topic)

            title = topic["titles"].get(lang, topic["titles"]["en"])
            highlight = topic["highlight"].get(lang, topic["highlight"]["en"])
            meta_desc = topic["meta_desc"].get(lang, topic["meta_desc"]["en"])

            p_cta_key = topic.get("primary_cta_partner", "hostinger")
            s_cta_key = topic.get("secondary_cta_partner", "n8n")
            p_cta = partners["partners"].get(p_cta_key, {})
            s_cta = partners["partners"].get(s_cta_key, {})

            # Dynamic editorial content tailored to topic
            if topic["category"] == "llm":
                arch_lead = "Modern LLM token economics dictate that 70-85% of production inference spend is generated by input context tokens during multi-turn RAG retrieval."
                arch_bullets = [
                    "Input vs Output Disparity: Output tokens are typically 3x to 5x more expensive than input tokens across all frontier providers.",
                    "Prompt Caching Arbitrage: Anthropic and OpenAI support prompt caching, lowering recurring context costs by up to 90%.",
                    "Distillation & Routing: Routing classification queries to Claude 3.5 Haiku or DeepSeek V3 slashes total invoice amounts immediately."
                ]
                math_lead = "The deterministic cost function for an LLM workload over a billing period is:"
                math_formula = "TotalCost = Sum_i [ Calls_i * ( (InTokens_i * Rate_In) + (OutTokens_i * Rate_Out) ) ]"
                recom_title = "FinOps Architectural Recommendation"
                recom_body = "Implement a two-tier semantic router: evaluate user prompts with an ultra-efficient model (Gemini Flash or DeepSeek V3) and escalate only complex synthesis to Claude 3.5 Sonnet or GPT-4o."
                faqs = [
                    {"q": "What is the cheapest flagship LLM for production in 2026?", "a": "DeepSeek V3 and Gemini 1.5 Flash offer the lowest price per 1M tokens ($0.075 to $0.14 input), while Claude 3.5 Sonnet remains the quality benchmark for complex code synthesis."},
                    {"q": "How does prompt caching affect token billing?", "a": "Prompt caching reduces input token costs by up to 90% for repeated prefix contexts, making large system prompts significantly more economical."},
                    {"q": "Can I switch models without changing client code?", "a": "Yes, by utilizing LiteLLM Proxy or an abstraction gateway, you can switch providers via simple environment variables."}
                ]
            elif topic["category"] == "automation":
                arch_lead = "Proprietary cloud automation SaaS platforms penalize multi-step workflows by charging for every single intermediate routing step as a billable 'Task'."
                arch_bullets = [
                    "The Per-Task Trap: A 5-step automation processing 10,000 webhook events consumes 50,000 tasks/month, costing over $448/month on Zapier.",
                    "n8n Fixed Infrastructure: On a dedicated KVM VPS (Hostinger ~6.99€/mo or DigitalOcean $12/mo), execution volume is unlimited.",
                    "Hybrid Orchestration: Use Make for rapid prototype integrations and migrate high-throughput webhooks to self-hosted n8n."
                ]
                math_lead = "The automation arbitrage break-even equation:"
                math_formula = "BreakEven = MonthlyVPSCost / EffectiveCostPerZapierTask (At $7.50/mo and $0.038/task, Break-Even is 197 tasks/month!)"
                recom_title = "Infrastructure Recommendation: Deploy n8n on VPS"
                recom_body = "Deploy n8n via Docker on a Hostinger KVM2 VPS (2 vCPU, 8 GB RAM) at ~6.99€/month. You immediately uncap workflow executions with 98% savings over Zapier."
                faqs = [
                    {"q": "Is self-hosted n8n difficult to maintain?", "a": "No. Running n8n via Docker Compose on Ubuntu takes under 5 minutes, and automated daily backups ensure enterprise reliability."},
                    {"q": "How much can a company save by switching from Zapier to n8n?", "a": "Companies processing 50,000 to 200,000 operations per month typically save between $4,500 and $20,000 per year."},
                    {"q": "Does n8n support webhooks and complex branching?", "a": "Yes, n8n natively handles JavaScript/Python functions, sub-workflows, loops, binary data, and custom webhooks."}
                ]
            elif topic["category"] == "reasoning":
                arch_lead = "Chain-of-thought reasoning models (OpenAI o1 vs DeepSeek R1) generate hidden reasoning tokens that are billed at output token rates."
                arch_bullets = [
                    "Hidden Token Consumption: A complex coding question may generate 4,000 hidden reasoning tokens before outputting 200 code tokens.",
                    "Extreme Pricing Delta: OpenAI o1 charges $60 per million output tokens, whereas DeepSeek R1 charges only $2.19 per million.",
                    "Open Weights Deployment: DeepSeek R1 can be consumed via high-speed API or self-hosted on private GPU clusters for zero-data retention compliance."
                ]
                math_lead = "Reasoning Cost Multiplier formula:"
                math_formula = "TotalReasoningCost = DailyRequests * [ (InTokens * Rate_In) + ((ReasoningTokens + OutTokens) * Rate_Out) ]"
                recom_title = "FinOps Recommendation for Reasoning Workloads"
                recom_body = "Adopt DeepSeek R1 as your default reasoning engine for internal code review, automated testing, and math verification. The 96% cost differential provides immediate capital efficiency."
                faqs = [
                    {"q": "Is DeepSeek R1 comparable to OpenAI o1 in benchmarks?", "a": "Yes, independent benchmarks (AIME, MATH-500, Codeforces) show DeepSeek R1 matches or exceeds OpenAI o1 at a 96% lower API price."},
                    {"q": "Are reasoning tokens billed differently?", "a": "Reasoning tokens are generated by the model during deliberation and are billed as standard output tokens."}
                ]
            else:  # database
                arch_lead = "Vector databases are the foundation of RAG (Retrieval-Augmented Generation), but their billing models differ drastically between flat compute and per-query reads."
                arch_bullets = [
                    "Supabase pgvector: Bundled inside standard PostgreSQL. For $25/month, you get full relational data plus vector similarity search with zero query overage.",
                    "Pinecone Serverless: Charged per Read Unit ($0.25/M) and storage ($0.33/GB). Optimal for small or intermittent workloads, but costs scale with read query volume.",
                    "Index Overhead: HNSW indexes add ~50-70% memory overhead on top of raw embedding dimensions."
                ]
                math_lead = "RAG Total Cost of Ownership formula:"
                math_formula = "TCO_RAG = StorageCost(GB) + ComputeFee + (MonthlyQueries / 1e6 * ReadUnitRate)"
                recom_title = "Architectural Recommendation for Vector RAG"
                recom_body = "If your application already uses a database, consolidate on Supabase pgvector to avoid multi-vendor data synchronization and eliminate per-query API bills."
                faqs = [
                    {"q": "Can pgvector handle millions of vectors?", "a": "Yes, with HNSW indexing and proper memory tuning, pgvector handles tens of millions of embeddings with sub-10ms latency."},
                    {"q": "When is Pinecone Serverless preferable?", "a": "Pinecone is ideal for serverless apps with unpredictable, sparse query traffic where you want zero database management."}
                ]

            topic_rendered = comparison_template.render(
                lang=lang,
                base_url=base_url,
                canonical_url=canonical_topic,
                page_title=title,
                meta_description=meta_desc,
                topic_badge=topic["category"].upper(),
                hero_title_prefix=title,
                hero_title_highlight=highlight,
                hero_title_suffix="",
                hero_subtitle=meta_desc,
                pricing_json_inline=pricing_json_str,
                partners_json_inline=partners_json_str,
                i18n_json_inline=i18n_json_str,
                section_architecture_title="In-Depth Technical Architecture & Token Economics",
                section_architecture_lead=arch_lead,
                architecture_bullets=arch_bullets,
                section_math_title="Deterministic Mathematical Calculation Model",
                section_math_explanation=math_lead,
                math_formula_text=math_formula,
                section_recommendation_title=recom_title,
                section_recommendation_body=recom_body,
                section_faq_title="Frequently Asked Technical & FinOps Questions",
                faqs=faqs,
                primary_cta_text=p_cta.get("cta_text", "Explore Infrastructure"),
                primary_cta_url=p_cta.get("affiliate_url", p_cta.get("url", "#")),
                secondary_cta_text=s_cta.get("cta_text", "Compare Alternatives"),
                secondary_cta_url=s_cta.get("affiliate_url", s_cta.get("url", "#")),
                partner_n8n_url=partners["partners"]["n8n"]["affiliate_url"],
                partner_hostinger_url=partners["partners"]["hostinger"]["affiliate_url"],
                partner_make_url=partners["partners"]["make"]["affiliate_url"],
                partner_digitalocean_url=partners["partners"]["digitalocean"]["affiliate_url"],
                partner_supabase_url=partners["partners"]["supabase"]["affiliate_url"],
                partner_n8n_hostinger_url=partners["partners"]["hostinger"]["affiliate_url"],
                **i18n
            )

            with open(target_file, "w", encoding="utf-8") as f:
                f.write(topic_rendered)

    # -----------------------------------------------------------------
    # 3. Create Root Landing / Redirect (docs/index.html)
    # -----------------------------------------------------------------
    root_index = f"""<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <title>AI FinOps Cost Oracle</title>
  <meta http-equiv="refresh" content="0; url={base_url}/en/">
  <script>
    const userLang = (navigator.language || navigator.userLanguage || 'en').substring(0, 2);
    const supported = ['en','fr','de','es','it','pt','nl','ja'];
    const target = supported.includes(userLang) ? userLang : 'en';
    window.location.replace('{base_url}/' + target + '/');
  </script>
</head>
<body style="background:#090d16; color:#fff; font-family:sans-serif; text-align:center; padding:100px 20px;">
  <h2>Redirecting to AI FinOps Cost Oracle...</h2>
  <p><a href="{base_url}/en/" style="color:#38bdf8;">Click here to continue to English</a> | <a href="{base_url}/fr/" style="color:#38bdf8;">Continuer en Français</a></p>
</body>
</html>"""
    with open(DOCS_DIR / "index.html", "w", encoding="utf-8") as f:
        f.write(root_index)

    # -----------------------------------------------------------------
    # 4. Generate sitemap.xml and robots.txt
    # -----------------------------------------------------------------
    sitemap_xml = build_sitemap_xml(base_url, generated_urls)
    with open(DOCS_DIR / "sitemap.xml", "w", encoding="utf-8") as f:
        f.write(sitemap_xml)

    robots_txt = build_robots_txt(base_url)
    with open(DOCS_DIR / "robots.txt", "w", encoding="utf-8") as f:
        f.write(robots_txt)

    logger.info(f"Static site generation complete: {len(generated_urls)} unique canonical URLs published in docs/")
    return len(generated_urls)


if __name__ == "__main__":
    from pricing_sync_engine import synchronize_pricing_matrix
    pricing = synchronize_pricing_matrix()
    total_pages = generate_static_site(pricing)
    print(f"[OK] Static site successfully generated: {total_pages} pages in docs/")
