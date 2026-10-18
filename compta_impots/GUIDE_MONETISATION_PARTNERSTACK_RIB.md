# Guide de Monétisation B2B & Raccordement Bancaire (5 Minutes Chrono)
> **AI FinOps Cost Oracle** – Encaissement des virements SEPA d'affiliation internationale (PartnerStack, Impact.com) et conformité fiscale Micro-Entreprise BNC.

---

## 1. Où coller ses identifiants et liens d'affiliation dans le projet ? (1 Minute)

Toutes les URLs et tags de suivi d'affiliation sont centralisés dans un seul et unique fichier :
📂 `config/partners.json`

Ouvrez ce fichier et remplacez les valeurs de `affiliate_url` par vos propres liens de tracking :
```json
{
  "partners": {
    "hostinger": {
      "affiliate_url": "https://www.hostinger.com/vps-hosting?ref=VOTRE_IDENTIFIANT"
    },
    "n8n": {
      "affiliate_url": "https://n8n.partnerlinks.io/VOTRE_CODE_PARTNERSTACK"
    },
    "make": {
      "affiliate_url": "https://www.make.com/en/register?pc=VOTRE_CODE_IMPACT"
    },
    "digitalocean": {
      "affiliate_url": "https://m.do.co/c/VOTRE_REF_DIGITALOCEAN"
    },
    "supabase": {
      "affiliate_url": "https://supabase.com/?utm_source=VOTRE_TAG"
    }
  }
}
```
Dès la prochaine régénération automatique (toutes les 6h ou via `python build.py`), **toutes les 40 pages et les 8 langues** pointeront instantanément vers vos liens monétisés.

---

## 2. Configuration du Virement SEPA sur PartnerStack (2 Minutes)

PartnerStack gère les programmes partenaires de **n8n, ElevenLabs, Webflow, Notion, etc.**

