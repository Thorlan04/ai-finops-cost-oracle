# ⚡ AI FinOps Cost Oracle

> **Calculateur Mathématique Temps Réel & Comparateur d'Arbitrage des Coûts d'API IA (LLM), d'Hébergement GPU/VPS et d'Automatisation (Make / n8n / Zapier) en 8 langues, 100% autonome et hébergé gratuitement sur GitHub Pages.**

[![Autonomous 24h Sync](https://github.com/Thorlan04/ai-finops-cost-oracle/actions/workflows/daily_sync_and_generate.yml/badge.svg)](https://github.com/Thorlan04/ai-finops-cost-oracle/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Pricing Sync](https://img.shields.io/badge/LiteLLM-Live%20Sync%20(0€)-10b981.svg)](https://github.com/BerriAI/litellm)
[![Languages](https://img.shields.io/badge/Languages-8%20i18n-8b5cf6.svg)](#)

---

## 🎯 Vision & Modèle Économique

`ai-finops-cost-oracle` ne vend aucun produit physique ni abonnement payant. C'est une **infrastructure d'autorité logicielle et d'arbitrage financier** qui résout la problématique n°1 des entreprises adoptant l'IA : **l'explosion incontrôlée des factures de tokens LLM et des outils d'automatisation SaaS.**

Le projet génère des revenus d'affiliation B2B passifs et récurrents (PartnerStack, Impact.com, Hostinger, Make, DigitalOcean) via des recommandations purement mathématiques et déterministes.

---

## 🚀 Fonctionnalités Clés

### 1. Synchronisation Quotidienne 0 € & Sans Clé (`src/pricing_sync_engine.py`)
- Se connecte gratuitement chaque jour au dépôt de référence mondial open-source de **LiteLLM** (`BerriAI/litellm`) pour ingérer les tarifs au million de tokens de plus de 4 000 modèles (OpenAI, Anthropic Claude, Google Gemini, Mistral, DeepSeek, Meta Llama, Cohere).
- Base locale de secours robuste (`data/Verified_AI_And_Cloud_Pricing.json`) en cas de défaillance réseau.
- Exposition d'une API statique publique consommable par les agents IA : `docs/api/v1/llm-pricing-matrix.json`.

### 2. Moteur Mathématique Déterministe (`src/finops_calculator.py`)
- Calcul au centime près du coût mensuel et annuel selon les requêtes journalières et la distribution de tokens entrée/sortie.
- **Arbitrage d'Automatisation :** calcul du coût exact de Zapier vs Make vs n8n Cloud vs **n8n Auto-hébergé sur VPS (Hostinger ~6,99 €/mois)**.
- Calcul automatique du **Point de Bascule Financier (*Break-Even Point*)** et de l'économie annuelle maximale.

### 3. Simulateur FinOps Interactif Multilingue en 8 Langues (`src/agent_generator.py`)
- Interface réactive en Vanilla JS (zéro latence, 0 dépendance CDN obligatoire) avec curseurs interactifs.
- Bandeau vert vif : **"Économie annuelle calculée : X € / an"** mis à jour en temps réel.
- Génération autonome de 40 pages web dans `docs/` en 8 langues :
  - 🇬🇧 Anglais (`en`)
  - 🇫🇷 Français (`fr`)
  - 🇩🇪 Allemand (`de`)
  - 🇪🇸 Espagnol (`es`)
  - 🇮🇹 Italien (`it`)
  - 🇵🇹 Portugais (`pt`)
  - 🇳🇱 Néerlandais (`nl`)
  - 🇯🇵 Japonais (`ja`)
- Redirections B2B configurables dans un fichier unique : `config/partners.json`.

### 4. Mégaphone IA & SEO/GEO (`src/ai_megaphone.py`)
- Génération automatique des standards **`docs/llms.txt`** et **`docs/llms-full.txt`** pour que ChatGPT Search, Perplexity, Claude et Cursor citent le site comme source officielle de référence.
- Envoi instantané des URLs à l'API **IndexNow** (Bing, Copilot, ChatGPT Search).
- Publication de synthèses techniques sur **Telegra.ph** et archivage sur **Archive.org**.

### 5. Module Fiscal Micro-Entreprise BNC (`compta_impots/`)
- Tenue du **Livre des Recettes chronologique** (conforme aux articles L. 123-12 du Code de commerce et 286 du CGI).
- Tableau de bord HTML local (`compta_impots/dashboard_bnc.html`) avec suivi des seuils de franchise en base de TVA (36 800 €) et plafond Micro-BNC (77 700 €).
- Feuille de calcul pré-remplie pour la déclaration fiscale annuelle **2042-C-PRO** :
  - **Case `5HQ`** : Régime micro-BNC classique (application de l'abattement forfaitaire de 34 %).
  - **Case `5TE`** : Option pour le versement libératoire de l'IR (2,2 %).
- **`GUIDE_MONETISATION_PARTNERSTACK_RIB.md`** : Guide pas-à-pas en 5 minutes pour relier son RIB français et son formulaire fiscal W-8BEN (0% retenue US).

---

## 📁 Architecture du Projet

```
d:\ai-finops-cost-oracle\
├── .github/
│   └── workflows/
│       └── daily_sync_and_generate.yml   # Workflow GitHub Actions autonome (toutes les 6h)
├── config/
│   ├── partners.json                     # Liens d'affiliation et partenaires commerciaux
│   └── settings.json                     # Configuration générale du site
├── data/
│   └── Verified_AI_And_Cloud_Pricing.json# Base de secours vérifiée (LLMs, Zapier, Make, n8n, Supabase)
├── src/
│   ├── __init__.py
│   ├── pricing_sync_engine.py            # Connecteur LiteLLM (0 € & sans clé)
│   ├── finops_calculator.py              # Moteur mathématique déterministe
│   ├── agent_generator.py                # Générateur multilingue (8 langues)
│   └── ai_megaphone.py                   # Générateur llms.txt & IndexNow
├── templates/
│   ├── base.html                         # Layout moderne responsive Dark FinOps
│   ├── finops_simulator.html             # Composant simulateur interactif Vanilla JS
│   ├── comparison_page.html              # Template comparatif B2B haute intention
│   └── index.html                        # Template hub d'accueil multilingue
├── compta_impots/
│   ├── livre_recettes.py                 # Script CLI de gestion comptable Micro-BNC
│   ├── dashboard_bnc.html                # Tableau de bord fiscal interactif HTML
│   ├── recettes_template.json            # Base des encaissements
│   └── GUIDE_MONETISATION_PARTNERSTACK_RIB.md # Guide 5 min RIB & W-8BEN
├── docs/                                 # Cible du déploiement GitHub Pages
│   ├── en/, fr/, de/, es/, it/, pt/, nl/, ja/
│   ├── api/v1/llm-pricing-matrix.json
│   ├── llms.txt & llms-full.txt
│   ├── sitemap.xml & robots.txt
│   └── index.html
├── build.py                              # Orchestrateur de build global
├── requirements.txt
└── README.md
```

---

## 🛠️ Installation & Lancement en Local

### Prérequis
- Python 3.9+ (Windows, macOS ou Linux)

### 1. Installation
```bash
git clone https://github.com/Thorlan04/ai-finops-cost-oracle.git
cd ai-finops-cost-oracle
pip install -r requirements.txt
```

### 2. Lancer le Build Complet
```bash
python build.py
```

Le script exécute en quelques secondes :
1. La synchronisation LiteLLM.
2. La génération des 40 pages multilingues dans `docs/`.
3. La création de `docs/llms.txt`, `docs/llms-full.txt` et `docs/api/v1/llm-pricing-matrix.json`.
4. La notification IndexNow.
5. L'audit fiscal Micro-BNC.

### 3. Visualiser le Site en Local
```bash
python -m http.server 8000 --directory docs
```
Ouvrez votre navigateur sur : `http://localhost:8000/en/` ou `http://localhost:8000/fr/`.

---

## 🌐 Déploiement Gratuit sur GitHub Pages

1. Créez un dépôt sur GitHub et poussez le code :
   ```bash
   git init
   git add .
   git commit -m "feat: initial commit AI FinOps Cost Oracle"
   git remote add origin https://github.com/Thorlan04/ai-finops-cost-oracle.git
   git push -u origin main
   ```
2. Dans les paramètres de votre dépôt GitHub (**Settings** &rarr; **Pages**) :
   - **Source :** *Deploy from a branch*
   - **Branch :** `main`
   - **Folder :** `/docs`
   - Cliquez sur **Save**.
3. Votre site est immédiatement en ligne, sécurisé en HTTPS et mis à jour automatiquement toutes les 6 heures par le workflow GitHub Actions !

---

## ⚖️ Licence
Distribué sous licence **MIT**. Libre de réutilisation, de modification et de déploiement commercial.
