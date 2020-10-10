import random
import copy
import solver


class sudoku():

    def __init__(self, size):
        #define size of sudoku
        self.size = size
        #count of sudoku
        self.count = self.size*self.size
        self.count_of_permutation = random.randint(10, 1000)
        #generate array of integer
        self.generate()
        self.make_sudoku()
        self.field = self.to_normal_ar()

    def generate(self):
        ar = [[[] for j in range(self.size)] for i in range(self.count)]
        series_of_num = [i for i in range(1, self.count+1)]
        movement = [i for i in range(self.size)]
        for i in range(self.count):
            if i % self.size == 0:
                series_of_num = [i for i in range(1, self.count+1)]
                shift = random.choice(movement)
                series_of_num = series_of_num[shift:]+series_of_num[0:shift]
                for _ in range(self.size):
                    if movement[_] == shift:
                        del movement[_]
                        break
            for j in range(self.size):
                ar[i][j] = series_of_num[(
                    i % self.size)*self.size:(i % self.size+1)*self.size]
                series_of_num = series_of_num[self.size:] + \
                    series_of_num[0:self.size]
        self.field = ar
        for _ in range(self.count_of_permutation):
            random.choice([self.transposing(), 
            self.swap_rows(), self.swap_colums(),
            self.swap_area_horizontal(), self.swap_area_vertical()])

    def transposing(self):
        ar = self.to_normal_ar()
        result = [[0 for j in range(self.count)] for i in range(self.count)]
        for i in range(self.count):
            for j in range(self.count):
                result[j][i] = ar[i][j]
        ar = result
        result = [[[] for j in range(self.size)] for i in range(self.count)]
        for j in range(0, self.count, int(self.count/self.size)):
            for i in range(self.size):
                for q in range(self.size):
                    result[j+q][i] = ar[j+i][q*self.size:(q+1)*self.size]
        self.field = result

    def swap_rows(self):
        area = random.randint(0,self.size - 1)
        first_r = random.randint(0, self.size - 1) + area*self.size
        second_r = random.randint(0, self.size - 1) + area*self.size
        while(first_r == second_r):
            first_r =  random.randint(0, self.size - 1) + area*self.size
        first = [first_r, area, first_r % self.size]
        second = [second_r, area, second_r % self.size]
        for i in range(self.size):
            self.field[first[1]*self.size+i][first[2]], self.field[second[1]*self.size+i][second[2]
                                                                                          ] = self.field[second[1]*self.size+i][second[2]], self.field[first[1]*self.size+i][first[2]]

    def swap_colums(self):
        area = random.randint(0,self.size - 1)
        first_c = random.randint(0, self.size - 1) + area*self.size
        second_c = random.randint(0, self.size - 1) + area*self.size
        while(first_c == second_c):
            first_c =  random.randint(0, self.size - 1) + area*self.size
        first = [first_c, area, first_c % self.size]
        second = [second_c, area, second_c % self.size]
        for i in range(0, self.count, self.size):
            for j in range(self.size):
                self.field[first[1]+i][j][first[2]], self.field[second[1]+i][j][second[2]
                                                                                ] = self.field[second[1]+i][j][second[2]], self.field[first[1]+i][j][first[2]]

    def swap_area_horizontal(self):
        first_a = random.randint(0, 2)
        second_a = random.randint(0, 2)
        while(first_a == second_a):
            second_a = random.randint(0, 2)
        for i in range(self.size):
            self.field[first_a*self.size + i], self.field[second_a*self.size +
                                                          i] = self.field[second_a*self.size + i], self.field[first_a*self.size + i]

    def swap_area_vertical(self):
        first_a = random.randint(0, 2)
        second_a = random.randint(0, 2)
        while(first_a == second_a):
            second_a = random.randint(0, 2)
        for i in range(0, self.count, self.size):
            self.field[first_a + i], self.field[second_a +
                                                i] = self.field[second_a + i], self.field[first_a + i]

    def make_sudoku(self):
        self.solution = copy.copy(self.field)
        visited = [[[False for q in range(self.size)] for j in range(
            self.size)] for i in range(self.count)]
        self.difficult = self.count*self.count
        #we will watch every single cage and i - count of visited cage
        i = 0
        while i < self.count**2:
            area = random.randint(0, 8)
            row = random.randint(0, 2)
            colum = random.randint(0, 2)
            if not(visited[area][row][colum]):
                visited[area][row][colum] = True
                i += 1
                temp = self.field[area][row][colum]
                self.field[area][row][colum] = 0
                self.difficult -= 1
                temp_field = copy.copy(self.field)
                i_solution = 0
                for solution in solver.solve_sudoku((self.size, self.size), self.to_normal_ar()):
                    i_solution += 1
                if i_solution != 1:
                    self.field[area][row][colum] = temp
                    self.difficult += 1
        self.solution = [i for i in solver.solve_sudoku((3, 3), self.to_normal_ar())][0]

    def to_normal_ar(self):
        ar = [[] for i in range(self.count)]
        for j in range(0, self.count, int(self.count/self.size)):
            for i in range(self.size):
                for q in range(self.size):
                    ar[j+i] += self.field[j+q][i]
        return ar
    def out(self, array):
        print("-"*(self.size*2)*self.size)
        for i in range(self.size):
            for j in range(self.size):
                for q in range(0,self.count, self.size):
                    print(*array[i*self.size+j][q:(q+self.size)], sep = ' ', end = '|')
                print()
            print("-"*(self.size*2)*self.size)

if __name__ == "__main__":
    a = sudoku(3)
    a.out(a.field)
    print("Solution of sudoku with difficult {}%".format(int((1 - a.difficult/(a.count**2)) * 100+1)))
    a.out(a.solution)