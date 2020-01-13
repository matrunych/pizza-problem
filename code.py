from init_solver import InitSolverSilly

import time
class Optimization:
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
        return ""

    def initial_solution(self):
        # TODO: If you want you may change an initial solution generation
        init_solver = InitSolverSilly()
        solution = init_solver.run(self.problem)
        return solution

    def search(self, solution, time_limit=float('inf')):

        import numpy as np
        R, C, L, H = [self.problem.max_width, self.problem.max_height, self.problem.L, self.problem.H]
        pizza = np.array(np.full((C, R), 0))
        for i in range(len(self.problem.field)):
            for j in range(len(self.problem.field[i])):
                if (self.problem.field[i][j] == 'T'):
                    pizza[i, j] = 1
                else:
                    pizza[i, j] = 0


        def copyc():
            R, C, L, H = [self.problem.max_width, self.problem.max_height, self.problem.L, self.problem.H]
            pizza = np.array(np.full((C, R), 0))
            for i in range(len(self.problem.field)):
                for j in range(len(self.problem.field[i])):
                    if (self.problem.field[i][j] == 'T'):
                        pizza[i, j] = 1
                    else:
                        pizza[i, j] = 0
            return R, C, L, H, pizza


        copyc()

        from random import randint


        def satisfy_constraints(location, shape, slice_mask, pizza, L, H):
            r, c = location
            dr, dc = shape
            if slice_mask[r:r + dr, c:c + dc].size == dr * dc:
                if np.all(slice_mask[r:r + dr, c:c + dc] == 0):
                    if dr * dc <= H:
                        tomatoes = np.sum(pizza[r:r + dr, c:c + dc])
                        mushrooms = dr * dc - tomatoes
                        if tomatoes >= L and mushrooms >= L:
                            return True
            return False

        def cut_slice(location, shape, current_slices, slice_mask):
            r, c = location
            dr, dc = shape
            slice_mask[r:r + dr, c:c + dc] = 1
            current_slices.append((r, c, dr, dc))

        def score(pizza_slices):
            s = 0
            for pizza_slice in pizza_slices:
                s += pizza_slice[2] * pizza_slice[3]
            return s


        import sympy
        from random import shuffle

        def generate_all_shapes(L, H):
            possible_shapes = []
            for size in range(2 * L, H + 1):
                factors = sympy.factorint(size)
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
            """Selects a random location that is still in empty_cells."""
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

        def greedy5(iters=3000000):
            possible_shapes = generate_all_shapes(L, H)
            slice_mask = np.zeros_like(pizza)
            pizza_slices = []
            empty_cells = set(tuple(args) for args in np.transpose(np.nonzero(1 - slice_mask)).tolist())
            random_locations = list(x for x in empty_cells)
            shuffle(random_locations)
            current_score = 0
            for _ in range(iters):
                location = get_random_available_location_set2(random_locations, empty_cells)
                if location is None:
                    break
                selected_shapes = []
                for shape in possible_shapes:
                    if satisfy_constraints(location, shape, slice_mask, pizza, L, H):
                        selected_shapes.append(shape)
                if len(selected_shapes) > 0:
                    current_score = score(pizza_slices)
                    shape = max(selected_shapes, key=lambda shp: current_score + shp[0] * shp[1])
                    cut_slice(location, shape, pizza_slices, slice_mask)
                    update_empty_cells(location, shape, empty_cells)
            # print('\n')
            # print(f"score: {score(pizza_slices)}")
            return pizza_slices
        best = 0
        am = 1000
        optimized_solution = Optimization()
        if R < 100 and C < 100:
            am = 100
        if R < 20 and C < 20:
            am = 10000
        if R > 100 and C > 100:
            am = 10
        for i in range(am):
            pizza_slices1 = greedy5()
            if score(pizza_slices1) > score(solution.get_all_slices()):
                if best < score(pizza_slices1):
                    best = score(pizza_slices1)
                print(score(pizza_slices1), score(solution.get_all_slices()))
                solution.slice_list = pizza_slices1

        if (best > solution.score()):
            optimized_solution.score1 = best
        else:
            optimized_solution.score1 = solution.score()
        # TODO: implement your search procedure. Do not forget about time limit!
        return optimized_solution

    def get_search_trace(self):
        return self.trace