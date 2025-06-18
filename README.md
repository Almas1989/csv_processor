# 📂 CSV Processor

Утилита для обработки CSV файлов с поддержкой фильтрации и агрегации данных.

---

## 🗂 Описание (на русском)

### 📦 Установка

```bash
pip install -r requirements.txt
```

### 🚀 Использование

```bash
# Показать все данные
python csv_processor.py sample_data.csv

# Фильтрация по равенству
python csv_processor.py sample_data.csv --filter "brand=eq=xiaomi"

# Фильтрация по числовым значениям
python csv_processor.py sample_data.csv --filter "price=gt=500"
python csv_processor.py sample_data.csv --filter "rating=lt=4.5"

# Агрегация данных
python csv_processor.py sample_data.csv --aggregate "price=avg"
python csv_processor.py sample_data.csv --aggregate "rating=min"
python csv_processor.py sample_data.csv --aggregate "price=max"

# Комбинирование фильтрации и агрегации
python csv_processor.py sample_data.csv --filter "brand=eq=xiaomi" --aggregate "price=avg"
```

### 🔧 Поддерживаемые операторы

- `eq` или `==` — равенство
- `gt` или `>` — больше
- `lt` или `<` — меньше

### 📊 Поддерживаемые функции агрегации

- `avg` — среднее значение
- `min` — минимальное значение
- `max` — максимальное значение

### 🧪 Тестирование

```bash
# Запуск тестов
pytest

# Покрытие кода (HTML-отчет)
pytest --cov=csv_processor --cov-report=html

# Подробный отчет в терминале
pytest -v --cov=csv_processor --cov-report=term-missing
```

### 💡 Примеры

```bash
# Фильтрация по бренду
python csv_processor.py sample_data.csv --filter "brand=eq=xiaomi"

# Агрегация по цене
python csv_processor.py sample_data.csv --aggregate "price=avg"

# Комбинированный запрос
python csv_processor.py sample_data.csv --filter "price=gt=400" --aggregate "rating=avg"
```

### 🧱 Архитектура

Проект реализован с использованием паттерна **Стратегия**, что позволяет легко добавлять новые операторы фильтрации и агрегации без изменения основного кода.

- `FilterOperator` — базовый класс операторов фильтрации
- `AggregationFunction` — базовый класс агрегационных функций
- `CSVProcessor` — основной класс обработки данных

---

## 📘 Description (in English)

### 📦 Installation

```bash
pip install -r requirements.txt
```

### 🚀 Usage

```bash
# Show all data
python csv_processor.py sample_data.csv

# Filter by equality
python csv_processor.py sample_data.csv --filter "brand=eq=xiaomi"

# Filter by numeric values
python csv_processor.py sample_data.csv --filter "price=gt=500"
python csv_processor.py sample_data.csv --filter "rating=lt=4.5"

# Aggregate data
python csv_processor.py sample_data.csv --aggregate "price=avg"
python csv_processor.py sample_data.csv --aggregate "rating=min"
python csv_processor.py sample_data.csv --aggregate "price=max"

# Combine filtering and aggregation
python csv_processor.py sample_data.csv --filter "brand=eq=xiaomi" --aggregate "price=avg"
```

### 🔧 Supported Operators

- `eq` or `==` — equal
- `gt` or `>` — greater than
- `lt` or `<` — less than

### 📊 Supported Aggregation Functions

- `avg` — average
- `min` — minimum
- `max` — maximum

### 🧪 Testing

```bash
# Run tests
pytest

# Code coverage (HTML report)
pytest --cov=csv_processor --cov-report=html

# Verbose terminal report
pytest -v --cov=csv_processor --cov-report=term-missing
```

### 💡 Examples

```bash
# Filter by brand
python csv_processor.py sample_data.csv --filter "brand=eq=xiaomi"

# Aggregate price
python csv_processor.py sample_data.csv --aggregate "price=avg"

# Combined query
python csv_processor.py sample_data.csv --filter "price=gt=400" --aggregate "rating=avg"
```

### 🧱 Architecture

The project uses the **Strategy pattern**, which makes it easy to add new filtering operators or aggregation functions without modifying core logic.

- `FilterOperator` — base class for filtering operators
- `AggregationFunction` — base class for aggregation functions
- `CSVProcessor` — main processing class