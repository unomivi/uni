import colorama
from colorama import Fore
colorama.init()

class Item:
    def __init__(self, elem):
        self.elem = elem
        self.next_item = None
        self.prev_item = None

class DoubleLinkedList:
    def __init__(self):
        self.head = None
        self.tail = None
        self.size = 0
    
    def insert_to_end(self, elem):
        new_item = Item(elem)
        if self.head is None:
            self.head = self.tail = new_item
        else:
            new_item.prev_item = self.tail
            self.tail.next_item = new_item
            self.tail = new_item
        self.size += 1
    
    def display(self):
        current = self.head
        index = 0
        while current:
            print(Fore.YELLOW + f"{index}: {current.elem}")
            current = current.next_item
            index += 1
        print(Fore.CYAN + "------------------------------")

    def display_words_not_first_letter(self, first_word):
        current = self.head
        index = 0
        while current:
            if current.elem[0] != first_word[0]:
                print(Fore.YELLOW + f"{index}: {current.elem}")
            current = current.next_item
            index += 1
        print(Fore.CYAN + "------------------------------")
    
    def capitalize_all_words(self):
        current = self.head
        while current:
            current.elem = current.elem.capitalize()
            current = current.next_item

while True:
    text = input("\nВведіть текст (має закінчуватися крапкою та містити малі літери): ")
    if text.islower() and text.endswith("."):
        print(Fore.CYAN + "\nНаш початковий текст:" + Fore.RESET, text)
        text = text.replace(".", "").replace(",", "").split()
        if len(text) < 2:
            print(Fore.RED + "\nТекст має містити хоча б два слова!" + Fore.RESET)
            continue
        break
    else:
        print(Fore.RED + "\nТекст має бути маленькими літерами та закінчуватися крапкою!" + Fore.RESET)

linked_list = DoubleLinkedList()
for word in text:
    linked_list.insert_to_end(word)

print(Fore.GREEN + "\nСлова, які не починаються з тієї ж літери, що перше слово:")
linked_list.display_words_not_first_letter(text[0])

linked_list.capitalize_all_words()
print(Fore.GREEN + "\nСлова з великої літери:")
linked_list.display()

print(Fore.MAGENTA + "\nДякую!" + Fore.RESET)
