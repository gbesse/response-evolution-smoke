# Response Evolution Smoke

[English](README.md) · Français · [Español](README.es.md)

**Le client généré d’hier peut-il encore lire la réponse de demain ?** Ce contrôle CI soumet à un ancien décodeur une réponse JSON valide, puis la même avec un champ ajouté. Il signale une `regression` seulement si la réponse initiale passe et la nouvelle échoue.

## Projets voisins

- [Hindsight #5454](https://github.com/vectorize-io/hindsight/issues/5454) rapporte qu’un ancien client Go généré refuse le nouveau champ `total` à cause de `DisallowUnknownFields()`.
- [oasdiff](https://github.com/oasdiff/oasdiff) compare les schémas API ; cet outil exécute plutôt votre ancien décodeur sur des exemples de réponse. Aucune intégration ni affiliation n’est revendiquée.

## Démo de dix secondes

```sh
python3 smoke.py demo --lang fr
python3 smoke.py check --fixture examples/list-response.json --field total --value 1 --decoder-cmd 'go run examples/old_go_client.go' --lang fr
```

Les décodeurs Python et Go fournis rejettent volontairement les champs inconnus. Pour votre client, transmettez une commande locale de confiance qui lit une réponse JSON sur l’entrée standard et sort avec le code 0 si le décodage réussit. La commande s’exécute sans shell. Codes de `check` : 0 compatible, 2 régression ou preuve incomplète, 1 entrée invalide. L’ajout se fait uniquement à la racine JSON ; l’outil ne lit pas OpenAPI et ne garantit pas toutes les évolutions futures.

Python 3.11+, bibliothèque standard. Tests : `python3 -m unittest discover -s tests -q`. Licence MIT.
