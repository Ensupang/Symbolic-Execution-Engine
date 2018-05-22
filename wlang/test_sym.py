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

import unittest
import wlang.ast as ast
import wlang.sym

class TestSym (unittest.TestCase):
    def test_one (self):
        prg1 = "havoc x; assume x > 10; assert x > 15"
        ast1 = ast.parse_string (prg1)
        sym = wlang.sym.SymExec ()
        st = wlang.sym.SymState ()
        out = [s for s in sym.run (ast1, st)]
        self.assertEquals (len(out), 1)
    def test_1 (self):
        prg1 = "havoc y;x:=11 ; assume x > 10; assume x < 10; assert x > 10; assert x <= 10; assert x = 10"
        ast1 = ast.parse_string (prg1)
        sym = wlang.sym.SymExec ()
        st = wlang.sym.SymState ()
        out = [s for s in sym.run (ast1, st)]
        self.assertEquals (len(out), 1)
    def test_2 (self):
        prg1 = "x:= 8;if x > 0 then x := x * 2 else x := x + 1;print_state"
        ast1 = ast.parse_string(prg1)
        sym = wlang.sym.SymExec ()
        st = wlang.sym.SymState ()
        out = sym.run (ast1, st)
    def test_3 (self):
        prg1 = "y := 8; skip; print_state"
        ast1 = ast.parse_string (prg1)
        sym = wlang.sym.SymExec ()
        st = wlang.sym.SymState ()
        out = [s for s in sym.run (ast1, st)]
        self.assertEquals (len(out), 1)
    def test_4 (self):
        prg1 = "x := 1; y := 2; z := 3;if (y >= x) or (z <= x) then x := 5 else x := 15;print_state"
        ast1 = ast.parse_string(prg1)
        sym = wlang.sym.SymExec ()
        st = wlang.sym.SymState ()
        out = sym.run (ast1, st)
    def test_5 (self):
        prg1 = "x := 1; y := 2; z := 3;if (y <= x) or (z <= x) then x := 5 else z:= 10;print_state"
        ast1 = ast.parse_string(prg1)
        sym = wlang.sym.SymExec ()
        st = wlang.sym.SymState ()
        out = sym.run (ast1, st)
    def test_6 (self):
        prg1 = "a := 1;if not false then a := 5 else a := 15;print_state"
        ast1 = ast.parse_string(prg1)
        sym = wlang.sym.SymExec ()
        st = wlang.sym.SymState ()
        out = sym.run (ast1, st)
    def test_7 (self):
        prg1 = "x := 15;while x > 0 do x := x - 1;print_state"
        ast1 = ast.parse_string(prg1)
        sym = wlang.sym.SymExec ()
        st = wlang.sym.SymState ()
        out = sym.run (ast1, st)
    def test_8 (self):
        prg1 = "x:= 1;if x > 0 then x := x + 1 else x := x - 1;print_state"
        ast1 = ast.parse_string(prg1)
        sym = wlang.sym.SymExec ()
        st = wlang.sym.SymState ()
        out = sym.run (ast1, st)
    def test_9 (self):
        prg1 = "x:= 10;if x > 0 then x := x / 2 else x := x + 1;print_state"
        ast1 = ast.parse_string(prg1)
        sym = wlang.sym.SymExec ()
        st = wlang.sym.SymState ()
        out = sym.run (ast1, st)
    def test_10 (self):
        prg1 = "x:=0;if x >= 0 then i := 1 else i := 5;print_state"
        ast1 = ast.parse_string(prg1)
        sym = wlang.sym.SymExec ()
        st = wlang.sym.SymState ()
        out = sym.run (ast1, st)
    def test_11 (self):
        prg1 = "x:= -1;if x > 0 then x := x + 1 else x := x - 1;print_state"
        ast1 = ast.parse_string(prg1)
        sym = wlang.sym.SymExec ()
        st = wlang.sym.SymState ()
        out = sym.run (ast1, st)
    def test_12 (self):
        prg1 = "x:=-5; if x < 0 then i := 5 else i := 5;print_state"
        ast1 = ast.parse_string(prg1)
        sym = wlang.sym.SymExec ()
        st = wlang.sym.SymState ()
        out = sym.run (ast1, st)
    def test_13 (self):
        prg1 = "x:=0; if 0 <= 0 then i := 4 else i := 5;print_state"
        ast1 = ast.parse_string(prg1)
        sym = wlang.sym.SymExec ()
        st = wlang.sym.SymState ()
        out = sym.run (ast1, st)
    def test_14 (self):
        prg1 = "a := 1; b := 2; b := 3;if not (b <= a) then a := 5 else a := 15;print_state"
        ast1 = ast.parse_string(prg1)
        sym = wlang.sym.SymExec ()
        st = wlang.sym.SymState ()
        out = sym.run (ast1, st)
    def test_15 (self):
        prg1 = "havoc x,y,z;while y > 0 do y := y - 1;while z > 0 do z := z - 1;print_state"
        ast1 = ast.parse_string(prg1)
        sym = wlang.sym.SymExec ()
        st = wlang.sym.SymState ()
        out = sym.run (ast1, st)
    def test_16 (self):
        prg1 = "x:=0; if x=0 then i := 3 else i := 5;print_state"
        ast1 = ast.parse_string(prg1)
        sym = wlang.sym.SymExec ()
        st = wlang.sym.SymState ()
        out = sym.run (ast1, st)
    def test_17 (self):
        prg1 = "x:=5;if x > 0 then i := 2 else i := 5;print_state"
        ast1 = ast.parse_string(prg1)
        sym = wlang.sym.SymExec ()
        st = wlang.sym.SymState ()
        out = sym.run (ast1, st)
    def test_18 (self):
        prg1 = "x := 1; y := 2; z := 3;if (y >= x) and (z >= x) then x := 5 else x := 15;print_state"
        ast1 = ast.parse_string(prg1)
        sym = wlang.sym.SymExec ()
        st = wlang.sym.SymState ()
        out = sym.run (ast1, st)
    def test_19 (self):
        import sys
        sys.argv = ['file', 'wlang/test1.prg']
        run = wlang.sym.main()
    def test_20 (self):
        prg1 = "x := 1; y := 2; z := 3;if (true) or (false) then x := 5 else z:= 10;print_state"
        ast1 = ast.parse_string(prg1)
        sym = wlang.sym.SymExec ()
        st = wlang.sym.SymState ()
        out = sym.run (ast1, st)
    def test_21 (self):
        prg1 = "x := 1; y := 2; z := 3;if (false) or (false) then x := 5 else z:= 10;print_state"
        ast1 = ast.parse_string(prg1)
        sym = wlang.sym.SymExec ()
        st = wlang.sym.SymState ()
        out = sym.run (ast1, st)
    def test_22 (self):
        prg1 = "x:=1;y:=1;  if x == y then x:=x+1 ; print_state"
        ast1 = ast.parse_string(prg1)
        sym = wlang.sym.SymExec ()
        st = wlang.sym.SymState ()
        out = sym.run (ast1, st)
    def test_23 (self):
        prg1 = "x := 1; if (false) then x := 5 ;print_state"
        ast1 = ast.parse_string(prg1)
        sym = wlang.sym.SymExec ()
        st = wlang.sym.SymState ()
        out = sym.run (ast1, st)
    def test_24 (self):
        prg1 = "x := 1; assert x:=2"
        ast1 = ast.parse_string(prg1)
        sym = wlang.sym.SymExec ()
        st = wlang.sym.SymState ()
        out = sym.run (ast1, st)
    def test_25 (self):
        prg1 = "havoc x, y; assume y >= 0;c := 0;r := x;while c < y inv c <= y and r = x + c do {r := r + 1;c := c + 1};assert r = x + y"
        ast1 = ast.parse_string(prg1)
        sym = wlang.sym.SymExec ()
        st = wlang.sym.SymState ()
        out = sym.run (ast1, st)
    def test_26 (self):
        prg1 = "havoc x, y; assume y >= 0;c := 0;r := x;while c < y inv c < y do {r := r + 1;c := c + 1}"
        ast1 = ast.parse_string(prg1)
        sym = wlang.sym.SymExec ()
        st = wlang.sym.SymState ()
        out = sym.run (ast1, st)
