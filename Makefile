# Makefile global Relinium Experimental Lab

.PHONY: help dev test bench stop docs-check new-doc

help:
	@echo "Cibles disponibles :"
	@echo "  make dev   POC=<path>   - lancer le POC (ex: POC=pocs/framework/fastapi)"
	@echo "  make test  POC=<path>   - lancer les tests du POC"
	@echo "  make bench POC=<path>   - lancer le bench léger sur le POC"
	@echo "  make stop  POC=<path>   - arrêter/clean le POC (si supporté)"

dev:
	@[ -n "$(POC)" ] || (echo "POC non défini. Utiliser POC=pocs/..." && exit 1)
	@echo "-> Démarrage POC $(POC)"
	@if [ -f "$(POC)/Makefile" ]; then \
	  $(MAKE) -C "$(POC)" dev; \
	else \
	  echo "⚠️ Aucun Makefile dans $(POC). À créer pour ce POC."; \
	fi

test:
	@[ -n "$(POC)" ] || (echo "POC non défini. Utiliser POC=pocs/..." && exit 1)
	@echo "-> Tests POC $(POC)"
	@if [ -f "$(POC)/Makefile" ]; then \
	  $(MAKE) -C "$(POC)" test; \
	else \
	  echo "⚠️ Aucun Makefile dans $(POC). À créer pour ce POC."; \
	fi

bench:
	@[ -n "$(POC)" ] || (echo "POC non défini. Utiliser POC=pocs/..." && exit 1)
	@echo "-> Bench POC $(POC)"
	@if [ -f "$(POC)/Makefile" ]; then \
	  $(MAKE) -C "$(POC)" bench; \
	else \
	  echo "⚠️ Aucun Makefile dans $(POC). À créer pour ce POC."; \
	fi

stop:
	@[ -n "$(POC)" ] || (echo "POC non défini. Utiliser POC=pocs/..." && exit 1)
	@echo "-> Stop POC $(POC)"
	@if [ -f "$(POC)/Makefile" ]; then \
	  $(MAKE) -C "$(POC)" stop; \
	else \
	  echo "⚠️ Aucun Makefile dans $(POC). À créer pour ce POC."; \
	fi

docs-check:
	@echo "-> Validation documentation (hash + registre)"
	@python scripts/ssot_hash_check.py --ci
	@python scripts/ssot_registry_check.py --ci

new-doc:
	@[ -n "$(ID)" ] || (echo "ID est requis (ex: ID=SPRINT-0002)" && exit 1)
	@[ -n "$(TYPE)" ] || (echo "TYPE est requis (ex: TYPE=SPRINT)" && exit 1)
	@[ -n "$(STATUS)" ] || (echo "STATUS est requis (ex: STATUS=\"En cours\")" && exit 1)
	@[ -n "$(DOC_PATH)" ] || (echo "DOC_PATH est requis (ex: DOC_PATH=docs/sprints/phase1/SPRINT-0002.md)" && exit 1)
	@[ -n "$(VERSION)" ] || (echo "VERSION est requis (ex: VERSION=1.0.0)" && exit 1)
	@[ -n "$(TAGS)" ] || (echo "TAGS est requis (ex: TAGS=\"sprint,inventaire,stack\")" && exit 1)
	@[ -n "$(LINKS)" ] || (echo "LINKS est requis (ex: LINKS=\"OBS-0001,RFC-0002\")" && exit 1)
	@[ -n "$(AUTHOR)" ] || (echo "AUTHOR est requis (ex: AUTHOR=\"Agent Codex\")" && exit 1)
	@python scripts/new_doc_routine.py \
	  --path "$(DOC_PATH)" \
	  --id "$(ID)" \
	  --type "$(TYPE)" \
	  --status "$(STATUS)" \
	  --version "$(VERSION)" \
	  --author "$(AUTHOR)" \
	  --tags "$(TAGS)" \
	  --links "$(LINKS)" \
	  $(if $(DATE),--date "$(DATE)",) \
	  $(if $(ID_ROOT),--id-root "$(ID_ROOT)",) \
	  $(if $(TITLE),--title "$(TITLE)",) \
	  $(if $(LINEAGE_TITLE),--lineage-title "$(LINEAGE_TITLE)",) \
	  $(if $(SCOPE),--scope "$(SCOPE)",) \
	  $(if $(PATTERN),--pattern "$(PATTERN)",) \
	  $(if $(BODY_TEMPLATE),--body-template "$(BODY_TEMPLATE)",) \
	  $(if $(OVERWRITE_BODY),--overwrite-body,) \
	  $(if $(REGISTRY_PATH),--registry "$(REGISTRY_PATH)",) \
	  $(if $(PREVIOUS_HASH),--previous-hash "$(PREVIOUS_HASH)",) \
	  $(if $(LINKS_KEY),--links-key "$(LINKS_KEY)",) \
	  $(if $(LINKS_DELIMITER),--links-delimiter "$(LINKS_DELIMITER)",) \
	  $(if $(COMMIT_MESSAGE),--commit-message "$(COMMIT_MESSAGE)",) \
	  $(if $(SKIP_VALIDATIONS),--skip-validations,) \
	  $(if $(SKIP_COMMIT),--skip-commit,)
