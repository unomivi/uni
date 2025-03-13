import time
import os
import re
from dataclasses import dataclass


FILENAME = "words.txt"


@dataclass
class TreeNode:
    word: str
    left: 'TreeNode' = None
    right: 'TreeNode' = None


class BinarySearchTree:
    def __init__(self):
        self.root = None
   
    def insert(self, word):
        if not word:
            return False
        word = word.lower()
        if not self.root:
            self.root = TreeNode(word)
            return True
        return self._insert_recursive(self.root, word)
   
    def _insert_recursive(self, node, word):
        if word == node.word:
            return False
        if word < node.word:
            if node.left is None:
                node.left = TreeNode(word)
                return True
            return self._insert_recursive(node.left, word)
        else:
            if node.right is None:
                node.right = TreeNode(word)
                return True
            return self._insert_recursive(node.right, word)
   
    def search(self, word):
        if not word or not self.root:
            return False
        word = word.lower()
        return self._search_recursive(self.root, word)
   
    def _search_recursive(self, node, word):
        if node is None:
            return False
        if word == node.word:
            return True
        if word < node.word:
            return self._search_recursive(node.left, word)
        else:
            return self._search_recursive(node.right, word)
   
    def delete(self, word):
        if not word or not self.root:
            return False
        word = word.lower()
        result, self.root = self._delete_recursive(self.root, word)
        return result
   
    def _delete_recursive(self, node, word):
        if node is None:
            return False, None
        if word < node.word:
            deleted, node.left = self._delete_recursive(node.left, word)
            return deleted, node
        elif word > node.word:
            deleted, node.right = self._delete_recursive(node.right, word)
            return deleted, node
        else:
            # Вузол знайдено
            if node.left is None:
                return True, node.right
            elif node.right is None:
                return True, node.left
            successor = self._find_min(node.right)
            node.word = successor.word
            deleted, node.right = self._delete_recursive(node.right, successor.word)
            return True, node
   
    def _find_min(self, node):
        current = node
        while current.left:
            current = current.left
        return current
   
    def print_tree(self):
        if not self.root:
            print("Дерево порожнє")
            return
        lines, *_ = display_aux(self.root)
        for line in lines:
            print(line)


# Функція для гарного горизонтального відображення дерева (root вгорі)
def display_aux(root):
    """
    Повертає список рядків, ширину, висоту та координату центру кореневого вузла.
    """
    if root is None:
        return [], 0, 0, 0


    line = str(root.word)
    width = len(line)


    if root.left is None and root.right is None:
        return [line], width, 1, width // 2


    if root.right is None:
        left_lines, n, p, x = display_aux(root.left)
        first_line = (x + 1) * " " + (n - x - 1) * "_" + line
        second_line = x * " " + "/" + (n - x - 1 + width) * " "
        shifted_lines = [l + width * " " for l in left_lines]
        return [first_line, second_line] + shifted_lines, n + width, p + 2, n + width // 2


    if root.left is None:
        right_lines, m, q, y = display_aux(root.right)
        first_line = line + y * "_" + (m - y) * " "
        second_line = (width + y) * " " + "\\" + (m - y - 1) * " "
        shifted_lines = [width * " " + r for r in right_lines]
        return [first_line, second_line] + shifted_lines, m + width, q + 2, width // 2


    left_lines, n, p, x = display_aux(root.left)
    right_lines, m, q, y = display_aux(root.right)
    first_line = (x + 1) * " " + (n - x - 1) * "_" + line + y * "_" + (m - y) * " "
    second_line = x * " " + "/" + (n - x - 1 + width + y) * " " + "\\" + (m - y - 1) * " "
    if p < q:
        left_lines += [n * " "] * (q - p)
    elif q < p:
        right_lines += [m * " "] * (p - q)
    zipped_lines = [a + width * " " + b for a, b in zip(left_lines, right_lines)]
    return [first_line, second_line] + zipped_lines, n + m + width, max(p, q) + 2, n + width // 2


