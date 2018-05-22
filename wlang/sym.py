# The MIT License (MIT)
# Copyright (c) 2016 Arie Gurfinkel

# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:

# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
from __future__ import print_function
from wlang.undef_visitor import UndefVisitor
import wlang.ast
import cStringIO
import sys
# import thread
import z3
class SymState(object):
    def __init__(self, solver = None):
        # environment mapping variables to symbolic constants
        self.env = dict()
        # path condition
        self.path = list ()
        self._solver = solver
        if self._solver is None:
            self._solver = z3.Solver ()
        # true if this is an error state
        self._is_error = False
    def add_pc (self, *exp):
        """Add constraints to the path condition"""
        self.path.extend (exp)
        self._solver.append (exp)
    def is_error (self):
        return self._is_error
    def mk_error (self):
        self._is_error = True
    def is_empty (self):
        """Check whether the current symbolic state has any concrete states"""
        res = self._solver.check ()
        return res == z3.unsat
    def fork(self):
        """Fork the current state into two identical states that can evolve separately"""
        child = SymState ()
        child.env = dict(self.env)
        child.add_pc (*self.path)
        return (self, child)
    def __str__ (self):
        buf = cStringIO.StringIO ()
        for k, v in self.env.iteritems():
            buf.write (str (k))
            buf.write (": ")
            buf.write (str (v))
            buf.write ("\n")
        buf.write ("pc: ")
        buf.write (str (self.path))
        buf.write ("\n")
        return buf.getvalue ()
