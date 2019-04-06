# -*- coding: utf-8 -*-
'''
A New Way to do GF2 mod computation
Can support large data computation
'''
import NewPolynomial as NP
import time


class PloynomialComputation:
    @staticmethod
    def add(p1, p2):
        result = []
        for i in p1:
            if i not in p2:
                result.append(i)
        for i in p2:
            if i not in p1:
                result.append(i)
        return NP.NewPolynomial._pre_proc(result)

    @staticmethod
    def shift(p, n):
        '''
        将 p 左移 n 位，n 为负则是右移
        '''
        result = []
        for i in p:
            if i + n >= 0:
                result.append(i + n)
        return NP.NewPolynomial._pre_proc(result)

    @staticmethod
    # 常规求模运算，p1 mod p2
    def reg_mod(p1, p2):
        while p1[0] >= p2[0]:
            p1 = PloynomialComputation.add(p1, PloynomialComputation.shift(p2, p1[0] - p2[0]))
            return PloynomialComputation.reg_mod(p1, p2)
        return p1


if __name__ == "__main__":
    start = time.clock()
    a = NP.NewPolynomial([789, 720, 567, 520, 433, 120, 98, 67, 19, 10, 1, 0])
    b = NP.NewPolynomial([163, 7, 6, 3, 0])
    print(PloynomialComputation.reg_mod(a.get(), b.get()))
    end = time.clock()
    print(end - start)
