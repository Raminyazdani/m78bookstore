# فروشگاه فایل مکتب ۷۸ (Maktab 78 File Store)

**دومین میکرو پروژه پایتون خام (پایانی پایتون - قبل از Flask)**

A small, educational, *framework-less* Python project that demonstrates:

- A simple **CLI router/menu system** (nested menus + callbacks)
- A lightweight **PostgreSQL persistence layer** (very small ORM-like base + query builders)
- A few **domain models** for a “file store” concept:
  - users
  - files
  - comments
  - order carts
  - order items

> This repo is intentionally minimal and instructional. It’s not production-ready (see **Known limitations**).

---

## Table of contents

- [Overview](#overview)
- [Project structure](#project-structure)
- [How it works](#how-it-works)
  - [CLI routing](#cli-routing)
  - [Database layer](#database-layer)
  - [Validation layer](#validation-layer)
- [Domain modules](#domain-modules)
  - [`users`](#users)
  - [`file`](#file)
  - [`comment`](#comment)
  - [`order_cart`](#order_cart)
  - [`order_item`](#order_item)
  - [`public`](#public)
- [Setup](#setup)
  - [Prerequisites](#prerequisites)
  - [Configure Postgres connection](#configure-postgres-connection)
  - [Install dependencies](#install-dependencies)
- [Usage](#usage)
  - [Run the CLI menu](#run-the-cli-menu)
  - [Run the DB demo script](#run-the-db-demo-script)
- [Testing](#testing)
- [Known limitations / technical notes](#known-limitations--technical-notes)
- [Roadmap ideas](#roadmap-ideas)
- [License](#license)

---

## Overview

This codebase is a learning project built with “raw Python” (no Flask/Django). It includes:

1. **A router/menu framework** (`core/router.py`) that lets you build a tree of menus (`Route`) and bind menu items to callable functions (`CallBack`).
2. **A minimal database manager** (`core/managers.py`) that:
   - connects to PostgreSQL using `psycopg2`
   - can create tables from models
   - can insert/read/update/delete rows
3. **Domain models** that represent the core entities of a file store.

---

## Project structure

Top-level:

- `main.py` — example script that creates a `DBManager`, inserts sample records, and prints reads.
- `routes.py` — defines the CLI router tree and links menu items to callback functions.
- `configs.py` — database connection settings and app info used by `public/utils.py`.
- `requirements.txt` — currently empty (dependencies are used but not declared).

Packages:

- `core/` — router framework + DB base model + query builders + validation utilities.
- `users/` — `User` model (with validation descriptors) + (out-of-sync) tests scaffold.
- `file/` — `Files` model.
- `comment/` — `Comment` model.
- `order_cart/` — `Order_cart` model.
- `order_item/` — `Order_item` model.
- `public/` — simple user-facing callbacks (e.g., About Us, Hello).

---

## How it works

### CLI routing

**Files:** `core/router.py`, `routes.py`, `public/utils.py`

The CLI menu is composed of:

- `Router(name, route)`
  - Entry point for the CLI application.
  - `generate()` clears the terminal and starts the root route.

- `Route(name, description=None, callback: CallBack=None, children=())`
  - Represents an item in a menu.
  - If `callback` is **not provided**, the route is treated as a **menu** and `children` are displayed.
  - If `callback` **is provided**, it’s treated as an **action** route.

- `CallBack(package, function, *args, **kwargs)`
  - Dynamically imports a module (`import_module(package)`) and resolves a function by name.
  - When the route runs, `CallBack.call()` runs the function with provided args/kwargs.

Routing tree is defined in `routes.py`. Example items already present:

- “About us” → `public.utils.about_us`
- “say hello” → `public.utils.salam(name="amirhosein")`

Navigation behavior:

- A parent stack is managed through `core.router.Config.parent`.
- After running a leaf callback, the UI waits for `Press enter to back menu` and returns.

### Database layer

**Files:** `core/managers.py`, `core/models.py`, `core/query.py`, `configs.py`

The persistence layer is made of:

- `DBModel` (`core/models.py`)
  - Abstract-ish base class that defines hooks to build SQL:
    - create table
    - check table exists
    - insert
    - read
    - update
    - delete

- Query builder functions (`core/query.py`)
  - `manager_db_create_table(instance|class)` builds a `CREATE TABLE ...` statement.
  - `manager_db_insert_to_table(instance)` builds an `INSERT INTO ...` statement.
  - `manager_db_read_from_table(class, pk=None)` builds `SELECT ...`.
  - `manager_db_update_to_table(instance)` / `manager_db_delete_from_table(instance)`.

- `DBManager` (`core/managers.py`)
  - Wraps a `psycopg2` connection.
  - Uses `RealDictCursor` so fetched rows are dict-like.
  - Key methods:
    - `insert_table(model_instance)`
    - `read(model_class, pk=None)`
    - `update(model_instance)`
    - `delete(model_instance)`
    - plus table helpers (`check_table_exists*`, `create_table*`, `delete_table`)

Table creation strategy:

- On insert/read/update/delete, code checks whether the table exists.
- If not, it prints a message and attempts to create the table using the model definition.

Database configuration:

- `configs.py` defines `DB_CONNECTION = {HOST, USER, PORT, PASSWORD}`.
- The database name is passed at runtime to `DBManager(database="...")`.

### Validation layer

**File:** `core/utils.py`

Validation is implemented using *descriptor classes* (e.g., `First_name`, `Email`, `Password`, etc.).

- Each descriptor validates values via regex helpers like `email_validator`, `password_validator`, etc.
- If invalid, it raises a specialized `ValidationError`.

Common validators included:

- names/usernames: must start with a letter (`^[a-zA-Z]{1}.*$`)
- email, phone, national id, age
- password: at least 8 chars, includes lowercase, uppercase, digit, and special character
- file id: numeric
- cart items: stored as a comma-separated string that becomes a list

The module also includes mappings used for table generation:

- `table_column_types`: maps attribute names → SQL column types
- `unique_table_column_types`: list of column names to be marked as `UNIQUE`

---

## Domain modules

### `users`

**Files:** `users/models.py`, `users/tests.py`, `users/utils.py`

Model: `User(DBModel)`

- Table: `users`
- Primary key: `id` (serial)
- Fields:
  - `first_name`, `last_name`, `username`, `email`, `phone`, `national_id`, `age`, `password`
  - `time_created`, `time_modified` (timestamps stored as strings)

Validation:

- `first_name`, `last_name`, `username` use the name validator.
- `email`, `phone`, `national_id`, `age`, `password` have dedicated validators.

Notes:

- `users/tests.py` exists but targets an older API (`DBManager.create`) and an older `User(...)` signature. See [Testing](#testing) and [Known limitations](#known-limitations--technical-notes).

### `file`

**Files:** `file/models.py`, `file/tests.py`, `file/utils.py`

Model: `Files(DBModel)`

- Table: `files`
- Fields:
  - `name` (validated)
  - `owner` (validated like username)
  - `path` (currently validated like name, which is restrictive)
  - `info`
  - `time_created`, `time_modified`

### `comment`

**Files:** `comment/models.py`, `comment/tests.py`, `comment/utils.py`

Model: `Comment(DBModel)`

- Table: `comments`
- Fields:
  - `file_id` (numeric string)
  - `owner` (validated like username)
  - `info`
  - `time_created`

### `order_cart`

**Files:** `order_cart/models.py`, `order_cart/tests.py`, `order_cart/utils.py`

Model: `Order_cart(DBModel)`

- Table: `order_cart`
- Fields:
  - `owner_id_cart` (username-ish; also listed as unique in `core/utils.py`)
  - `items`
  - `time_created`

`items` behavior:

- Accepts `None`, empty string, a comma-separated string, or a list.
- Intended to represent file IDs.

### `order_item`

**Files:** `order_item/models.py`, `order_item/tests.py`, `order_item/utils.py`

Model: `Order_item(DBModel)`

- Table: `order_item`
- Fields:
  - `file_id`
  - `order_cart_id`
  - `time_created`

### `public`

**Files:** `public/utils.py`

This module contains basic functions meant to be used as router callbacks.

- `about_us()` prints info from `configs.INFO`.
- `salam(name)` prints a greeting.

---

## Setup

### Prerequisites

- Python 3.x
- PostgreSQL (reachable using the connection parameters in `configs.py`)
- A database created (example names used in code: `test`, `file_store`)

### Configure Postgres connection

Edit `configs.py` and set:

- `DB_CONNECTION["HOST"]`
- `DB_CONNECTION["USER"]`
- `DB_CONNECTION["PORT"]`
- `DB_CONNECTION["PASSWORD"]`

> Tip: avoid committing real passwords. Consider using environment variables in a future iteration.

### Install dependencies

`requirements.txt` is currently empty, but the code imports `psycopg2`.

To run the database code you’ll need to install:

- `psycopg2` (or `psycopg2-binary` for local development)

Example (PowerShell):

```powershell
python -m pip install psycopg2-binary
```

---

## Usage

### Run the CLI menu

The router is defined in `routes.py`. To run the interactive menu, `main.py` should call:

- `router.generate()`

In the current code, this line exists but is commented out.

Example (PowerShell):

```powershell
python main.py
```

> If you want the menu to start, uncomment `router.generate()` in `main.py` (not done in this README update).

### Run the DB demo script

`main.py` currently acts as a small demo:

- creates `DBManager("test")`
- creates instances of `User`, `Files`, `Comment`, `Order_cart`, `Order_item`
- inserts them
- reads back and prints results

Make sure the database name you pass to `DBManager(...)` exists in Postgres.

---

## Testing

Tests are placed inside each domain package as `tests.py`.

Current state:

- `users/tests.py` contains a `unittest.TestCase` class.
- Other `*/tests.py` files are present but empty.

Important:

- `users/tests.py` appears **out-of-sync** with the current implementation:
  - It calls `DBManager.create(...)`, but `DBManager` currently exposes `insert_table(...)` instead.
  - It builds `User(...)` with a different parameter list than `users/models.py` currently requires.

Because of that mismatch, the existing test suite is not expected to run successfully without updates.

---

## Known limitations / technical notes

This section documents behaviors that are important for understanding the current code.

- **No dependency pinning:** `requirements.txt` is empty.
- **SQL building is string-based:** `core/query.py` uses f-strings to embed values directly into SQL.
  - This is typical for learning exercises but is vulnerable to SQL injection in real apps.
- **`INSERT` builds from `vars(instance)` ordering:** `manager_db_insert_to_table()` uses `list(vars(instance).keys())[:-1]`.
  - This assumes `id` is the last attribute; models set `id` last to support this.
- **`read(pk=...)` uses the hard-coded column name `id`:** the `PK` attribute on models isn’t used in query building.
- **`create_table_model` introspection is brittle:** it uses `list(vars(class_name).keys())[3:-4]` to decide columns.
- **`FilePath` validation is overly restrictive:** it uses the same validator as names.
- **Errors/rollbacks are broad:** DB operations catch all exceptions without preserving the error.

---

## Roadmap ideas

If you want to evolve this project further (still keeping it simple), here are safe next steps:

- Fill `requirements.txt` (pin `psycopg2-binary` at least).
- Add a `.env`-based configuration (never hard-code passwords).
- Replace string-formatted SQL with parameterized queries.
- Improve router UX (input validation, back/exit actions).
- Update and expand tests to match the current DBManager API.

---

## License

See `LICENSE`.
