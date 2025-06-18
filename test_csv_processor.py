import pytest
import tempfile
import os
from unittest.mock import patch, mock_open
from csv_processor import (
    CSVProcessor,
    EqualsOperator,
    GreaterOperator,
    LessOperator,
    AverageFunction,
    MinFunction,
    MaxFunction,
    parse_filter,
    parse_aggregation
)


class TestFilterOperators:
    """Тесты для операторов фильтрации."""

    def test_equals_operator(self):
        op = EqualsOperator()
        assert op.apply("apple", "apple") is True
        assert op.apply("Apple", "apple") is True  # case insensitive
        assert op.apply("apple", "samsung") is False
        assert op.apply("123", "123") is True

    def test_greater_operator(self):
        op = GreaterOperator()
        assert op.apply("10", "5") is True
        assert op.apply("5", "10") is False
        assert op.apply("10.5", "10") is True
        assert op.apply("not_a_number", "5") is False
        assert op.apply("5", "not_a_number") is False

    def test_less_operator(self):
        op = LessOperator()
        assert op.apply("5", "10") is True
        assert op.apply("10", "5") is False
        assert op.apply("9.5", "10") is True
        assert op.apply("not_a_number", "5") is False
        assert op.apply("5", "not_a_number") is False


class TestAggregationFunctions:
    """Тесты для функций агрегации."""

    def test_average_function(self):
        func = AverageFunction()
        assert func.calculate([1, 2, 3, 4, 5]) == 3.0
        assert func.calculate([10.5, 20.5]) == 15.5
        assert func.calculate([]) == 0.0
        assert func.calculate([42]) == 42.0

    def test_min_function(self):
        func = MinFunction()
        assert func.calculate([1, 2, 3, 4, 5]) == 1
        assert func.calculate([10.5, 5.2, 20.8]) == 5.2
        assert func.calculate([]) == 0.0
        assert func.calculate([42]) == 42

    def test_max_function(self):
        func = MaxFunction()
        assert func.calculate([1, 2, 3, 4, 5]) == 5
        assert func.calculate([10.5, 5.2, 20.8]) == 20.8
        assert func.calculate([]) == 0.0
        assert func.calculate([42]) == 42


class TestCSVProcessor:
    """Тесты для основного класса CSVProcessor."""

    @pytest.fixture
    def processor(self):
        return CSVProcessor()

    @pytest.fixture
    def sample_data(self):
        return [
            {'name': 'iphone 15 pro', 'brand': 'apple', 'price': '999', 'rating': '4.9'},
            {'name': 'galaxy s23 ultra', 'brand': 'samsung', 'price': '1199', 'rating': '4.8'},
            {'name': 'redmi note 12', 'brand': 'xiaomi', 'price': '199', 'rating': '4.6'},
            {'name': 'poco x5 pro', 'brand': 'xiaomi', 'price': '299', 'rating': '4.4'}
        ]

    def test_read_csv_success(self, processor):
        csv_content = "name,brand,price,rating\niphone 15 pro,apple,999,4.9\ngalaxy s23,samsung,800,4.7"

        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            f.write(csv_content)
            temp_path = f.name

        try:
            data = processor.read_csv(temp_path)
            assert len(data) == 2
            assert data[0]['name'] == 'iphone 15 pro'
            assert data[0]['brand'] == 'apple'
            assert data[1]['name'] == 'galaxy s23'
        finally:
            os.unlink(temp_path)

    def test_read_csv_file_not_found(self, processor):
        with pytest.raises(FileNotFoundError):
            processor.read_csv('nonexistent_file.csv')

    def test_filter_data_equals(self, processor, sample_data):
        result = processor.filter_data(sample_data, 'brand', 'eq', 'xiaomi')
        assert len(result) == 2
        assert all(row['brand'] == 'xiaomi' for row in result)

    def test_filter_data_greater(self, processor, sample_data):
        result = processor.filter_data(sample_data, 'price', 'gt', '500')
        assert len(result) == 2
        assert all(float(row['price']) > 500 for row in result)

    def test_filter_data_less(self, processor, sample_data):
        result = processor.filter_data(sample_data, 'price', 'lt', '500')
        assert len(result) == 2
        assert all(float(row['price']) < 500 for row in result)

    def test_filter_data_invalid_column(self, processor, sample_data):
        with pytest.raises(ValueError, match="Колонка 'invalid_column' не найдена"):
            processor.filter_data(sample_data, 'invalid_column', 'eq', 'value')

    def test_filter_data_invalid_operator(self, processor, sample_data):
        with pytest.raises(ValueError, match="Неподдерживаемый оператор"):
            processor.filter_data(sample_data, 'brand', 'invalid_op', 'value')

    def test_aggregate_data_average(self, processor, sample_data):
        result = processor.aggregate_data(sample_data, 'price', 'avg')
        expected = (999 + 1199 + 199 + 299) / 4
        assert result == expected

    def test_aggregate_data_min(self, processor, sample_data):
        result = processor.aggregate_data(sample_data, 'price', 'min')
        assert result == 199.0

    def test_aggregate_data_max(self, processor, sample_data):
        result = processor.aggregate_data(sample_data, 'price', 'max')
        assert result == 1199.0

    def test_aggregate_data_empty_data(self, processor):
        result = processor.aggregate_data([], 'price', 'avg')
        assert result == 0.0

    def test_aggregate_data_invalid_column(self, processor, sample_data):
        with pytest.raises(ValueError, match="Колонка 'invalid_column' не найдена"):
            processor.aggregate_data(sample_data, 'invalid_column', 'avg')

    def test_aggregate_data_invalid_function(self, processor, sample_data):
        with pytest.raises(ValueError, match="Неподдерживаемая функция агрегации"):
            processor.aggregate_data(sample_data, 'price', 'invalid_func')

    def test_aggregate_data_non_numeric_column(self, processor, sample_data):
        with pytest.raises(ValueError, match="нет числовых значений для агрегации"):
            processor.aggregate_data(sample_data, 'name', 'avg')

    @patch('builtins.print')
    def test_display_table(self, mock_print, processor, sample_data):
        processor.display_table(sample_data)
        mock_print.assert_called()

    @patch('builtins.print')
    def test_display_table_empty_data(self, mock_print, processor):
        processor.display_table([])
        mock_print.assert_called_with("Нет данных для отображения")

    @patch('builtins.print')
    def test_display_aggregation_result(self, mock_print, processor):
        processor.display_aggregation_result('price', 'avg', 674.0)
        mock_print.assert_called()


