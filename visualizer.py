import pygame
import random
import math
pygame.init()

class DrawInformation:
    BLACK = 0, 0, 0
    WHITE = 255, 255, 255
    GREEN = 0, 255, 0
    RED = 255, 0, 0
    BACKGROUND_COLOR = WHITE
    SIDE_PAD = 100
    TOP_PAD = 150
    GRADIENTS = [
        (128, 128, 128),
        (160, 160, 160),
        (192, 192, 192)
    ]
    FONT = pygame.font.SysFont('segoeuisymbol', 20)
    LARGE_FONT = pygame.font.SysFont('segoeuisymbol', 27)

    def __init__(self, width, height, lst):
        self.width = width
        self.height = height
        self.window = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Sorting Visualizer")
        self.set_list(lst)

    def set_list(self, lst):
        self.lst = lst
        self.min_val = min(lst)
        self.max_val = max(lst)
        self.block_width = round((self.width - self.SIDE_PAD) / len(lst))
        self.block_height = math.floor((self.height - self.TOP_PAD) / (self.max_val - self.min_val))
        self.start_x = self.SIDE_PAD // 2

def draw(draw_info, algo_name, ascending):
    draw_info.window.fill(draw_info.BACKGROUND_COLOR)

    title = draw_info.LARGE_FONT.render(f"{algo_name} - {'Ascending' if ascending else 'Descending'}", 1, draw_info.GREEN)
    draw_info.window.blit(title, (draw_info.width / 2 - title.get_width() / 2, 5))

    controls = draw_info.FONT.render("R - Reset | SPACE - Start Sorting | A - Ascending | D - Descending", 1, draw_info.BLACK)
    draw_info.window.blit(controls, (draw_info.width / 2 - controls.get_width() / 2, 45))

    sorting = draw_info.FONT.render("1 - Insertion Sort | 2 - Bubble Sort | 3 - Selection Sort | 4 - Shell Sort | 5 - Merge Sort | 6 - Bogo Sort", 1, draw_info.BLACK)
    draw_info.window.blit(sorting, (draw_info.width / 2 - sorting.get_width() / 2, 75))

    draw_list(draw_info)
    pygame.display.update()

def draw_list(draw_info, color_positions={}, clear_bg=False):
    lst = draw_info.lst

    if clear_bg:
        clear_rect = (draw_info.SIDE_PAD // 2, draw_info.TOP_PAD, 
                      draw_info.width - draw_info.SIDE_PAD, 
                      draw_info.height - draw_info.TOP_PAD)
        
        pygame.draw.rect(draw_info.window, draw_info.BACKGROUND_COLOR, clear_rect)

    for i, val in enumerate(lst):
        x = draw_info.start_x + i * draw_info.block_width
        y = draw_info.height - (val - draw_info.min_val) * draw_info.block_height

        color = draw_info.GRADIENTS[i % 3]

        if i in color_positions:
            color = color_positions[i]

        pygame.draw.rect(draw_info.window, color, (x, y, draw_info.block_width, draw_info.height))
    
    if clear_bg:
        pygame.display.update()

def generate_starting_list(n, min_val, max_val):
    lst = []
    #can use min_val and max_val to get a complete randomized list including duplicates
    #for _ in range(n):
        #val = random.randint(min_val, max_val)
        #lst.append(val)
    while len(lst) != n:
        val = random.randint(1, n)
        if val not in lst:
            lst.append(val)
    return lst

def bubble_sort(draw_info, ascending=True):
    lst = draw_info.lst
    for i in range(len(lst) - 1):
        for j in range(len(lst) - 1 - i):
            num1 = lst[j]
            num2 = lst[j + 1]
            if (num1 > num2 and ascending) or (num1 < num2 and not ascending):
                lst[j], lst[j + 1] = lst[j + 1], lst[j]
                draw_list(draw_info, {j: draw_info.GREEN, j+1: draw_info.RED}, True)
                yield True
    return lst

def insertion_sort(draw_info, ascending=True):
    lst = draw_info.lst
    for i in range(1, len(lst)):
        cur = lst[i]
        while True:
            ascending_sort = i > 0 and lst[i - 1] > cur and ascending
            descending_sort = i > 0 and lst[i - 1] < cur and not ascending
            if not ascending_sort and not descending_sort:
                break
            lst[i] = lst[i - 1]
            i -= 1
            lst[i] = cur
            draw_list(draw_info, {i-1: draw_info.GREEN, i: draw_info.RED}, True)
            yield True
    return lst

def selection_sort(draw_info, ascending=True):
    lst = draw_info.lst
    for i in range(0, len(lst)):
        min_i = i
        for j in range(i + 1, len(lst)):
            if (lst[j] < lst[min_i] and ascending) or (lst[j] > lst[min_i] and not ascending):
                min_i = j
        if min_i != i:
            lst[i], lst[min_i] = lst[min_i], lst[i]
            draw_list(draw_info, {i: draw_info.GREEN, min_i: draw_info.RED}, True)
            yield True
    return lst

