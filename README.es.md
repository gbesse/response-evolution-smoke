# Response Evolution Smoke

[English](README.md) · [Français](README.fr.md) · Español

**¿Puede el cliente generado ayer leer todavía la respuesta de mañana?** Esta comprobación CI entrega a un decodificador antiguo una respuesta JSON válida y la misma respuesta con un campo añadido. Marca `regression` solo cuando la respuesta inicial funciona y la nueva falla.

## Proyectos relacionados

- [Hindsight #5454](https://github.com/vectorize-io/hindsight/issues/5454) informa de que un cliente Go generado antiguo rechaza el nuevo campo `total` por `DisallowUnknownFields()`.
- [oasdiff](https://github.com/oasdiff/oasdiff) compara esquemas API; esta herramienta ejecuta el decodificador antiguo con ejemplos de respuesta. No afirma integración ni afiliación.

## Demostración de diez segundos

```sh
python3 smoke.py demo --lang es
python3 smoke.py check --fixture examples/list-response.json --field total --value 1 --decoder-cmd 'go run examples/old_go_client.go' --lang es
```

Los decodificadores Python y Go incluidos rechazan a propósito los campos desconocidos. Para su cliente, indique un comando local de confianza que lea una respuesta JSON de la entrada estándar y termine con código 0 si puede decodificarla. El comando se ejecuta sin shell. Códigos de `check`: 0 compatible, 2 regresión o evidencia incompleta, 1 entrada no válida. Solo se añade un campo en la raíz JSON; la herramienta no lee OpenAPI ni garantiza todos los cambios futuros.

Python 3.11+, biblioteca estándar. Pruebas: `python3 -m unittest discover -s tests -q`. Licencia MIT.
