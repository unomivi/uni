class Item:
    def __init__(self, prev_item=None, next_item=None, item=None):
        self.prev_item = prev_item
        self.next_item = next_item
        self.elem = item


class LinkedListQueue:
    def __init__(self):
        self.head = None
        self.tail = None

    def enqueue(self, item):
        new_item = Item(self.tail, None, item)
        if self.tail is not None:
            self.tail.next_item = new_item
        self.tail = new_item
        if self.head is None:
            self.head = new_item

    def dequeue(self):
        if self.head is None:
            return None
        item = self.head.elem
        self.head = self.head.next_item
        if self.head is None:
            self.tail = None
        return item

    def display(self):
        cur = self.head
        while cur is not None:
            print(cur.elem, end=' ')
            cur = cur.next_item
        print()


if __name__ == '__main__':
    list_nums = [26, 1, 35, -15]
    list_nums_2 = [9, 6, 99]
    queue = LinkedListQueue()
    for num in list_nums:
        queue.enqueue(num)
    print(f'Черга створена:', end=' ')
    queue.display()
    print('Елемент для видалення:', queue.dequeue())
    print('Елемент для видалення:', queue.dequeue())
    print(f'Черга після видалення елементів:', end=' ')
    queue.display()
    for num in list_nums_2:
        queue.enqueue(num)
    print(f'Черга після додавання елементів:', end=' ')
    queue.display()
