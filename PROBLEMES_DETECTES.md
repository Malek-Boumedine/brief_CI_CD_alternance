## fichier database.py :

- imports inutiles : 
  - import sys
  - from typing import Generator
- DATABASE_URL : pas d'identifiants en DUR, tout mettre dans le .env
- get_db() : pas de type de retour
- variable inutilisée : POOL_SIZE = 10; ne pas coder en dur -> mettre dans le .env

## main.py :

- imports inutiles : 
  - import os
  - import sys
  - import json
  - from typing import Dict, Any
- DEBUG_MODE, UNUSED_VAR : à mettre dans le .env
- UNUSED_VAR : supprimer si jamais utilisée
- dans lifespan() : connexion jamais fermée après le yield
- secret, API_KEY : ne pas mettre en dur, les mettre dans le .env et les charger
- very_long_variable_name_that_exceeds_line_length : nom de variable trop long

## fichier models/item.py : 

- import inutile : from typing import Optional
- _legacy_method non implémentée

## fichier routes/items.py :

- imports inutiles : 
  - from typing import List
  - import datetime
  - ItemCreate
- MAX_ITEMS_PER_PAGE : à mettre dans le .env
- get_items(), get_item(), create_item(), update_item(), delete_item() -> pas de type de retour
- _old_helper_function : doit être supprimée
- 

## fichier schema/item.py :

- import inutile : from typing import Optional
- class ItemCreate() : non implémentée

## fichier services/item_service.py :


### =============================================================================

## avec ruff : 

F401 [*] `sys` imported but unused
  --> app/database.py:9:8
   |
 7 | from sqlmodel import create_engine, Session
 8 | import os
 9 | import sys
   |        ^^^
10 | from typing import Generator
   |
help: Remove unused import: `sys`

F401 [*] `typing.Generator` imported but unused
  --> app/database.py:10:20
   |
 8 | import os
 9 | import sys
10 | from typing import Generator
   |                    ^^^^^^^^^
11 |
12 | DATABASE_URL = os.getenv(
   |
help: Remove unused import: `typing.Generator`

F401 [*] `os` imported but unused
 --> app/main.py:2:8
  |
1 | from contextlib import asynccontextmanager
2 | import os
  |        ^^
3 | import sys
4 | from fastapi import FastAPI
  |
help: Remove unused import: `os`

F401 [*] `sys` imported but unused
 --> app/main.py:3:8
  |
1 | from contextlib import asynccontextmanager
2 | import os
3 | import sys
  |        ^^^
4 | from fastapi import FastAPI
5 | from sqlmodel import SQLModel
  |
help: Remove unused import: `sys`

F401 [*] `json` imported but unused
 --> app/main.py:6:8
  |
4 | from fastapi import FastAPI
5 | from sqlmodel import SQLModel
6 | import json
  |        ^^^^
7 | from typing import Dict, Any
8 | from app.database import engine
  |
help: Remove unused import: `json`

F401 [*] `typing.Dict` imported but unused
 --> app/main.py:7:20
  |
5 | from sqlmodel import SQLModel
6 | import json
7 | from typing import Dict, Any
  |                    ^^^^
8 | from app.database import engine
9 | from app.routes import items_router
  |
help: Remove unused import

F401 [*] `typing.Any` imported but unused
 --> app/main.py:7:26
  |
5 | from sqlmodel import SQLModel
6 | import json
7 | from typing import Dict, Any
  |                          ^^^
8 | from app.database import engine
9 | from app.routes import items_router
  |
help: Remove unused import

F401 [*] `typing.Optional` imported but unused
 --> app/models/item.py:2:20
  |
1 | from sqlmodel import Field, SQLModel
2 | from typing import Optional
  |                    ^^^^^^^^
3 |
4 | class Item(SQLModel, table=True):
  |
help: Remove unused import: `typing.Optional`

F401 [*] `typing.List` imported but unused
 --> app/routes/items.py:3:20
  |
1 | from fastapi import APIRouter, Depends, HTTPException, status
2 | from sqlmodel import Session
3 | from typing import List
  |                    ^^^^
4 | import datetime
  |
help: Remove unused import: `typing.List`

F401 [*] `datetime` imported but unused
 --> app/routes/items.py:4:8
  |
2 | from sqlmodel import Session
3 | from typing import List
4 | import datetime
  |        ^^^^^^^^
5 |
6 | from app.database import get_db
  |
help: Remove unused import: `datetime`

F401 [*] `app.schemas.item.ItemCreate` imported but unused
 --> app/routes/items.py:7:30
  |
6 | from app.database import get_db
7 | from app.schemas.item import ItemCreate, ItemResponse, ItemUpdate
  |                              ^^^^^^^^^^
8 | from app.services.item_service import ItemService
  |
help: Remove unused import: `app.schemas.item.ItemCreate`

F401 [*] `typing.Optional` imported but unused
 --> app/schemas/item.py:2:20
  |
1 | from sqlmodel import Field, SQLModel
2 | from typing import Optional
  |                    ^^^^^^^^
3 |
4 | class ItemBase(SQLModel):
  |
help: Remove unused import: `typing.Optional`

Found 12 errors.
[*] 12 fixable with the `--fix` option.

fix avec --fix de ruff :
uv run ruff check --fix

### =============================================================================

## avec mypy : 

uv run mypy app/
app/database.py:19: error: Function is missing a return type annotation  [no-untyped-def]
app/models/item.py:10: error: Function is missing a return type annotation  [no-untyped-def]
app/models/item.py:10: note: Use "-> None" if function does not return a value
app/routes/items.py:13: error: Function is missing a return type annotation  [no-untyped-def]
app/routes/items.py:19: error: Function is missing a return type annotation  [no-untyped-def]
app/routes/items.py:19: error: Function is missing a type annotation for one or more arguments  [no-untyped-def]
app/routes/items.py:30: error: Function is missing a type annotation  [no-untyped-def]
app/routes/items.py:35: error: Function is missing a return type annotation  [no-untyped-def]
app/routes/items.py:46: error: Function is missing a return type annotation  [no-untyped-def]
app/routes/items.py:54: error: Function is missing a type annotation  [no-untyped-def]
app/main.py:12: error: Function is missing a return type annotation  [no-untyped-def]
app/main.py:28: error: Function is missing a return type annotation  [no-untyped-def]
app/main.py:33: error: Function is missing a return type annotation  [no-untyped-def]
Found 12 errors in 4 files (checked 11 source files)

fix : manuellement








