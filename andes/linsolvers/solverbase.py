from andes.linsolvers.cupy import CuPySolver
from andes.linsolvers.scipy import SpSolve
from andes.linsolvers.suitesparse import UMFPACKSolver, KLUSolver
from numpy import angle, conj, exp, r_, Inf
from numpy.linalg import norm
from scipy.sparse.linalg import splu
from scipy import linalg
from qiskit import QuantumCircuit
from qiskit.algorithms.linear_solvers.hhl import HHL
from qiskit import quantum_info

class Solver:
    """
    Sparse matrix solver class.

    This class wraps UMFPACK, KLU, SciPy and CuPy solvers to provide an unified
    interface for solving sparse linear equations ``Ax = b``.

    Provides methods ``solve``, ``linsolve`` and ``clear``.
    """

    def __init__(self, sparselib='umfpack'):

        # solvers
        self.umfpack = UMFPACKSolver()
        self.klu = KLUSolver()
        self.spsolve = SpSolve()
        self.cupy = CuPySolver()

        # KLU as failsafe
        if sparselib not in self.__dict__:
            self.sparselib = 'klu'
        else:
            self.sparselib = sparselib

        self.worker = self.__dict__[self.sparselib]

    def solve(self, A, b):
        """
        Solve linear equations and cache factorizations if possible.

        Parameters
        ----------
        A : kvxopt.spmatrix
            Sparse N-by-N matrix
        b : kvxopt.matrix or numpy.ndarray
            Dense N-by-1 matrix

        Returns
        -------
        numpy.ndarray
            Dense N-by-1 array
        """
        return self.worker.solve(A, b)

    def linsolve(self, A, b):
        """
        Solve linear equations without caching facorization. Performs full factorization each call.

        Parameters
        ----------
        A : kvxopt.spmatrix
            Sparse N-by-N matrix
        b : kvxopt.matrix or numpy.ndarray
            Dense N-by-1 matrix

        Returns
        -------
        numpy.ndarray
            Dense N-by-1 array
        """
        return self.worker.linsolve(A, b)
    
    def quantum_solve(self, A, b):
        """
        Solve linear equations using the HHL algorithm
        ------
        This requires the A matrix to be Hermitian.
        """
        isHermitian = scipy.linalg.ishermitian(A)
        if isHermitian is False:
            A = A.getH()
        
        num_qubits = int(np.log2(A.shape[0]))
        b_norm = b / np.linalg.norm(b)
        qc = QuantumCircuit(num_qubits)
        qc.isometry(b_norm, list(range(num_qubits)), None)
        hhl = HHL()
        solution = hhl.solve(A, b_norm)
        total_qubits = solution.state.num_qubits
        approx_result = quantum_info.Statevector(solution.state).data[2 ** (total_qubits - 1) : 2 ** (total_qubits - 1) + 2 ** num_qubits]
        mismatch = abs(approx_result)*np.lingalg.norm(b) # Multiple the approximate result by the norm
        return mismatch

    def clear(self):
        """
        Remove all cached objects.
        """
        self.worker.clear()
        
     
