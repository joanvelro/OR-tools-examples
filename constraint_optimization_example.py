from ortools.sat.python import cp_model

from ortools.sat.python import cp_model


class VarArraySolutionPrinter(cp_model.CpSolverSolutionCallback):
    """Print intermediate solutions."""

    def __init__(self, variables):
        cp_model.CpSolverSolutionCallback.__init__(self)
        self.__variables = variables
        self.__solution_count = 0

    def on_solution_callback(self):
        self.__solution_count += 1
        for v in self.__variables:
            print('%s=%i' % (v, self.Value(v)), end=' ')
        print()

    def solution_count(self):
        return self.__solution_count


def SearchForAllSolutionsSampleSat():
    """Showcases calling the solver to search for all solutions."""
    # Creates the model.
    model = cp_model.CpModel()

    # Creates the variables.
    num_vals = 3
    x = model.NewIntVar(0, num_vals - 1, 'x')
    y = model.NewIntVar(0, num_vals - 1, 'y')
    z = model.NewIntVar(0, num_vals - 1, 'z')

    # Create the constraints.
    model.Add(x != y)
    model.Add(x + y == z-1)
    model.Add(z + y >= x + 1)

    # Create a solver and solve.
    solver = cp_model.CpSolver()
    solution_printer = VarArraySolutionPrinter([x, y, z])
    # Enumerate all solutions.
    solver.parameters.enumerate_all_solutions = True
    # Solve.
    status = solver.Solve(model, solution_printer)

    """
    The CP-SAT solver returns one of the status values shown in the table below. In this example, the value returned is OPTIMAL.
    Status 	        Description
    OPTIMAL         An optimal feasible solution was found.
    FEASIBLE 	    A feasible solution was found, but we don't know if it's optimal.
    INFEASIBLE 	    The problem was proven infeasible.
    MODEL_INVALID 	The given CpModelProto didn't pass the validation step. You can get a detailed error by calling ValidateCpModel(model_proto).
    UNKNOWN 	    The status of the model is unknown because no solution was found (or the problem was not proven INFEASIBLE) 
                    before something caused the solver to stop, such as a time limit, a memory limit, or a custom limit set by the user.
    """

    print('Status = %s' % solver.StatusName(status))

    if status == cp_model.FEASIBLE or status == cp_model.OPTIMAL:
        print('Number of solutions found: %i' % solution_printer.solution_count())
        # print('x = %i' % solver.Value(x))
        # print('y = %i' % solver.Value(y))
        # print('z = %i' % solver.Value(z))


SearchForAllSolutionsSampleSat()