1. Connectez-vous sur votre espace affilié : [https://dash.partnerstack.com/](https://dash.partnerstack.com/)
2. Rendez-vous dans **Settings** (Paramètres) &rarr; **Payouts** (Paiements).
3. Cliquez sur **Add Payout Provider** &rarr; Choisissez **Direct Deposit / Bank Transfer (Powered by Stripe)**.
4. Renseignez votre identité professionnelle :
   - **Pays :** France 🇫🇷
   - **Nom de l'entreprise ou Nom/Prénom :** Identique à votre Kbis / déclaration INSEE d'auto-entrepreneur.
   - **Devise de versement :** Sélectionnez **EUR (€)** (pour éviter tout frais de change de votre banque française).
   - **IBAN :** Renseignez votre IBAN français (`FR76...`).
   - **BIC / SWIFT :** Code BIC de votre banque.
5. Définissez le versement automatique : activez le seuil minimum de virement (ex: 25 $ ou 50 $), PartnerStack versera automatiquement les fonds chaque mois directement sur votre compte bancaire français via le réseau SEPA.

---

## 3. Configuration du Virement Bancaire sur Impact.com (1 Minute)

Impact.com gère l'affiliation de **Hostinger, Make, DigitalOcean, Canva, etc.**

1. Connectez-vous à la console : [https://app.impact.com/](https://app.impact.com/)
2. En bas à gauche, cliquez sur la roue crantée **Settings** &rarr; **Bank Account (Finance)**.
3. Cliquez sur **Add Payment Method** :
   - **Payment Type :** *Electronic Funds Transfer (EFT / SEPA)*
   - **Currency :** *Euros (EUR)*
   - **Bank Country :** *France*
   - **Bank Account Number (IBAN) :** `FR76...`
   - **Bank Identifier Code (BIC) :** Votre BIC.
4. Activez l'option **Auto-Pay by Day of Month** (ex: le 1er ou le 15 de chaque mois).

---

## 4. Formulaire Fiscal Américain W-8BEN (Obligatoire pour 0% de retenue US)

Étant donné que PartnerStack et Impact Tech sont basés en Amérique du Nord :
1. Les plateformes vous demanderont de remplir un formulaire fiscal en ligne nommé **W-8BEN** (pour personne physique / auto-entrepreneur) ou **W-8BEN-E** (si vous êtes en société SASU/SARL).
2. Ce formulaire se remplit en 2 minutes directement sur leur interface :
   - **Part I - Identification :** Nom, Adresse en France, Pays de citoyenneté (France).
   - **Foreign Tax Identifying Number (FTIN) :** Renseignez votre numéro **SIREN (9 chiffres)** ou votre **Numéro Fiscal de Référence français**.
   - **Part II - Claim of Tax Treaty Benefits (Convention fiscale Franco-Américaine) :**
     - Cochez que vous êtes résident fiscal français bénéficiant du traité fiscal franco-américain (*Article 7 - Business Profits / Bénéfices des entreprises*).
     - **Taux de retenue à la source :** **0.0%**.
   - **Signature électronique :** Tapez votre nom et validez.
3. ✅ **Résultat immédiat :** Vous recevez **100% de vos gains bruts** sans aucune retenue à la source américaine de 30%.

---

## 5. Comptabilité & Déclaration Fiscale Micro-Entreprise BNC en France

L'activité d'apporteur d'affaires en ligne, d'affiliation d'infrastructure logicielle et de conseil FinOps relève des **BNC (Bénéfices Non Commerciaux)** au titre des activités libérales non réglementées (Code APE/NAF typique : `6202A` ou `6209Z`).

### A. Règle d'or : La comptabilité de caisse (Encaissements)
En micro-BNC, seules les sommes **effectivement créditées sur votre compte bancaire** au cours de l'année civile (du 1er janvier au 31 décembre) doivent être comptabilisées.
- Le taux de change à appliquer est le taux au jour de l'encaissement effectif sur votre relevé bancaire.
- Exécutez le script du projet pour tenir votre registre officiel :
  ```bash
  python compta_impots/livre_recettes.py
  ```

### B. Déclaration Périodique URSSAF (Mensuelle ou Trimestrielle)
- Rendez-vous sur `autoentrepreneur.urssaf.fr`.
- Ligne de déclaration : **Prestations de services et activités libérales BNC**.
- Taux de cotisations sociales : **21,1 %** (ou ~10,6 % si vous bénéficiez de l'ACRE la 1ère année).

### C. Déclaration Annuelle des Impôts sur le Revenu (Formulaire 2042-C-PRO)

Lors de votre déclaration de revenus au printemps :

| Votre Situation | Case à Déclarer | Montant à Inscrire | Traitement Fiscal DGFIP |
| :--- | :---: | :---: | :--- |
| **Régime Micro-BNC Classique** (Sans versement libératoire) | **`5HQ`** | **Total CA Brut Encaissé** | L'administration applique automatiquement un **abattement forfaitaire de 34 %** pour frais professionnels. L'impôt sur le revenu est calculé sur les 66 % restants selon votre tranche marginale (TMI). |
| **Option pour le Versement Libératoire de l'IR** (Payé à l'URSSAF) | **`5TE`** | **Total CA Brut Encaissé** | Vous avez déjà payé l'impôt forfaitaire de **2,2 %** à l'URSSAF lors de vos télédéclarations. Cette case sert uniquement à déterminer votre Revenu Fiscal de Référence (RFR) sans double imposition. |

### D. TVA et Territorialité (Ventes B2B Internationales)
- Les virements de PartnerStack (USA) et Impact.com (Irlande) sont des **prestations B2B fournies à des preneurs assujettis hors de France**.
- Selon l'article **259 B du CGI** et le principe de l'autoliquidation de la TVA (article **283-2 du CGI**), ces prestations sont situées hors du champ de la TVA française.
- Tant que votre chiffre d'affaires annuel reste sous le seuil de **36 800 €**, vous conservez la **Franchise en base de TVA (article 293 B du CGI)** : vous ne facturez pas de TVA et n'en reversez pas.

---

💡 **Tableau de bord interactif :** Double-cliquez sur `compta_impots/dashboard_bnc.html` pour visualiser en temps réel vos jauges de plafond, vos marges avant TVA et le montant exact à inscrire dans les cases `5HQ` et `5TE`.
