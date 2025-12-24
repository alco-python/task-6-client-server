# task-6-client-server

Сервер для управления и вычисления параметризованных функций вида `y = f(x, λ)`.  
Поддерживает:

- **REST API** (на FastAPI) — для интеграции;
- **Командную строку (CLI)** — для локального использования.

Функции сохраняются в директории проекта в папке `storage` в формате `json`.

## Установка и запуск

### 1. Клонируйте репозиторий
```bash
git clone <https://github.com/alco-python/task-6-client-server.git>
cd <task-6-client-server>
```
### 2. Создайте вирутальное окружение
```bash
python3 -m venv .venv
```
### 3. Активируйте окружение
#### Windows (PowerShell)
```bash
.\.venv\Scripts\Activate.ps1
```
#### Linux / macOS
```bash
source .venv/bin/activate
```
### 4. Установите зависимости:
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 5. Запустите API-сервер:
```bash
uvicorn api:app --reload
```
---

## Использование
### Пример работы с CLI

При запуске CLI автоматически загружаются 4 функции:

| Функция       | Формула                      | Параметры по умолчанию                     |
|---------------|------------------------------|--------------------------------------------|
| `linear`      | `y = a * x + b`              | `{"a": 1.0, "b": 0.0}`                     |
| `quadratic`   | `y = a * x² + b * x + c`     | `{"a": 1.0, "b": 0.0, "c": 0.0}`           |
| `sinusoidal`  | `y = a * sin(w * x + p) + c` | `{"a": 1.0, "w": 1.0, "p": 0.0, "c": 0.0}` |
| `exponential` | `y = a * exp(k * x) + c`     | `{"a": 1.0, "k": 0.1, "c": 0.0}`           |

#### Основные команды

```bash
# Список функций
python cli.py list

# Информация о функции
python cli.py info linear

# Вычислить
python cli.py call linear 5
python cli.py call quadratic "2.5"

# Обновить параметры
python cli.py create linear --params '{"a": 2.0, "b": 3.0}'

# Удалить функцию
python cli.py delete exponential
```

### Пример работы с API


#### Unix

```bash
# Список функций
curl http://127.0.0.1:8000/functions

# Обновить параметры linear
curl -X PUT http://127.0.0.1:8000/functions/linear \
  -H "Content-Type: application/json" \
  -d '{"a": 2.0, "b": 3.0}'

# Вычислить linear
curl -X POST http://127.0.0.1:8000/functions/linear/call \
  -H "Content-Type: application/json" \
  -d '{"x": 4}'
```

#### Windows

##### PowerShell
```powershell
# Список функций
curl.exe http://127.0.0.1:8000/functions

# Обновить параметры
curl.exe -X PUT http://127.0.0.1:8000/functions/linear `
  -H "Content-Type: application/json" `
  -d '{"a": 2.0, "b": 3.0}'

# Вычислить
curl.exe -X POST http://127.0.0.1:8000/functions/linear/call `
  -H "Content-Type: application/json" `
  -d '{"x": 4}'
```

##### Command Prompt (`cmd`)
```cmd
curl http://127.0.0.1:8000/functions

curl -X PUT http://127.0.0.1:8000/functions/linear ^
  -H "Content-Type: application/json" ^
  -d "{\"a\": 2.0, \"b\": 3.0}"

curl -X POST http://127.0.0.1:8000/functions/linear/call ^
  -H "Content-Type: application/json" ^
  -d "{\"x\": 4}"
```