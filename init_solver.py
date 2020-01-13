from solution import Solution
import re


class InitSolver:

    def __init__(self):
        pass

    def run(self, problem):
        """
        @type problem: Problem
        :rtype: Solution
        """
        raise Exception("Need to implement 'run' method")


#
# Goes from left to right, from top to bottom
# Cut slice whenever max conditions are met (<=H pieces in a slice)
#
class InitSolverSilly(InitSolver):

    def run(self, problem):
        """
        @type problem: Problem
        :rtype: Solution
        """
        sol = Solution(problem)     # type: Solution
        formats = problem.slices_formats()
        row, col = 0, 0
        while True:
            for f in formats:
                if sol.is_free_space(row, col, f[0], f[1]) and problem.is_valid_slice(row, col, f[0], f[1]):
                    sol.create_new_slice(row, col, f[0], f[1])
                    col += f[1]
                    break
            else:
                col += 1
            if col >= problem.max_width:
                row += 1
                col = 0
            if row >= problem.max_height:
                break
            # print(row, col)
        return sol
