#!/usr/bin/env python3
"""
CSV файл процессор с поддержкой фильтрации и агрегации.
"""

import argparse
import csv
import sys
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional, Union
from tabulate import tabulate


class FilterOperator(ABC):
    """Абстрактный базовый класс для операторов фильтрации."""

    @abstractmethod
    def apply(self, value: Any, target: Any) -> bool:
        """Применить оператор фильтрации."""
        pass


class EqualsOperator(FilterOperator):
    """Оператор равенства."""

    def apply(self, value: Any, target: Any) -> bool:
        return str(value).lower() == str(target).lower()


class GreaterOperator(FilterOperator):
    """Оператор больше."""

    def apply(self, value: Any, target: Any) -> bool:
        try:
            return float(value) > float(target)
        except (ValueError, TypeError):
            return False


class LessOperator(FilterOperator):
    """Оператор меньше."""

    def apply(self, value: Any, target: Any) -> bool:
        try:
            return float(value) < float(target)
        except (ValueError, TypeError):
            return False


class AggregationFunction(ABC):
    """Абстрактный базовый класс для функций агрегации."""

    @abstractmethod
    def calculate(self, values: List[float]) -> float:
        """Вычислить результат агрегации."""
        pass


class AverageFunction(AggregationFunction):
    """Функция вычисления среднего значения."""

    def calculate(self, values: List[float]) -> float:
        if not values:
            return 0.0
        return sum(values) / len(values)


class MinFunction(AggregationFunction):
    """Функция вычисления минимального значения."""

    def calculate(self, values: List[float]) -> float:
        if not values:
            return 0.0
        return min(values)


class MaxFunction(AggregationFunction):
    """Функция вычисления максимального значения."""

    def calculate(self, values: List[float]) -> float:
        if not values:
            return 0.0
        return max(values)


class CSVProcessor:
    """Основной класс для обработки CSV файлов."""

    def __init__(self):
        self.operators = {
            'eq': EqualsOperator(),
            'gt': GreaterOperator(),
            'lt': LessOperator()
        }

        self.aggregation_functions = {
            'avg': AverageFunction(),
            'min': MinFunction(),
            'max': MaxFunction()
        }

    def read_csv(self, filepath: str) -> List[Dict[str, Any]]:
        """Читать CSV файл и возвращать список словарей."""
        try:
            with open(filepath, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                return list(reader)
        except FileNotFoundError:
            raise FileNotFoundError(f"Файл {filepath} не найден")
        except Exception as e:
            raise Exception(f"Ошибка при чтении файла: {e}")

    def filter_data(self, data: List[Dict[str, Any]], column: str,
                   operator: str, value: str) -> List[Dict[str, Any]]:
        """Фильтровать данные по заданному условию."""
        if column not in data[0]:
            raise ValueError(f"Колонка '{column}' не найдена в данных")

        if operator not in self.operators:
            raise ValueError(f"Неподдерживаемый оператор: {operator}")

        filter_op = self.operators[operator]
        filtered_data = []

        for row in data:
            if filter_op.apply(row[column], value):
                filtered_data.append(row)

        return filtered_data

    def aggregate_data(self, data: List[Dict[str, Any]], column: str,
                      function: str) -> float:
        """Агрегировать данные по заданной функции."""
        if not data:
            return 0.0

        if column not in data[0]:
            raise ValueError(f"Колонка '{column}' не найдена в данных")

        if function not in self.aggregation_functions:
            raise ValueError(f"Неподдерживаемая функция агрегации: {function}")

        # Извлекаем числовые значения
        numeric_values = []
        for row in data:
            try:
                numeric_values.append(float(row[column]))
            except (ValueError, TypeError):
                # Пропускаем нечисловые значения
                continue

        if not numeric_values:
            raise ValueError(f"В колонке '{column}' нет числовых значений для агрегации")

        agg_func = self.aggregation_functions[function]
        return agg_func.calculate(numeric_values)

    def display_table(self, data: List[Dict[str, Any]], headers: Optional[List[str]] = None):
        """Отобразить данные в виде таблицы."""
        if not data:
            print("Нет данных для отображения")
            return

        if headers is None:
            headers = list(data[0].keys())

        table_data = []
        for row in data:
            table_data.append([row.get(header, '') for header in headers])

        print(tabulate(table_data, headers=headers, tablefmt='grid'))

    def display_aggregation_result(self, column: str, function: str, result: float):
        """Отобразить результат агрегации."""
        function_names = {
            'avg': 'Среднее',
            'min': 'Минимум',
            'max': 'Максимум'
        }

        function_display = function_names.get(function, function.upper())
        table_data = [[column, function_display, f"{result:.2f}"]]
        headers = ['Колонка', 'Функция', 'Результат']

        print(tabulate(table_data, headers=headers, tablefmt='grid'))


def parse_filter(filter_str: str) -> tuple:
    """Парсить строку фильтра в формате column=operator=value."""
    if not filter_str:
        return None, None, None

    parts = filter_str.split('=')
    if len(parts) != 3:
        raise ValueError("Фильтр должен быть в формате: column=operator=value")

    column, operator, value = parts

    # Преобразуем операторы в внутренний формат
    operator_map = {
        '==': 'eq',
        'eq': 'eq',
        '>': 'gt',
        'gt': 'gt',
        '>=': 'gt',
        '<': 'lt',
        'lt': 'lt',
        '<=': 'lt'
    }

    if operator not in operator_map:
        raise ValueError(f"Неподдерживаемый оператор: {operator}")

    return column.strip(), operator_map[operator], value.strip()


def parse_aggregation(agg_str: str) -> tuple:
    """Парсить строку агрегации в формате column=function."""
    if not agg_str:
        return None, None

    parts = agg_str.split('=')
    if len(parts) != 2:
        raise ValueError("Агрегация должна быть в формате: column=function")

    column, function = parts
    return column.strip(), function.strip().lower()


def main():
    """Главная функция."""
    parser = argparse.ArgumentParser(
        description='CSV файл процессор с поддержкой фильтрации и агрегации',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Примеры использования:
  %(prog)s data.csv --filter "price=gt=500"
  %(prog)s data.csv --aggregate "rating=avg"
  %(prog)s data.csv --filter "brand=eq=apple" --aggregate "price=max"
        """
    )

    parser.add_argument('file', help='Путь к CSV файлу')
    parser.add_argument('--filter', '-f',
                       help='Фильтр в формате: column=operator=value (операторы: eq, gt, lt)')
    parser.add_argument('--aggregate', '-a',
                       help='Агрегация в формате: column=function (функции: avg, min, max)')

    args = parser.parse_args()

    processor = CSVProcessor()

    try:
        # Читаем данные
        data = processor.read_csv(args.file)

        if not data:
            print("CSV файл пустой")
            return

        # Применяем фильтрацию если указана
        if args.filter:
            column, operator, value = parse_filter(args.filter)
            data = processor.filter_data(data, column, operator, value)

            if not data:
                print("Нет данных, соответствующих условию фильтрации")
                return

        # Выполняем агрегацию если указана
        if args.aggregate:
            column, function = parse_aggregation(args.aggregate)
            result = processor.aggregate_data(data, column, function)
            processor.display_aggregation_result(column, function, result)
        else:
            # Отображаем отфильтрованные данные
            processor.display_table(data)

    except Exception as e:
        print(f"Ошибка: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()