class SymExec (wlang.ast.AstVisitor):
    While_Output=list()
    def __init__(self):
        self.St_=list ()
        self.count=0
    def run (self, ast, state):
        k=self.visit (ast, state=state)
        tlist_=list()
        if isinstance(k, list):
            tlist_=k
            output_list=[]
            while (True):
                if tlist_==[]:
                    break
                for index,i in enumerate(tlist_):
                    if type(i)== list:
                        tlist_=i+tlist_[index+1:]
                        break
                    else:
                        output_list.append(i)
                        tlist_.pop(index)
                        break
            for mem in output_list:
                self.St_.append(mem)
        else:
            self.St_.append(k)
        return self.St_
    def havoc (self, node):
        dVisitor = UndefVisitor ()
        dVisitor.check (node)
        return dVisitor.get_defs ()
    def visit_IntVar (self, node, *args, **kwargs):
        return kwargs["state"].env [node.name]
    def visit_BoolConst(self, node, *args, **kwargs):
        # print ("[sym]In visit_BoolConst")
        return z3.BoolVal (node.val)
    def visit_IntConst (self, node, *args, **kwargs):
        # print ("[sym]In visit_IntConst",node.val)
        return z3.IntVal (node.val)
    def visit_RelExp (self, node, *args, **kwargs):
        # print ("[sym]In visit_RelExp",node)
        lhs = self.visit (node.arg (0), *args, **kwargs)
        rhs = self.visit (node.arg (1), *args, **kwargs)
        # print ("-------------------------------In visit_RelExp------------------------------------",lhs)
        if node.op == "<=": return lhs <= rhs
        if node.op == "<": return lhs < rhs
        if node.op == "=": return lhs == rhs
        if node.op == ">=": return lhs >= rhs
        if node.op == ">": return lhs > rhs
        assert False
    def visit_BExp (self, node, *args, **kwargs):
        # print ("[sym]In visit_BExp")
        kids = [self.visit (a, *args, **kwargs) for a in node.args]
        if node.op == "not":
            assert node.is_unary ()
            assert len (kids) == 1
            return z3.Not (kids[0])
        fn = None
        base = None
        if node.op == "and":
            fn = lambda x, y : z3.And (x, y)
            base = z3.BoolVal (True)
        elif node.op == "or":
            fn = lambda x, y : z3.Or (x, y)
            base = z3.BoolVal (False)
        assert fn is not None
        return reduce (fn, kids, base)
    def visit_AExp (self, node, *args, **kwargs):
        # print ("[sym]In visit_AExp")
        kids = [self.visit (a, *args, **kwargs) for a in node.args]
        fn = None
        base = None
        if node.op == "+":
            fn = lambda x, y: x + y
        elif node.op == "-":
            fn = lambda x, y: x - y
        elif node.op == "*":
            fn = lambda x, y: x * y
        elif node.op == "/":
            fn = lambda x, y : x / y
        assert fn is not None
        return reduce (fn, kids)

    def visit_SkipStmt (self, node, *args, **kwargs):
        return kwargs["state"]
    def visit_PrintStateStmt (self, node, *args, **kwargs):
        # print (kwargs["state"])
        return kwargs["state"]
    def visit_AsgnStmt (self, node, *args, **kwargs):
        val = self.visit (node.rhs, *args, **kwargs)
        st = kwargs["state"]
        name = node.lhs.name
        sym_val = z3.FreshInt (name)
        st.env [name] = sym_val
        st.add_pc (sym_val == val)
        return st
    def visit_IfStmt (self, node, *args, **kwargs):
        cond=self.visit(node.cond,*args,**kwargs)
        Return_LIst=list()
        THEN,ELSE=kwargs["state"].fork()
        THEN.add_pc(cond)
        if not THEN.is_empty():
            kwargs["state"]=self.visit (node.then_stmt, *args, **kwargs)
            Return_LIst.append(kwargs["state"])
        ELSE.add_pc(z3.Not(cond))
        if node.has_else ():
            if not ELSE.is_empty():
                kwargs["state"] = ELSE
                Return_LIst.append(self.visit (node.else_stmt, *args, **kwargs))
        else:
            Return_LIst.append(ELSE)
        kwargs["state"]=Return_LIst
        return kwargs["state"]
    def visit_WhileStmt (self, node, *args, **kwargs):
        # print ("In visit_WhileStmt------------------------------------------",self.While_Output)
        #no invariant branch
        if node.inv is None:
            cond = self.visit (node.cond, *args, **kwargs)
            IN, NOIN=kwargs["state"].fork()
            IN.add_pc(cond)
            NOIN.add_pc(z3.Not(cond))
            # print ("What's in IN?",IN,cond)
            if not IN.is_empty() and self.count<=10:
                self.count=self.count+1
                st= self.visit (node.body, *args, **kwargs)
                kwargs["state"] =st
                stt=self.visit (node, *args, **kwargs)
                # self.While_Output.append(kwargs["state"])
            elif self.count>10:
                self.While_Output=[]
                return self.While_Output
            if not NOIN.is_empty():
                # self.While_Output=[]
                self.While_Output.append(NOIN)
            return self.While_Output
        else:
            inv=self.visit(node.inv,*args,**kwargs)
            first_check,check_over=kwargs["state"].fork()
            first_check.add_pc(inv)
            # 1 assert inv;
            if first_check.is_empty():
                print("invariant cannot be hold on entry")
                return first_check
            else:
                # 2 havoc V;
                for var in self.havoc (node.body):
                    check_over.env[var.name]=z3.FreshInt(var.name)
                kwargs["state"]=check_over
                # 3 assume inv;
                inv=self.visit(node.inv,*args,**kwargs)
                check_over.add_pc(inv)
                cond=self.visit(node.cond,*args,**kwargs)
                # 4 if b then { s ; assert inv; assume false }
                IN,NOIN=check_over.fork()
                IN.add_pc(cond)
                NOIN.add_pc(z3.Not(cond))
                if not IN.is_empty ():
                    st=self.visit (node.body,*args,**kwargs)
                    kwargs["state"] =st
                    check_inv=self.visit(node.inv,*args,**kwargs)
                    st.add_pc(z3.Not(check_inv))
                    if not st.is_empty ():
                        print("invariant cannot be hold at the end of the loop")
                if not NOIN.is_empty ():
                    return NOIN
    def visit_AssertStmt (self, node, *args, **kwargs):
        cond = self.visit (node.cond, *args, **kwargs)
        true_,false_= kwargs["state"].fork ()
        true_.add_pc(cond)
        false_.add_pc(z3.Not(cond))
        if not false_.is_empty ():
            print("Assertion error")
            print("Assertion:",cond)
            print("State: Error")
            false_.mk_error()
        if not kwargs["state"].is_empty():
            return kwargs['state']

    def visit_AssumeStmt (self, node, *args, **kwargs):
        # print ("In visit_AssumeStmt")
        st = kwargs["state"]
        cond_val = self.visit (node.cond, *args, **kwargs)
        st.add_pc (cond_val)
        if not st.is_empty ():
            return st
    def visit_HavocStmt (self, node, *args, **kwargs):
        # print ("[sym]In visit_HavocStmt")
        st = kwargs["state"]
        for v in node.vars:
            st.env[v.name] = z3.FreshInt (v.name)
        return st
    def visit_StmtList (self, node, *args, **kwargs):
        # print ("---------[sym]In visit_StmtList",kwargs["state"])
        # tlist_=list()
        Result=list()
        st=kwargs["state"]
        nkwargs=dict (kwargs)
        for stmt in node.stmts:
            # print ("==========",st,stmt)
            tlist_=list()
            if isinstance(st, list):
                tlist_=st
                # print ("am i in?",tlist_)
                output_list=[]
                Result=[]
                while (True):
                    if tlist_==[]:
                        break
                    for index,i in enumerate(tlist_):
                        if type(i)== list:
                            tlist_=i+tlist_[index+1:]
                            break
                        else:
                            output_list.append(i)
                            tlist_.pop(index)
                            break
                for mem in output_list:
                    nkwargs ["state"] = mem
                    Result.append(self.visit (stmt, *args, **nkwargs))
                st=Result
            else:
                nkwargs ["state"] = st
                st = self.visit (stmt, *args, **nkwargs)
        return st
def _parse_args ():
    import argparse
    ap = argparse.ArgumentParser (prog="sym",
                                  description="WLang Interpreter")
    ap.add_argument ("in_file", metavar="FILE", help="WLang program to interpret")
    ap.add_argument ("--bound", metavar="BOUND", help="Global loop bound", \
                     type=int, default=10)
    args = ap.parse_args ()
    return args
def main ():
    args = _parse_args ()
    # print ("In main args=",args)
    ast = wlang.ast.parse_file (args.in_file)
    # print("In main ast=",ast)
    st = SymState ()#pc, st is the SymState type
    # print ("In main st=",st)
    sym = SymExec ()
    # print ("In main sym=",sym)
    states = sym.run (ast, st)
    if states is None:
        print ("[symexec]: no output states")
    else:
        count = 0
        for out in states:
            if out is None:
                print ("[symexec]: no output states")
                return 0
            else:
                count = count + 1
                print ("[symexec]: symbolic state reached")
                print (out)
        print ("[symexec]: found", count, "symbolic states")
    return 0
if __name__ == "__main__":
    sys.exit (main ())
