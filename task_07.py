
from init_solver import InitSolverSilly
import time
from random import shuffle
from random import choice
import math

class Optimized:
    score1 = 0
    def score(self):
        return self.score1

class Solver:

    problem = None
    trace = None

    def __init__(self, problem):
        self.problem = problem

    def description(self):
        """
        :return: String with the description of the approach
        """
        # TODO: Place your algorithm's description here
        return "Let`s assume that we have got an existing solution and it`s not the best. To improve solution we wanna find some place on our matrix,\n where there are empty cells,"\
        "try to remove them and fill them again, trying to do it, as good, as possible.\n To do this, we need to generate all possible shapes that will satisfy our constrains.\n"\
        "After successful attempt, we can increase our score. We will do this algorithm until time limit isn`t exceeded."

    def initial_solution(self):
        """
        Finds an initial solution for the problem
        :return: Solution object
        """
        # TODO: If you want you may change an initial solution generation
        init_solver = InitSolverSilly()
        solution = init_solver.run(self.problem)
        return solution

    def search(self, solution, time_limit=float('inf')):
        def getData():
            C, R, L, H = [self.problem.max_width, self.problem.max_height, self.problem.L, self.problem.H]
            pizza = self.problem.field
            p = []
            for i in range(R):
                g = []
                for j in range(C):
                    if pizza[i][j] == 'T':
                        g.append(1)
                    else:
                        g.append(0)
                p .append(g)
            return R, C, L, H, p

        def cut_slice(location, shape, current_slices, slice_mask):
            r, c = location
            dr, dc = shape
            for i in range(r, r + dr):
                for j in range(c, c + dc):
                    slice_mask[i][j] = 1
            #     slice_mask[r:r + dr, c:c + dc] = 1
            current_slices.append((r, c, dr, dc))

        def generate_all_shapes(L, H):
            possible_shapes = []
            for size in range(2 * L, H + 1):
                factors = {}
                while size % 2 == 0:
                    if 2 in factors:
                        factors[2] += 1
                    else:
                        factors[2] = 1
                    size = size / 2

                for i in range(3, int(math.sqrt(size)) + 1, 2):

                    while size % i == 0:
                        if i in factors:
                            factors[int(i)] += 1
                        else:
                            factors[int(i)] = 1
                        size = size / i

                if size > 2:
                    if size in factors:
                        factors[int(size)] += 1
                    else:
                        factors[int(size)] = 1
                if len(factors) == 1:
                    prime = list(factors.keys())[0]
                    max_exp = list(factors.values())[0]
                    for exp in range(0, max_exp + 1):
                        factor1 = prime ** exp
                        factor2 = prime ** (max_exp - exp)
                        possible_shapes.append((factor1, factor2))
                elif len(factors) == 2:
                    prime1, prime2 = list(factors.keys())
                    max_exp1, max_exp2 = list(factors.values())
                    for exp1 in range(0, max_exp1 + 1):
                        for exp2 in range(0, max_exp2 + 1):
                            factor1 = prime1 ** (max_exp1 - exp1) * prime2 ** (max_exp2 - exp2)
                            factor2 = prime1 ** (exp1) * prime2 ** (exp2)
                            possible_shapes.append((factor1, factor2))
                else:
                    raise NotImplementedError
            return possible_shapes

        def get_random_available_location_set2(random_locations, empty_cells):
            while len(random_locations) > 0:
                candidate = random_locations.pop()
                if candidate in empty_cells:
                    return candidate
            else:
                return None

        def update_empty_cells(location, shape, empty_cells):
            r, c = location
            dr, dc = shape
            for rr in range(r, r + dr):
                for cc in range(c, c + dc):
                    empty_cells.discard((rr, cc))

        def getScore(pizza_slices):
            s = 0
            for pizza_slice in pizza_slices:
                s += pizza_slice[2] * pizza_slice[3]
            return s

        def checkConstrains(location, shape, slice_mask, pizza, L, H, R, C):
            r, c = location
            dr, dc = shape
            start = True
            if R - r < dr or C - c < dc:
                start = False
            if start:
                ok = True
                for i in range(r, r + dr):
                    for j in range(c, c + dc):
                        if slice_mask[i][j] == 1:
                            ok = False
                            break
                if ok:
                    if dr * dc <= H:
                        tomatoes = 0
                        for i in range(r, r + dr):
                            for j in range(c, c + dc):
                                tomatoes += pizza[i][j]
                        mushrooms = dr * dc - tomatoes
                        if tomatoes >= L and mushrooms >= L:
                            return True
            return False

        def optimize(iters=10000, disable_progress_bar=False):
            R, C, L, H, pizza = getData()
            possible_shapes = generate_all_shapes(L, H)
            slice_mask = [[0] * C] * R
            pizza_slices = []
            empty_cells = set()
            for i in range(R):
                for j in range(C):
                    empty_cells.add((i, j))
            random_locations = list(x for x in empty_cells)
            shuffle(random_locations)
            current_score = 0
            for _ in range(iters):
                location = get_random_available_location_set2(random_locations, empty_cells)
                if location is None:
                    break
                selected_shapes = []
                for shape in possible_shapes:
                    if checkConstrains(location, shape, slice_mask, pizza, L, H, R, C):
                        selected_shapes.append(shape)
                if len(selected_shapes) > 0:
                    current_score = getScore(pizza_slices)
                    shape = max(selected_shapes, key=lambda shp: current_score + shp[0] * shp[1])
                    cut_slice(location, shape, pizza_slices, slice_mask)
                    update_empty_cells(location, shape, empty_cells)
            return getScore(pizza_slices), pizza_slices
        best = 0
        optimized = Optimized()
        start_time = time.time()
        while True:
            if time.time() - start_time >= time_limit:
                break
            l1, l2 = optimize()
            if l1 > best:
                best = l1
                optimized.score1 = best

        if optimized.score1 > solution.score():
            return optimized
        return solution


    def get_search_trace(self):
        return self.trace


