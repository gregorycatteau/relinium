# Makefile global Relinium Experimental Lab

.PHONY: help dev test bench stop

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
