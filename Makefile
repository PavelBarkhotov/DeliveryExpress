# ===============================
# Project settings
# ===============================

PY_SRCS = app tests
APP = main:app


# ===============================
# Service targets
# ===============================

.PHONY: \
	help install run \
	lint lint-fix fmt fmt-check \
	type security test check fix \
	migration migrate downgrade \
	alembic-current


# ===============================
# Help
# ===============================

help:
	@echo "Доступные команды:"
	@echo ""
	@echo "  make install              Установить зависимости"
	@echo "  make run                  Запустить FastAPI"
	@echo ""
	@echo "  make lint                 Проверить код Ruff"
	@echo "  make lint-fix             Исправить ошибки Ruff"
	@echo "  make fmt                  Отформатировать код"
	@echo "  make fmt-check            Проверить форматирование"
	@echo "  make type                 Проверить типы mypy"
	@echo "  make security             Проверить код Bandit"
	@echo "  make test                 Запустить тесты"
	@echo ""
	@echo "  make check                Запустить все проверки"
	@echo "  make fix                  Ruff fix + форматирование"
	@echo ""
	@echo "  make migration msg=\"...\" Создать миграцию Alembic"
	@echo "  make migrate              Применить миграции"
	@echo "  make downgrade            Откатить одну миграцию"
	@echo "  make alembic-current      Показать текущую миграцию"


# ===============================
# Dependencies
# ===============================

install:
	uv sync


# ===============================
# Application
# ===============================

run:
	uv run uvicorn $(APP) --reload


# ===============================
# Ruff
# ===============================

lint:
	uv run ruff check $(PY_SRCS)

lint-fix:
	uv run ruff check $(PY_SRCS) --fix

fmt:
	uv run ruff format $(PY_SRCS)

fmt-check:
	uv run ruff format --check $(PY_SRCS)


# ===============================
# Mypy
# ===============================

type:
	uv run mypy $(PY_SRCS)


# ===============================
# Bandit
# ===============================

security:
	uv run bandit -r app -x tests,migrations


# ===============================
# Tests
# ===============================

test:
	uv run python -m pytest


# ===============================
# Alembic
# ===============================

migration:
	@test -n "$(msg)" || (echo 'Использование: make migration msg="описание миграции"' && exit 1)
	uv run alembic revision --autogenerate -m "$(msg)"

migrate:
	uv run alembic upgrade head

downgrade:
	uv run alembic downgrade -1

alembic-current:
	uv run alembic current


# ===============================
# Quality gates
# ===============================

check: lint fmt-check type test security

fix: lint-fix fmt