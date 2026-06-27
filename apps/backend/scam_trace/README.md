# Relinium Anti-Scam (`scam_trace`)

App Django de filiere anti-scam defensive.

## Perimetre MVP

- dossiers victime/cas;
- metadonnees d'artefacts et SHA-256;
- questionnaire operateur;
- extraction passive d'indicateurs depuis texte/EML colle;
- timeline probatoire;
- evenements de custody;
- rapports Markdown;
- correlations simples entre dossiers.

## Limites de securite

- aucun clic sur lien suspect;
- aucun telechargement de contenu distant;
- aucun stockage binaire lourd en base;
- aucun secret en clair;
- aucune soumission automatique aux autorites, banques ou plateformes;
- validation humaine obligatoire avant transmission.

## GraphQL

Queries:

- `scamCases`
- `scamCase(id)`
- `scamCaseTimeline(caseId)`
- `scamCaseIndicators(caseId)`
- `scamCaseReports(caseId)`
- `scamCaseCorrelations(caseId)`
- `scamQuestionnaireTemplate`

Mutations:

- `createScamCase`
- `addScamArtifact`
- `answerScamQuestion`
- `generateScamReports`
- `markReportReviewed`

Le texte brut MVP est limite cote service a 200 Ko.
