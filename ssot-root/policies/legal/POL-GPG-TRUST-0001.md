# POL-GPG-TRUST-0001 — Politique de confiance cryptographique Relinium

## 1. Objet

Cette politique définit la manière dont les utilisateurs peuvent vérifier
l’authenticité et l’intégrité :

- du dépôt Relinium SSOT,
- des tags de version “officiels”,
- et, plus largement, des artefacts signés associés au projet.

Relinium ne garantit pas que les usages faits du code soient éthiques.
Il garantit que ce qui prétend être Relinium officiel peut être vérifié
cryptographiquement.

## 2. Portée

Cette politique s’applique :

- au dépôt Git public utilisé comme référence de code,
- aux tags de version canoniques (ex. v0.1-ssot-genesis),
- aux archives publiées et signées par PixelProwlers.

Elle ne couvre pas :

- les forks tiers non signés,
- les modifications locales non signées,
- les déploiements opérés par des organisations externes.

## 3. Identité cryptographique officielle

L’identité cryptographique de référence du projet Relinium SSOT est :

- Nom : Pixelprowlers (Relinium SSOT)
- Adresse : contact@pixelprowlers.io
- Type de clé : ed25519 (signatures) + sous-clé cv25519 (chiffrement)
- KeyID long : B6AB0FC82888D157
- Empreinte (fingerprint) :
  A5A1 6737 3F3A 800B 4861 034B B6AB 0FC8 2888 D157

Toute signature GPG revendiquée comme "officielle Relinium" doit être
émise par cette clé (ou une clé déclarée comme successeure dans une
future politique de rotation).

## 4. Engagements du mainteneur

Le mainteneur s’engage à :

1. Signer les commits canoniques.
2. Signer les tags de version canoniques.
3. Ne jamais réécrire l’historique signé (pas de push --force sur main).
4. Documenter toute rotation de clé dans une nouvelle politique de type
   POL-GPG-TRUST-0002.

## 5. Vérification par les utilisateurs

### 5.1. Vérifier la signature d’un commit

Commande type :

git log --show-signature -1

L’utilisateur doit vérifier que la signature est "good" et que l’empreinte
de la clé correspond à l’identité décrite plus haut.

### 5.2. Vérifier un tag de version

Commande type :

git tag -v v0.1-ssot-genesis

Le tag est considéré comme valide si :

- la signature est "good",
- la clé correspond à Pixelprowlers (Relinium SSOT) <contact@pixelprowlers.io>.

### 5.3. Vérifier un artefact externe

Si une archive (tar/zip) est publiée avec :

- un fichier .asc (signature GPG), ou
- un fichier .sha256 signé,

l’utilisateur doit vérifier :

1. la signature GPG du fichier .asc,
2. la cohérence du hash avec l’archive téléchargée.

## 6. Politique de clés et rotation

1. Durée de vie : les clés Relinium sont émises avec une date d’expiration
   limitée. La validité doit être vérifiée avant toute confiance.
2. Rotation planifiée : une nouvelle clé est générée, signée par l’ancienne
   et documentée dans une nouvelle politique.
3. Compromission : la clé est révoquée, un avis formel est publié dans
   ssot_canon, et une nouvelle politique POL-GPG-TRUST-XXXX définit la suite.

## 7. Forks, dérivés et responsabilités

1. Forks non signés : tout dépôt qui ne respecte pas cette politique ne peut
   pas être présenté comme version officielle Relinium SSOT.
2. Dérivés signés par d’autres clés : ils peuvent exister mais ne peuvent pas
   revendiquer l’identité Pixelprowlers (Relinium SSOT).
3. Responsabilité d’usage : Relinium fournit des mécanismes pour tracer les
   faits et la provenance des décisions. La responsabilité des usages
   incombe aux organisations qui déploient le système.

## 8. Évolution de la politique

Cette politique est versionnée comme tout document SSOT :

- tout changement substantiel donne lieu à une nouvelle version numérotée,
- chaque version est signée, horodatée et enregistrée dans le registre
  et dans le Event Kernel.

