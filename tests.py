import unittest
from mainfile import Flashcard, PeerFlashcard, CircularPriorityQueue, Stack

class testData(unittest.TestCase):
    def test_queue_isEmpty(self):
        sample_queue = CircularPriorityQueue(10)
        self.assertEqual(sample_queue.isEmpty(), True, "The queue is not recognised as empty.")

    def test_newflashcard_enQueued(self):
        sample_flashcard = Flashcard(1, "Question", "Answer", -1)
        sample_queue = CircularPriorityQueue(1)
        sample_queue.enQueue(sample_flashcard)
        self.assertIsInstance(sample_flashcard.priority, float, "The priority of the new flashcard is wrong.")
        self.assertIn(sample_flashcard.priority, [0.0,1.0,2.0,3.0,4.0,5.0,6.0,7.0,8.0,9.0,10.0], "The priority of the new flashcard is wrong.")

    def test_flashcardpriority_enQueued(self):
        sample_flashcard1 = Flashcard(1, "Question", "Answer", 7)
        sample_flashcard2 = Flashcard(2, "Question", "Answer", 10)
        sample_flashcard3 = Flashcard(3, "Question", "Answer", 3)
        sample_flashcard4 = Flashcard(4, "Question", "Answer", 5)
        sample_flashcard5 = Flashcard(5, "Question", "Answer", 1)
        sample_queue = CircularPriorityQueue(5)
        sample_queue.enQueue(sample_flashcard1)
        sample_queue.enQueue(sample_flashcard2)
        sample_queue.enQueue(sample_flashcard3)
        sample_queue.enQueue(sample_flashcard4)
        sample_queue.enQueue(sample_flashcard5)
        flashcards = sample_queue.getQueue()
        priority_list = [flashcard[1] for flashcard in flashcards if flashcard]
        self.assertEqual(priority_list, sorted(priority_list, reverse=True), "The flashcards are not ordered by priority.")

    def test_flashcardsamepriority_enQueued(self):
        flashcard_enqueue_order = [5, 1, 4]
        sample_flashcard1 = Flashcard(1, "Question", "Answer", 5)
        sample_flashcard2 = Flashcard(2, "Question", "Answer", 10)
        sample_flashcard3 = Flashcard(3, "Question", "Answer", 3)
        sample_flashcard4 = Flashcard(4, "Question", "Answer", 5)
        sample_flashcard5 = Flashcard(5, "Question", "Answer", 5)
        sample_queue = CircularPriorityQueue(5)
        sample_queue.enQueue(sample_flashcard2)
        sample_queue.enQueue(sample_flashcard5)
        sample_queue.enQueue(sample_flashcard3)
        sample_queue.enQueue(sample_flashcard1)
        sample_queue.enQueue(sample_flashcard4)
        flashcards = sample_queue.getQueue()
        samepriority_list = [flashcard[0] for flashcard in flashcards if flashcard and flashcard[1] == 5]
        self.assertEqual(flashcard_enqueue_order, samepriority_list, "Flashcards with the same priority are not enqueued properly.")

    def test_circularwrap_enQueued(self):
        dequeued_flashcards = []
        sample_flashcard1 = Flashcard(1, "Question", "Answer", 7)
        sample_flashcard2 = Flashcard(2, "Question", "Answer", 10)
        sample_flashcard3 = Flashcard(3, "Question", "Answer", 3)
        sample_flashcard4 = Flashcard(4, "Question", "Answer", 5)
        sample_flashcard5 = Flashcard(5, "Question", "Answer", 1)
        sample_flashcard6 = Flashcard(6, "Question", "Answer", 8)
        sample_flashcard7 = Flashcard(7, "Question", "Answer", 4)
        sample_flashcard8 = Flashcard(8, "Question", "Answer", 6)
        sample_queue = CircularPriorityQueue(5)
        sample_queue.enQueue(sample_flashcard1)
        sample_queue.enQueue(sample_flashcard2)
        sample_queue.enQueue(sample_flashcard3)
        sample_queue.enQueue(sample_flashcard4)
        sample_queue.enQueue(sample_flashcard5)
        for _ in range(0, 3):
            sample_queue.deQueue()
        sample_queue.enQueue(sample_flashcard6)
        sample_queue.enQueue(sample_flashcard7)
        sample_queue.enQueue(sample_flashcard8)
        for _ in range(0, 5):
            dequeued_flashcards.append((sample_queue.deQueue()).priority)
        self.assertEqual(dequeued_flashcards, sorted(dequeued_flashcards, reverse=True), "The queue does not wrap around.")

    def test_flashcard_deQueued(self):
        sample_flashcard1 = Flashcard(1, "Question", "Answer", 7)
        sample_flashcard2 = Flashcard(2, "Question", "Answer", 10)
        sample_flashcard3 = Flashcard(3, "Question", "Answer", 3)
        sample_flashcard4 = Flashcard(4, "Question", "Answer", 5)
        sample_flashcard5 = Flashcard(5, "Question", "Answer", 1)
        sample_queue = CircularPriorityQueue(5)
        sample_queue.enQueue(sample_flashcard1)
        sample_queue.enQueue(sample_flashcard2)
        sample_queue.enQueue(sample_flashcard3)
        sample_queue.enQueue(sample_flashcard4)
        sample_queue.enQueue(sample_flashcard5)
        dequeued_flashcard = sample_queue.deQueue()
        flashcards = sample_queue.getQueue()
        priority_list = [flashcard[1] for flashcard in flashcards if flashcard]
        highest_priority = max(priority_list)
        self.assertEqual(dequeued_flashcard.priority, highest_priority, "The flashcard with the highest priority was not dequeued first.")

    def test_stack_isEmpty(self):
        sample_stack = Stack(10)
        self.assertEqual(sample_stack.isEmpty(), True, "The stack is not recognised as empty.")

    def test_stack_pop(self):
        sample_stack = Stack(3)
        sample_flashcard1 = PeerFlashcard(1, "Question", "Answer", 7, "Input")
        sample_flashcard2 = PeerFlashcard(2, "Question", "Answer", 1, "Input")
        sample_flashcard3 = PeerFlashcard(3, "Question", "Answer", 5, "Input")
        sample_stack.push(sample_flashcard1)
        sample_stack.push(sample_flashcard2)
        sample_stack.push(sample_flashcard3)
        popped_flashcard = sample_stack.pop()
        self.assertEqual(popped_flashcard.id, 3, "The last pushed flashcard was not popped first.")

if __name__ == '__main__':
    unittest.main()