# Робота з файлом


def read_words_from_file(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            text = f.read()
        # Видаляємо знаки пунктуації та зайві пробіли
        text = re.sub(r'[^\w\s]', ' ', text)
        text = re.sub(r'\s+', ' ', text)
        return text.lower().split()
    except FileNotFoundError:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("це тестовий текст для перевірки роботи програми")
        return read_words_from_file(filename)
    except Exception as e:
        print(f"Помилка при читанні файлу: {e}")
        return []


def save_words_to_file(filename, words):
    try:
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(' '.join(words))
    except Exception as e:
        print(f"Помилка при збереженні файлу: {e}")


def linear_search_in_file(filename, word):
    words = read_words_from_file(filename)
    word = word.lower()
    start_time = time.perf_counter()
    found = word in words
    end_time = time.perf_counter()
    return found, end_time - start_time


def search_in_tree(tree, word):
    word = word.lower()
    start_time = time.perf_counter()
    found = tree.search(word)
    end_time = time.perf_counter()
    return found, end_time - start_time


def add_word(tree, filename, word):
    if not word:
        return
    word = word.lower()
    start_time = time.perf_counter()
    added = tree.insert(word)
    if added:
        words = read_words_from_file(filename)
        words.append(word)
        save_words_to_file(filename, words)
        end_time = time.perf_counter()
        print(f"Слово '{word}' додано. Час: {end_time - start_time:.8f} сек.")
    else:
        end_time = time.perf_counter()
        print(f"Слово '{word}' вже існує. Час: {end_time - start_time:.8f} сек.")


def delete_word(tree, filename, word):
    if not word:
        return
    word = word.lower()
    start_time = time.perf_counter()
    deleted = tree.delete(word)
    if deleted:
        words = read_words_from_file(filename)
        words = [w for w in words if w != word]
        save_words_to_file(filename, words)
        end_time = time.perf_counter()
        print(f"Слово '{word}' видалено. Час: {end_time - start_time:.8f} сек.")
    else:
        end_time = time.perf_counter()
        print(f"Слово '{word}' не знайдено. Час: {end_time - start_time:.8f} сек.")


def main():
    # Переконуємось, що файл існує та не порожній
    if not os.path.exists(FILENAME) or os.path.getsize(FILENAME) == 0:
        with open(FILENAME, 'w', encoding='utf-8') as file:
            file.write("це тестовий текст для перевірки роботи програми бінарного дерева пошуку")
   
    tree = BinarySearchTree()
    for word in read_words_from_file(FILENAME):
        tree.insert(word)
   
    print("Бінарне дерево:")
    tree.print_tree()


    try:
        while True:
            word = input("\nСлово для пошуку: ").strip().lower()


            found_tree, time_tree = search_in_tree(tree, word)
            found_file, time_file = linear_search_in_file(FILENAME, word)
           
            print(f"Дерево: {'Знайдено' if found_tree else 'Не знайдено'}. Час: {time_tree:.8f} сек.")
            print(f"Файл: {'Знайдено' if found_file else 'Не знайдено'}. Час: {time_file:.8f} сек.")
           
            if time_tree < time_file:
                print(f"Дерево швидше у {time_file/time_tree:.2f} разів")
            else:
                print(f"Файл швидше у {time_tree/time_file:.2f} разів")
           
            if found_tree:
                if input(f"Видалити '{word}'? (так/ні): ").strip().lower() in ["так", "yes", "y", "т"]:
                    delete_word(tree, FILENAME, word)
                    print("\nОновлене дерево:")
                    tree.print_tree()
            else:
                if input(f"Додати '{word}'? (так/ні): ").strip().lower() in ["так", "yes", "y", "т"]:
                    add_word(tree, FILENAME, word)
                    print("\nОновлене дерево:")
                    tree.print_tree()


    except KeyboardInterrupt:
        print("\nПрограму завершено")


if __name__ == "__main__":
    main()