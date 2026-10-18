#!/usr/bin/env python3
"""
AI FinOps Cost Oracle - Module Fiscal Micro-Entreprise BNC
Livre des Recettes Chronologique & Simulateur Déclaration Fiscale 2042-C-PRO (Cases 5HQ / 5TE)
Conforme aux articles L. 123-12 du Code de commerce et 286 du Code Général des Impôts (CGI).
"""

import argparse
import csv
import json
import os
import sys
from datetime import datetime
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path
from typing import Any, Dict, List

BASE_DIR = Path(__file__).resolve().parent
RECETTES_FILE = BASE_DIR / "recettes_template.json"
EXPORT_CSV_FILE = BASE_DIR / "livre_des_recettes_officiel.csv"


def round_cur(val: float) -> float:
    return float(Decimal(str(val)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))


def load_recettes_data() -> Dict[str, Any]:
    if not RECETTES_FILE.exists():
        raise FileNotFoundError(f"Fichier de recettes introuvable : {RECETTES_FILE}")
    with open(RECETTES_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_recettes_data(data: Dict[str, Any]):
    with open(RECETTES_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def compute_fiscal_summary(data: Dict[str, Any]) -> Dict[str, Any]:
    recettes = data.get("recettes", [])
    total_ca_eur = sum(r.get("montant_encaisse_eur", 0.0) for r in recettes)
    total_ca_eur = round_cur(total_ca_eur)

    plafond_bnc = float(data.get("plafond_micro_bnc_eur", 77700.0))
    seuil_tva_base = float(data.get("seuil_franchise_tva_base_eur", 36800.0))
    seuil_tva_majore = float(data.get("seuil_franchise_tva_majore_eur", 39100.0))

    taux_urssaf = float(data.get("taux_cotisations_urssaf", 0.211))
    abattement_bnc = float(data.get("abattement_forfaitaire_bnc", 0.34))
    taux_liberatoire = float(data.get("taux_versement_liberatoire", 0.022))

    # Cotisations sociales URSSAF
    cotisations_urssaf = round_cur(total_ca_eur * taux_urssaf)

    # Déclaration Fiscale - Option 1 : Régime Classique Micro-BNC (Case 5HQ)
    # L'administration fiscale applique automatiquement l'abattement forfaitaire de 34%
    abattement_montant = round_cur(total_ca_eur * abattement_bnc)
    revenu_net_imposable_5hq = round_cur(total_ca_eur - abattement_montant)

    # Déclaration Fiscale - Option 2 : Option pour le Versement Libératoire (Case 5TE)
    # Impôt payé directement à l'URSSAF lors des déclarations périodiques (2,2% du CA)
    montant_versement_liberatoire_5te = round_cur(total_ca_eur * taux_liberatoire)

    # Statut TVA
    depassement_tva = total_ca_eur > seuil_tva_base
    franchise_active = not depassement_tva

    # Plafond micro
    pct_plafond_consomme = round((total_ca_eur / plafond_bnc) * 100, 2)

    return {
        "annee": data.get("fiscal_year", 2026),
        "total_ca_encaisse_eur": total_ca_eur,
        "nombre_recettes": len(recettes),
        "cotisations_urssaf_estimees_eur": cotisations_urssaf,
        "case_5hq_ca_brut_a_declarer_eur": total_ca_eur,
        "abattement_fiscal_34pct_eur": abattement_montant,
        "revenu_net_fiscal_imposable_eur": revenu_net_imposable_5hq,
        "case_5te_versement_liberatoire_eur": montant_versement_liberatoire_5te,
        "statut_tva": "Franchise en base (TVA non applicable, art. 293 B du CGI)" if franchise_active else "ATTENTION : Seuil franchise TVA dépassé (facturation TVA requise)",
        "reste_avant_seuil_tva_eur": max(0.0, round_cur(seuil_tva_base - total_ca_eur)),
        "reste_avant_plafond_bnc_eur": max(0.0, round_cur(plafond_bnc - total_ca_eur)),
        "pourcentage_plafond_consomme": pct_plafond_consomme
    }


def export_to_csv(data: Dict[str, Any]):
    recettes = data.get("recettes", [])
    headers = [
        "ID", "Date Encaissement", "Référence Pièce", "Client / Débiteur", "Pays",
        "Nature Prestation", "Mode Règlement", "Montant Devise ($)", "Taux Change",
        "Montant Encaissé (€)", "Mention Légale TVA", "Case 5HQ", "Case 5TE"
    ]
    with open(EXPORT_CSV_FILE, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f, delimiter=";")
        writer.writerow(headers)
        for r in recettes:
            writer.writerow([
                r.get("id"),
                r.get("date_encaissement"),
                r.get("reference_piece"),
                r.get("client"),
                r.get("pays"),
                r.get("nature"),
                r.get("mode_reglement"),
                f"{r.get('montant_devise_origine_usd', 0.0):.2f}",
                r.get("taux_change"),
                f"{r.get('montant_encaisse_eur', 0.0):.2f}",
                r.get("tva_applicable"),
                r.get("case_fiscale_principale", "5HQ"),
                r.get("case_fiscale_versement_liberatoire", "5TE")
            ])
    print(f"[OK] Livre des recettes légal exporté au format CSV : {EXPORT_CSV_FILE}")


def display_terminal_report(summary: Dict[str, Any]):
    print("\n" + "="*70)
    print("   AI FINOPS COST ORACLE - RAPPORT FISCAL MICRO-ENTREPRISE BNC")
    print("="*70)
    print(f" Année Fiscale : {summary['annee']} | Activité Libérale Non Réglementée (BNC)")
    print(f" Chiffre d'Affaires Brut Encaissé : {summary['total_ca_encaisse_eur']:,.2f} €")
    print(f" Nombre d'encaissements comptabilisés : {summary['nombre_recettes']}")
    print("-" * 70)
    print(" 1. COTISATIONS SOCIALES URSSAF (Déclarations Mensuelles / Trimestrielles) :")
    print(f"    -> Taux légal Micro-BNC : 21.1 %")
    print(f"    -> Montant Cotisations à régler : {summary['cotisations_urssaf_estimees_eur']:,.2f} €")
    print("-" * 70)
    print(" 2. DÉCLARATION ANNUELLE DES REVENUS (Formulaire 2042-C-PRO) :")
    print(f"    [OPTION A] Régime Micro-BNC classique (Sans option versement libératoire) :")
    print(f"       -> Case à remplir : [ 5HQ ] = {summary['case_5hq_ca_brut_a_declarer_eur']:,.2f} €")
    print(f"       -> Abattement forfaitaire légal DGFIP (34 %) : - {summary['abattement_fiscal_34pct_eur']:,.2f} €")
    print(f"       -> Base nette imposable au barème de l'IR : {summary['revenu_net_fiscal_imposable_eur']:,.2f} €")
    print()
    print(f"    [OPTION B] Option pour le Versement Libératoire de l'IR :")
    print(f"       -> Case à remplir : [ 5TE ] = {summary['case_5hq_ca_brut_a_declarer_eur']:,.2f} €")
    print(f"       -> Prélèvement fiscal libératoire payé à l'URSSAF (2.2 %) : {summary['case_5te_versement_liberatoire_eur']:,.2f} €")
    print("-" * 70)
    print(" 3. CONTRÔLE DES SEUILS LÉGAUX :")
    print(f"    - Plafond Annuel Micro-BNC (77 700 €) : {summary['pourcentage_plafond_consomme']} % consommé")
    print(f"      Marge restante : {summary['reste_avant_plafond_bnc_eur']:,.2f} €")
    print(f"    - Seuil Franchise TVA (36 800 €) : {summary['statut_tva']}")
    print(f"      Marge restante avant TVA : {summary['reste_avant_seuil_tva_eur']:,.2f} €")
    print("="*70 + "\n")


if __name__ == "__main__":
    data = load_recettes_data()
    summary = compute_fiscal_summary(data)
    display_terminal_report(summary)
    export_to_csv(data)
