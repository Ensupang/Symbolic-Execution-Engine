# Symbolic-Execution-Engine
Automatically explore program paths

• Execute program on “symbolic” input values

• “Fork” execution at each branch

• Record branching conditions

• Analysis of programs by tracking symbolic rather than actual values

The implementation of the symbolic execution engine is located in directory wlang. Execute the engine
using the following command:

(venv) $ python -m wlang.sym wlang/test1.prg
