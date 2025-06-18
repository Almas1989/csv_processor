# CSV Processor

Утилита для обработки CSV файлов с поддержкой фильтрации и агрегации данных.

## Установка

```bash
pip install -r requirements.txt
```

## Использование

### Основные команды

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

### Поддерживаемые операторы

- `eq` или `==` - равенство
- `gt` или `>` - больше
- `lt` или `<` - меньше

### Поддерживаемые функции агрегации

- `avg` - среднее значение
- `min` - минимальное значение
- `max` - максимальное значение

## Тестирование

```bash
# Запуск тестов
pytest

# Запуск тестов с покрытием кода
pytest --cov=csv_processor --cov-report=html

# Запуск тестов с детальным отчетом
pytest -v --cov=csv_processor --cov-report=term-missing
```

## Примеры работы

### Фильтрация по бренду
```bash
$ python csv_processor.py sample_data.csv --filter "brand=eq=xiaomi"
```

### Агрегация по цене
```bash
$ python csv_processor.py sample_data.csv --aggregate "price=avg"
```

### Комбинированный запрос
```bash
$ python csv_processor.py sample_data.csv --filter "price=gt=400" --aggregate "rating=avg"
```

## Архитектура

Проект построен с использованием паттерна Стратегия для операторов фильтрации и функций агрегации, что позволяет легко добавлять новые операторы и функции без изменения существующего кода.

- `FilterOperator` - абстрактный базовый класс для операторов фильтрации
- `AggregationFunction` - абстрактный базовый класс для функций агрегации
- `CSVProcessor` - основной класс для обработки CSV файлов