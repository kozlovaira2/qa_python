import pytest
from main import BooksCollector

# класс TestBooksCollector объединяет набор тестов, которыми мы покрываем наше приложение BooksCollector
# обязательно указывать префикс Test
class TestBooksCollector:

    # пример теста:
    # обязательно указывать префикс test_
    # дальше идет название метода, который тестируем add_new_book_
    # затем, что тестируем add_two_books - добавление двух книг
    def test_add_new_book_add_two_books(self):
        # создаем экземпляр (объект) класса BooksCollector
        collector = BooksCollector()

        # добавляем две книги
        collector.add_new_book('Гордость и предубеждение и зомби')
        collector.add_new_book('Что делать, если ваш кот хочет вас убить')

        # проверяем, что добавилось именно две
        # словарь books_rating (неверно указан словарь, должен быть books_genre), который нам возвращает метод get_books_rating (get_books_genre), имеет длину 2
        assert len(collector.get_books_genre()) == 2

    # напиши свои тесты ниже
    # чтобы тесты были независимыми в каждом из них создавай отдельный экземпляр класса BooksCollector()

    @pytest.mark.parametrize("name", ["Война и мир", "А" * 40, "Название с пробелами"])
    def test_add_new_book_valid_name(self, name):
        """Добавление книги с валидным названием (длина 1-40 символов)"""
        collector = BooksCollector()
        collector.add_new_book(name)
        assert name in collector.get_books_genre()
        assert collector.get_book_genre(name) == ""

    # Тесты для set_book_genre и get_book_genre
    @pytest.mark.parametrize("genre", ["Фантастика", "Ужасы", "Детективы", "Мультфильмы", "Комедии"])
    def test_set_book_genre_valid_genre(self, genre):
        """Установка валидного жанра для существующей книги"""
        collector = BooksCollector()
        collector.add_new_book("Книга")
        collector.set_book_genre("Книга", genre)
        assert collector.get_book_genre("Книга") == genre

    def test_set_book_genre_for_nonexistent_book(self):
        """Установка жанра для несуществующей книги"""
        collector = BooksCollector()
        collector.add_new_book("Существующая")
        collector.set_book_genre("Несуществующая", "Фантастика")
        assert "Несуществующая" not in collector.get_books_genre()
        assert collector.get_book_genre("Существующая") == ""

    def test_set_book_genre_invalid_genre(self):
        """Установка жанра, которого нет в списке genre"""
        collector = BooksCollector()
        collector.add_new_book("Книга")
        collector.set_book_genre("Книга", "Несуществующий жанр")
        assert collector.get_book_genre("Книга") == ""

    # Тесты для get_books_with_specific_genre
    @pytest.mark.parametrize("genre, expected_count", [
        ("Фантастика", 2),
        ("Ужасы", 1),
        ("Комедии", 0)
    ])
    def test_get_books_with_specific_genre(self, genre, expected_count):
        """Получение списка книг определённого жанра"""
        collector = BooksCollector()
        collector.add_new_book("Книга1")
        collector.add_new_book("Книга2")
        collector.add_new_book("Книга3")
        collector.set_book_genre("Книга1", "Фантастика")
        collector.set_book_genre("Книга2", "Фантастика")
        collector.set_book_genre("Книга3", "Ужасы")
        
        books = collector.get_books_with_specific_genre(genre)
        assert len(books) == expected_count
        if expected_count > 0:
            assert all(collector.get_book_genre(book) == genre for book in books)

    def test_get_books_with_specific_genre_empty(self):
        """Запрос книг по жанру, когда словарь пуст"""
        collector = BooksCollector()
        assert collector.get_books_with_specific_genre("Фантастика") == []

    # Тесты для get_books_for_children
    @pytest.mark.parametrize("genre, should_be_in_children", [
        ("Фантастика", True),
        ("Мультфильмы", True),
        ("Комедии", True),
        ("Ужасы", False),
        ("Детективы", False)
    ])
    def test_get_books_for_children(self, genre, should_be_in_children):
        """Книги с возрастным рейтингом не попадают в детский список"""
        collector = BooksCollector()
        collector.add_new_book("Детская книга")
        collector.set_book_genre("Детская книга", genre)
        
        children_books = collector.get_books_for_children()
        if should_be_in_children:
            assert "Детская книга" in children_books
        else:
            assert "Детская книга" not in children_books

    def test_get_books_for_children_no_genre(self):
        """Книга без жанра не попадает в детский список"""
        collector = BooksCollector()
        collector.add_new_book("Без жанра")
        children_books = collector.get_books_for_children()
        assert "Без жанра" not in children_books

    # Тест для add_book_in_favorites
    def test_add_book_in_favorites(self):
        """Добавление существующей книги в избранное"""
        collector = BooksCollector()
        collector.add_new_book("Избранная")
        collector.add_book_in_favorites("Избранная")
        assert "Избранная" in collector.get_list_of_favorites_books()

    # Тест для delete_book_from_favorites
    def test_delete_book_from_favorites(self):
        """Удаление книги из избранного"""
        collector = BooksCollector()
        collector.add_new_book("Удаляемая")
        collector.add_book_in_favorites("Удаляемая")
        collector.delete_book_from_favorites("Удаляемая")
        assert "Удаляемая" not in collector.get_list_of_favorites_books()

    # Тест для get_books_genre
    def test_get_books_genre_returns_copy(self):
        """Проверка, что get_books_genre возвращает актуальный словарь"""
        collector = BooksCollector()
        collector.add_new_book("Книга1")
        collector.add_new_book("Книга2")
        books_dict = collector.get_books_genre()
        assert len(books_dict) == 2
        assert "Книга1" in books_dict
        assert "Книга2" in books_dict