class TestParseFunctions:
    """Тесты для функций парсинга."""

    def test_parse_filter_success(self):
        column, operator, value = parse_filter("price=gt=500")
        assert column == "price"
        assert operator == "gt"
        assert value == "500"

    def test_parse_filter_with_equals_operator(self):
        column, operator, value = parse_filter("brand=eq=apple")
        assert column == "brand"
        assert operator == "eq"
        assert value == "apple"

    def test_parse_filter_with_symbolic_operators(self):
        column, operator, value = parse_filter("price=>=500")
        assert column == "price"
        assert operator == "gt"
        assert value == "500"

        column, operator, value = parse_filter("price=<=500")
        assert column == "price"
        assert operator == "lt"
        assert value == "500"

    def test_parse_filter_empty_string(self):
        result = parse_filter("")
        assert result == (None, None, None)

    def test_parse_filter_invalid_format(self):
        with pytest.raises(ValueError, match="Фильтр должен быть в формате"):
            parse_filter("invalid_format")

    def test_parse_filter_invalid_operator(self):
        with pytest.raises(ValueError, match="Неподдерживаемый оператор"):
            parse_filter("price=invalid=500")

    def test_parse_aggregation_success(self):
        column, function = parse_aggregation("price=avg")
        assert column == "price"
        assert function == "avg"

    def test_parse_aggregation_empty_string(self):
        result = parse_aggregation("")
        assert result == (None, None)

    def test_parse_aggregation_invalid_format(self):
        with pytest.raises(ValueError, match="Агрегация должна быть в формате"):
            parse_aggregation("invalid_format")

    def test_parse_aggregation_case_insensitive(self):
        column, function = parse_aggregation("price=AVG")
        assert column == "price"
        assert function == "avg"


class TestIntegration:
    """Интеграционные тесты."""

    @pytest.fixture
    def csv_file(self):
        csv_content = """name,brand,price,rating
iphone 15 pro,apple,999,4.9
galaxy s23 ultra,samsung,1199,4.8
redmi note 12,xiaomi,199,4.6
poco x5 pro,xiaomi,299,4.4"""

        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            f.write(csv_content)
            temp_path = f.name

        yield temp_path
        os.unlink(temp_path)

    def test_filter_and_aggregate_together(self, csv_file):
        processor = CSVProcessor()

        # Читаем данные
        data = processor.read_csv(csv_file)

        # Фильтруем данные (только xiaomi)
        filtered_data = processor.filter_data(data, 'brand', 'eq', 'xiaomi')

        # Агрегируем отфильтрованные данные
        result = processor.aggregate_data(filtered_data, 'price', 'avg')

        # Проверяем результат (среднее из 199 и 299)
        expected = (199 + 299) / 2
        assert result == expected

    def test_filter_no_results(self, csv_file):
        processor = CSVProcessor()
        data = processor.read_csv(csv_file)

        # Фильтр, который не должен найти результатов
        filtered_data = processor.filter_data(data, 'brand', 'eq', 'nonexistent')

        assert len(filtered_data) == 0