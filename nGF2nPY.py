# -*- coding: utf-8 -*-
'''
New GF2nPY, store polynomial's deg num.
eg. f(x)=x^256+x^224+x^128 => [256,224,128]

In this new class, we provide some new algorithm 
which optimize the efficency.
'''

class Polynomial:
    '''
    A new data struct can support large data polynomial store.
    '''
    def __init__(self, polynomial=[]):
        self.polynomial = self._pre_proc(polynomial)

    def set(self, ploynomial):
        self.polynomial = self._pre_proc(ploynomial)

    def get(self):
        return self.polynomial

    @staticmethod
    def _pre_proc(polynomial):
        '''
        预处理多项式，检查并按照从大到小的顺序进行排列
        '''
        try:
            for item in polynomial:
                if not (isinstance(item, int)):
                    raise TypeError("Ploynomial list's item should be integer. ")
        except:
            raise TypeError("Ploynomial should be in list form. ")
        return sorted(polynomial, reverse=True)

    def set_by_bin(self, poly_bin, split=0):
        '''
        使用二进制形式来更新多项式
        '''
        self.polynomial = self._pre_proc(self.get_ploy_simpli(poly_bin, split))

    def deg(self):
        '''获取多项式的阶'''
        return self.polynomial[0]

    def make_ploy_bin(self, split=0):
        '''
        将简化形式的多项式表达为二进制形式
        '''
        result = []
        for i in range(self.deg() + 1):
            result.append(0)
        for i in self.polynomial:
            result[len(result) - i - 1] = 1
        if split != 0:
            while len(result) % split != 0:
                result = [0] + result
            poly = result
            result = []
            for i in range(int(len(poly) / split)):
                result.append(poly[i * 32 + 0:(i + 1) * 32])
        return result

    @staticmethod
    def get_ploy_simpli(poly_bin, split=0):
        '''
        将二进制形式的多项式表达为简化形式
        split 为有分割模式
        '''
        if split != 0:
            poly = []
            for i in poly_bin:
                poly += i
            poly_bin = poly
        result = []
        m = 0
        for i in poly_bin:
            m += 1
            if i == 1:
                result.append(len(poly_bin) - m)
        return result

class PloynomialComputation:
    '''
    A New Way to do GF2 mod computation
    Can support large data computation
    '''
    @staticmethod
    def add(p1, p2):
        result = []
        for i in p1:
            if i not in p2:
                result.append(i)
        for i in p2:
            if i not in p1:
                result.append(i)
        return Polynomial._pre_proc(result)

    @staticmethod
    def shift(p, n):
        '''
        将 p 左移 n 位，n 为负则是右移
        '''
        result = []
        for i in p:
            if i + n >= 0:
                result.append(i + n)
        return Polynomial._pre_proc(result)

    @staticmethod
    # 常规求模运算，p1 mod p2
    def reg_mod(p1, p2):
        while p1[0] >= p2[0]:
            p1 = PloynomialComputation.add(p1, PloynomialComputation.shift(p2, p1[0] - p2[0]))
            return PloynomialComputation.reg_mod(p1, p2)
        return p1

class PMRP:
    '''
    Polynomial modular reduction for pentanomials
    PMRP算法是基于处理器位数优化的，想要使用pre_proc()方法，将
    指数存储的多项式变为二进制形式，再进行运算。
    '''
    @staticmethod
    def pre_proc(W_x, W=32):
        '''
        输入W_x需要按照从高位到地位的排列顺序存储，将使用指数存
        储的多项式变为二进制形式，二进制又按位数分成k[0]个部分，
        每部分位数W个字节。返回值两个列表，分别是每一位与第一位
        相差的块数k[i]，和该位在块中的位置kr[i]
        '''
        k = [int(W_x[0] / W)]
        kr = [W_x[0] % W]
        for i in W_x[1:]:
            k.append(int((W_x[0] - i) / W))
            kr.append((W_x[0] - i) % W)
        return [k, kr]

    @staticmethod
    def bin_shift(poly_bin, shift):
        '''
        [0,1,0,1,0,1,1,1]<<4=[0,1,1,1,0,1,0,1]
        '''
        if abs(shift) < len(poly_bin):
            result = poly_bin[shift:]
            result += poly_bin[:shift]
        else:
            raise ValueError("Shift must below the ploy length")
        return result

    @staticmethod
    def add(p1, p2):
        result = []
        for i in range(len(p1)):
            result.append(p1[i] ^ p2[i])
        return result

    @staticmethod
    def PMRP(D_x, W_x, W=32):
        d = Polynomial(D_x)
        w = Polynomial(W_x)
        [k, kr] = PMRP.pre_proc(w.get())

        i = int(d.deg() / W)
        while d.deg() >= w.deg():
            tmp = d.make_ploy_bin(32)[::-1]
            ttmmpp = [0] * 32
            ttmmpp[31 - d.deg() % W] = 1
            if (d.deg() % W < kr[1]):
                tmp[i - k[1] - 1] = PMRP.add(tmp[i - k[1] - 1], PMRP.bin_shift(ttmmpp, -kr[1]))
            else:
                tmp[i - k[1]] = PMRP.add(tmp[i - k[1]], PMRP.bin_shift(ttmmpp, -kr[1]))
            if (d.deg() % W < kr[2]):
                tmp[i - k[2] - 1] = PMRP.add(tmp[i - k[2] - 1], PMRP.bin_shift(ttmmpp, -kr[2]))
            else:
                tmp[i - k[2]] = PMRP.add(tmp[i - k[2]], PMRP.bin_shift(ttmmpp, -kr[2]))
            if (d.deg() % W < kr[3]):
                tmp[i - k[3] - 1] = PMRP.add(tmp[i - k[3] - 1], PMRP.bin_shift(ttmmpp, -kr[3]))
            else:
                tmp[i - k[3]] = PMRP.add(tmp[i - k[3]], PMRP.bin_shift(ttmmpp, -kr[3]))
            if (d.deg() % W < kr[0]):
                tmp[i - k[0] - 1] = PMRP.add(tmp[i - k[0] - 1], PMRP.bin_shift(ttmmpp, -kr[0]))
            else:
                tmp[i - k[0]] = PMRP.add(tmp[i - k[0]], PMRP.bin_shift(ttmmpp, -kr[0]))
            d.set_by_bin(tmp[::-1], 1)
            d.set(d.get()[1:])
            i = int(d.deg() / W)
        return d
