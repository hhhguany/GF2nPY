'''
A new data struct can support large data polynomial store
'''


class NewPolynomial:
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
