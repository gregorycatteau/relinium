# RFC - Filiere Relinium Anti-Scam v0.1

Statut: draft controle

## 1. Objectif

Relinium Anti-Scam (`scam_trace`) transforme un incident d'arnaque numerique en dossier probatoire structure. La filiere preserve la preuve originale, calcule les empreintes, guide l'operateur, construit une timeline, extrait des indicateurs techniques, cherche des correlations simples et prepare des rapports relisibles.

La filiere est defensive uniquement. Elle ne visite pas les liens suspects, ne contourne aucun systeme, ne contacte pas agressivement d'infrastructure suspecte et ne soumet aucun rapport sans validation humaine.

## 2. Perimetre multi-vecteurs

Le phishing email est un vecteur parmi d'autres. La filiere couvre au minimum:

- email;
- SMS;
- appel telephonique;
- messagerie;
- document collaborateur;
- cle USB suspecte;
- faux site;
- transaction bancaire;
- acces distant;
- poste victime;
- recit de la victime.

## 3. Chaine de conservation

Chaque artefact doit etre traite comme une piece a preserver:

- original conserve hors base operationnelle lorsque le fichier est lourd ou sensible;
- hash SHA-256 de l'artefact ou du texte colle dans le MVP;
- horodatage d'ingestion;
- operateur ou acteur logique;
- source de la preuve;
- statut d'integrite;
- extraction controlee des indicateurs sans interaction externe.

PostgreSQL garde les metadonnees, hashes, evenements de custody, timelines et rapports. Les fichiers binaires lourds ne sont pas stockes en base dans le MVP.

## 4. Questionnaire guide

Le questionnaire minimal documente les faits utiles a la decision:

- clic sur lien;
- saisie de mot de passe;
- carte bancaire communiquee;
- virement ou paiement;
- logiciel installe;
- documents envoyes;
- appel telephonique;
- acces distant;
- montant perdu;
- banque contactee;
- plainte ou signalement deja effectue.

Chaque question indique pourquoi l'information est utile et quelle action defensive lancer.

## 5. Analyse technique parallele

L'analyse MVP accepte un texte brut, notamment EML colle. Elle extrait passivement:

- headers `From`, `Reply-To`, `Return-Path`, `Subject`, `Received`;
- URLs simples;
- domaines issus des URLs;
- emails, telephones, IBAN, IP et hashes visibles;
- mots-cles d'urgence, paiement, compte, carte vitale, amende ou colis;
- mismatch basique entre domaine apparent et domaine cible.

Aucune URL n'est cliquee et aucun contenu distant n'est telecharge.

## 6. Timeline probatoire

La timeline combine:

- reception ou collecte de preuve;
- declarations victime;
- evenements deduits du questionnaire;
- analyse technique;
- actions de remediation;
- preparation de rapport.

Chaque evenement porte une source et un niveau de confiance.

## 7. Correlations multi-cas

Le MVP correle les dossiers par indicateurs partages:

- domaine;
- motif URL;
- telephone;
- IBAN;
- IP;
- hash;
- motif texte simple.

Ces correlations sont indicatives. Elles doivent etre relues avant usage externe.

## 8. Scoring

Le scoring combine:

- risque technique;
- impact financier ou identitaire;
- confiance d'attribution;
- urgence operationnelle.

Le MVP calcule une severite `low`, `medium`, `high` ou `critical` a partir des reponses critiques, montants et indicateurs a risque eleve.

## 9. Rapports generes

La filiere prepare des rapports Markdown:

- rapport victime;
- rapport autorites;
- rapport banque;
- rapport entreprise;
- rapport technique.

Chaque rapport distingue:

- faits prouves;
- declarations victime;
- elements techniques;
- hypotheses et correlations;
- actions recommandees.

## 10. Canaux francais a prevoir

Les rapports peuvent aider une transmission manuelle vers:

- Signal Spam;
- 33700 pour SMS;
- Phishing Initiative;
- 17Cyber;
- THESEE ou PHAROS selon cas;
- police ou gendarmerie;
- banque.

Relinium ne soumet rien automatiquement dans le MVP.

## 11. Limites legales et RGPD

- validation humaine obligatoire avant transmission;
- minimisation RGPD des champs et libelles;
- pas de stockage de secrets en clair;
- pas de copie de `personal_vault`, `vault_index` ou `users/user_template`;
- pas d'envoi automatique aux autorites, banques ou plateformes;
- pas d'interaction offensive avec l'infrastructure suspecte.

## 12. MVP implemente dans ce tour

- app Django `scam_trace`;
- modeles PostgreSQL pour dossiers, artefacts, questionnaire, indicateurs, timeline, custody, rapports et correlations;
- services backend pour ingestion texte, hash, extraction passive, timeline, rapports Markdown et correlations simples;
- queries et mutations GraphQL camelCase;
- page Nuxt `/anti-scam` en francais;
- outil Go defensif `relinium-evidence-hash` pour hash local et NDJSON de custody;
- documentation applicative.

## 13. Evolutions futures

- connecteurs mailbox;
- Microsoft Graph;
- Google Workspace;
- SIEM, proxy et DNS;
- correlations avancees;
- export PDF;
- horodatage externe;
- gestion d'upload binaire controlee;
- workflow de revue multi-operateurs.
