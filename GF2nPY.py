'''
支持GF2域下运算的python包
'''


class Polynomial:
    _bin = ""

    def __init__(self, string):
        self._bin = string

    def set_value(self, string):
        self._bin = string

    def get_value_bin(self):
        return self._bin

    def get_value_int(self):
        return int(self._bin, 2)

    def get_polynome(self, **arg):
        '''
        f(255) = x^0 + x^1 + x^2 + x^3 + x^4 + x^5 + x^6 + x^7
        '''
        out = ""
        if "with_fx" in arg and arg["with_fx"] == 1:
            out += "f(x) ="
        elif "with_fx" in arg and arg["with_fx"] == 2:
            out += "f" + "(" + str(int(self._bin, 2)) + ") ="
        for i in range(len(self._bin)):
            if self._bin[i] == "1":
                out += " x^" + str(i)
                if i < len(self._bin) - 1:
                    out += " +"
        return out


class Test:
    def __init__(self):
        self._value1 = 255
        self._value2 = 123

    def test_Polynomial(self):
        result = "\nStart test class Polynomial\n"
        p1 = Polynomial(bin(self._value1)[2:])
        result += "Test get_value_bin() OK.\n" if p1.get_value_bin() == bin(self._value1)[2:] else "Test get_value_bin() ERROR.\n"
        result += "Test get_polynome() OK.\n" if p1.get_polynome(with_fx=2) == "f(255) = x^0 + x^1 + x^2 + x^3 + x^4 + x^5 + x^6 + x^7" else "Test get_polynome() ERROR.\n"
        return result

    def test_Bin(self):
        result = "\nStart test class Bin\n"
        p1 = Polynomial(bin(self._value1)[2:])
        p2 = Polynomial(bin(self._value2)[2:])
        result += "Test bin_add() OK.\n" if Bin.bin_add(p1.get_value_bin(), p2.get_value_bin()) == "10000100" else "Test bin_add() ERROR.\n"
        result += "Test bin_multiply() OK.\n" if Bin.bin_multiply(p1.get_value_bin(), p2.get_value_bin()) == "10100100101001" else "Test bin_multiply() ERROR.\n"
        result += "Test bin_divide() OK.\n" if Bin.bin_divide(p1.get_value_bin(), p2.get_value_bin()) == ["1", "1001"] else "Test bin_divide() ERROR.\n"
        result += "Test bin_mod() OK.\n" if Bin.bin_mod(p1.get_value_bin(), p2.get_value_bin()) == "1001" else "Test bin_mod() ERROR.\n"
        result += "Test bin_gcd() OK.\n" if Bin.bin_gcd(p1.get_value_bin(), p2.get_value_bin()) == "11" else "Test bin_gcd() ERROR.\n"
        result += "Test bin_gcd() OK.\n" if Bin.bin_divide(p1.get_value_bin(), "100011011") == ["0", "11111111"] else "Test bin_gcd() ERROR.\n"
        return result


class Bin:
    @staticmethod
    def _preproc(_bin1, _bin2):
        return [_bin2, _bin1] if len(_bin1) > len(_bin2) else [_bin1, _bin2]

    @staticmethod
    def bin_add(_bin1, _bin2):
        result = ""
        [_bin1, _bin2] = Bin._preproc(_bin1, _bin2)
        while len(_bin1) != len(_bin2):
            _bin1 = "0" + _bin1
        for i in range(len(_bin1)):
            result += str(int(_bin1[i]) ^ int(_bin2[i]))
        while result[0] == "0" and result != "0":  #去除开头的0
            result = result[1:]
        return result

    @staticmethod
    def bin_multiply(_bin1, _bin2):
        result = "0"
        [_bin1, _bin2] = Bin._preproc(_bin1, _bin2)
        for shift in range(len(_bin1)):
            if _bin1[len(_bin1) - shift - 1] == "1":
                result = Bin.bin_add(result, bin(int(_bin2, 2) << int(shift))[2:])
        return result

    @staticmethod
    def bin_divide(dividend, divisor):
        quotient, remainder = "", ""
        resultLength = len(dividend) - len(divisor) + 1
        while len(dividend) >= len(divisor) and dividend != "0":
            # TODO: 解决商的bug
            #for i in range(len(dividend) - len(divisor))

            preDL = len(dividend)
            dividend = Bin.bin_add(dividend, bin(int(divisor, 2) << (len(dividend) - len(divisor)))[2:])
            if (preDL - len(dividend)) <= resultLength:
                quotient = Bin.bin_add(quotient, bin(int("1", 2) << (preDL - len(dividend)))[2:])
            else:
                quotient = Bin.bin_add(quotient, bin(int("1", 2) << resultLength - 1)[2:])
            #quotient += "1"

        remainder = dividend
        if quotient == "":
            quotient = "0"
        return [quotient, remainder]

    @staticmethod
    def bin_mod(dividend, divisor):
        return Bin.bin_divide(dividend, divisor)[1]

    @staticmethod
    def bin_gcd(_bin1, _bin2):
        [_bin2, _bin1] = Bin._preproc(_bin1, _bin2)
        if Bin.bin_mod(_bin1, _bin2) != "0":
            return Bin.bin_gcd(_bin2, Bin.bin_mod(_bin1, _bin2))
        else:
            return _bin2

    @staticmethod
    def bin_extend_euclid(_bin1, _bin2):
        flag = 0
        if len(_bin1) < len(_bin2):
            [_bin2, _bin1] = [_bin1, _bin2]
            flag = 1
        a, b = ["", ""], ["", ""]

        if _bin2 != Bin.bin_gcd(_bin1, _bin2):
            [quotient, remainder] = Bin.bin_divide(_bin1, _bin2)
            _bin1, _bin2 = _bin2, remainder
            a = ["1", quotient]

            if _bin2 != Bin.bin_gcd(_bin1, _bin2):
                [quotient, remainder] = Bin.bin_divide(_bin1, _bin2)
                _bin1, _bin2 = _bin2, remainder
                b = [quotient, Bin.bin_add(Bin.bin_multiply(a[1], quotient), "1")]
            else:
                b = a
        else:
            b = a

        while _bin2 != Bin.bin_gcd(_bin1, _bin2):
            [quotient, remainder] = Bin.bin_divide(_bin1, _bin2)
            _bin1, _bin2 = _bin2, remainder
            tmp = a
            a = b
            b[0] = Bin.bin_add(tmp[0], Bin.bin_multiply(a[0], quotient))
            b[1] = Bin.bin_add(tmp[1], Bin.bin_multiply(a[1], quotient))

        return b if flag == 0 else [b[1], b[0]]


class GF2nField:
    pass


if __name__ == "__main__":
    t = Test()
    print(t.test_Polynomial())
    print(t.test_Bin())
    print(Bin.bin_divide("11011", "11"))