def shell_sort(draw_info, ascending=True):
    lst = draw_info.lst
    length = len(lst)
    gap = length // 2
    while gap > 0:
        for i in range(gap, length):
            temp = lst[i]
            j = i
            while j >= gap and ((lst[j - gap] > temp and ascending) 
                                or (lst[j - gap] < temp and not ascending)):
                lst[j] = lst[j - gap]
                j -= gap
                draw_list(draw_info, {j: draw_info.GREEN, j-gap: draw_info.RED}, True)
                yield True
            lst[j] = temp
        gap //= 2
    return lst

def merge_sort(draw_info, ascending=True):
    lst = draw_info.lst
    yield from merge_sort_recursive(draw_info, lst, 0, len(lst) - 1, ascending)

def merge_sort_recursive(draw_info, lst, low, high, ascending):
    if low < high:
        mid = (low + high) // 2
        yield from merge_sort_recursive(draw_info, lst, low, mid, ascending)
        yield from merge_sort_recursive(draw_info, lst, mid + 1, high, ascending)
        yield from merge(draw_info, lst, low, mid, high, ascending)

def merge(draw_info, lst, low, mid, high, ascending):
    left = lst[low:mid + 1]
    right = lst[mid + 1:high + 1]
    i = j = 0
    k = low
    while i < len(left) and j < len(right):
        if (left[i] < right[j] and ascending) or (left[i] > right[j] and not ascending):
            lst[k] = left[i]
            i += 1
        else:
            lst[k] = right[j]
            j += 1
        draw_list(draw_info, {i: draw_info.GREEN, j: draw_info.RED}, True)
        k += 1
    while i < len(left):
        lst[k] = left[i]
        i += 1
        k += 1
        draw_list(draw_info, {i: draw_info.GREEN, k: draw_info.RED}, True)
    while j < len(right):
        lst[k] = right[j]
        j += 1
        k += 1
        draw_list(draw_info, {j: draw_info.GREEN, k: draw_info.RED}, True)
    draw_list(draw_info, {low + i: draw_info.GREEN for i in range(len(left))}, True)
    draw_list(draw_info, {mid + 1 + j: draw_info.RED for j in range(len(right))}, True)
    yield True

def bogo_sort(draw_info, ascending=True):
    lst = draw_info.lst
    sorted_lst = sorted(lst)
    while lst != sorted_lst:
        random.shuffle(lst)
        draw_list(draw_info, {-1: draw_info.GREEN, len(lst): draw_info.RED}, True)
        yield True
    return lst
    
def main():
    run = True
    clock = pygame.time.Clock()
    n = 100
    min_val = 0
    max_val = 100
    lst = generate_starting_list(n, min_val, max_val)
    draw_info = DrawInformation(1600, 1200, lst)
    sorting = False
    ascending = True
    sorting_algorithm = bubble_sort
    sorting_algo_name = "Bubble Sort"
    sorting_algorithm_generator = None

    while run:
        clock.tick(60)
        if sorting:
            try:
                next(sorting_algorithm_generator)
            except StopIteration:
                sorting = False
        else:
            draw(draw_info, sorting_algo_name, ascending)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type != pygame.KEYDOWN:
                continue

            if event.key == pygame.K_r:
                lst = generate_starting_list(n, min_val, max_val)
                draw_info.set_list(lst)
                sorting = False
            elif event.key == pygame.K_SPACE and sorting == False:
                sorting = True
                sorting_algorithm_generator = sorting_algorithm(draw_info, ascending)
            elif event.key == pygame.K_a and not sorting:
                ascending = True
            elif event.key == pygame.K_d and not sorting:
                ascending = False
            elif event.key == pygame.K_1 and not sorting:
                sorting_algorithm = insertion_sort
                sorting_algo_name = "Insertion Sort"
            elif event.key == pygame.K_2 and not sorting:
                sorting_algorithm = bubble_sort
                sorting_algo_name = "Bubble Sort"
            elif event.key == pygame.K_3 and not sorting:
                sorting_algorithm = selection_sort
                sorting_algo_name = "Selection Sort"
            elif event.key == pygame.K_4 and not sorting:
                sorting_algorithm = shell_sort
                sorting_algo_name = "Shell Sort"
            elif event.key == pygame.K_5 and not sorting:
                sorting_algorithm = merge_sort
                sorting_algo_name = "Merge Sort"
            elif event.key == pygame.K_6 and not sorting:
                sorting_algorithm = bogo_sort
                sorting_algo_name = "Bogo Sort"
    pygame.quit()

if __name__ == "__main__":
    main()