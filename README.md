# ttl-dict

![Build Status](https://github.com/nitsugahcram/ttl-dict/actions/workflows/ci.yml/badge.svg)
![Coverage](https://img.shields.io/codecov/c/github/nitsugahcram/ttl-dict)
![PyPI version](https://img.shields.io/pypi/v/ttl-dict)
![License](https://img.shields.io/pypi/l/ttl-dict)

## Descripción

`ttl-dict` es una implementación de diccionario en Python con soporte de Time-To-Live (TTL) para cada clave. Cada elemento expirará y será eliminado automáticamente tras el tiempo configurado.

### Motivación

En escenarios donde necesitamos almacenar valores temporales en memoria (por ejemplo, cachés de datos con expiración), un diccionario estándar no ofrece mecanismos incorporados de TTL. `ttl-dict` resuelve este problema de forma sencilla.

## Características

- Asignación de TTL individual por clave.
- Eliminación automática de entradas expiradas.
- API compatible con `dict` donde resulta posible.

## Instalación

```bash
pip install ttl-dict
```

## Uso Básico

```python
from ttl_dict import TTLDict

d = TTLDict(default_ttl=60)  # TTL por defecto: 60 segundos

d['foo'] = 'bar'
print(d['foo'])  # 'bar'

# Después de 60 segundos:
# print(d['foo'])  # KeyError porque ha expirado
```

## Ejemplos Avanzados

```python
# TTL por entrada individual
d['baz'] = ('qux', 30)  # TTL de 30 segundos

# Iteración y métodos completos
d.update({'a': 1, 'b': 2})
keys = list(d.keys())

# Uso de context manager para suspender limpieza automática
with d.pause_cleanup():
    # realiza varias operaciones sin limpieza intermedia
    pass
```

## API

| Método                  | Descripción                                      |
|-------------------------|--------------------------------------------------|
| `TTLDict(default_ttl)`  | Crea un diccionario con TTL por defecto.         |
| `__setitem__`           | Asigna clave, valor y TTL opcional.              |
| `__getitem__`           | Obtiene valor si no ha expirado.                 |
| `cleanup()`             | Forzar limpieza de elementos expirados.          |
| `pause_cleanup()`       | Context manager para pausar limpieza automática. |

## Contribuciones

Lee [CONTRIBUTING.md](CONTRIBUTING.md) para pautas sobre cómo contribuir.

## Licencia

Este proyecto está licenciado bajo la Licencia MIT. Ver `LICENSE` para más detalles.
