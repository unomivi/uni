class CircularQueue:
    def __init__(self, size):
        self.size = size
        self.queue = [None] * size
        self.head = self.tail = -1

    def enqueue(self, item):
        if (self.tail + 1) % self.size == self.head:
            print('Черга заповнена')
        elif self.head == -1:
            self.head = 0
            self.tail = 0
            self.queue[self.tail] = item
        else:
            self.tail = (self.tail + 1) % self.size
            self.queue[self.tail] = item

    def dequeue(self):
        if self.head == -1:
            print('Черга порожня')
        elif self.head == self.tail:
            temp = self.queue[self.head]
            self.head = -1
            self.tail = -1
            return temp
        else:
            temp = self.queue[self.head]
            self.head = (self.head + 1) % self.size
            return temp

    def display(self):
        if self.head == -1:
            print('Черга порожня')
        elif self.tail >= self.head:
            for i in range(self.head, self.tail + 1):
                print(self.queue[i], end=' ')
            print()
        else:
            for i in range(self.head, self.size):
                print(self.queue[i], end=' ')
            for i in range(0, self.tail + 1):
                print(self.queue[i], end=' ')
            print()


if __name__ == '__main__':
    list_nums = [15, 33, 56, -8]
    list_nums_2 = [25, 90, 69]
    queue = CircularQueue(5)
    for num in list_nums:
        queue.enqueue(num)
    print(f'Створена черга:', end=' ')
    queue.display()
    print(f'Елемент для видалення: {queue.dequeue()}')
    print(f'Елемент для видалення: {queue.dequeue()}')
    print(f'Черга після видалення елементів:', end=' ')
    queue.display()
    for num in list_nums_2:
        queue.enqueue(num)
    print(f'Черга після додавання елементів:', end=' ')
    queue.display()

