# -*- coding: utf-8 -*-
import GF2nPY


class Test:
    def __init__(self):
        self._value1 = 255
        self._value2 = 123

    def test_Polynomial(self):
        result = "\nStart test class Polynomial\n"
        p1 = GF2nPY.Polynomial(bin(self._value1)[2:])
        result += "Test get_value_bin() OK.\n" if p1.get_value_bin() == bin(self._value1)[2:] else "Test get_value_bin() ERROR.\n"
        result += "Test get_polynome() OK.\n" if p1.get_polynome(with_fx=2) == "f(255) = x^0 + x^1 + x^2 + x^3 + x^4 + x^5 + x^6 + x^7" else "Test get_polynome() ERROR.\n"
        return result

    def test_Bin(self):
        result = "\nStart test class Bin\n"
        p1 = GF2nPY.Polynomial(bin(self._value1)[2:])
        p2 = GF2nPY.Polynomial(bin(self._value2)[2:])
        result += "Test bin_add() OK.\n" if GF2nPY.Bin.bin_add(p1.get_value_bin(), p2.get_value_bin()) == "10000100" else "Test bin_add() ERROR.\n"
        result += "Test bin_multiply() OK.\n" if GF2nPY.Bin.bin_multiply(p1.get_value_bin(), p2.get_value_bin()) == "10100100101001" else "Test bin_multiply() ERROR.\n"
        result += "Test bin_divide() OK.\n" if GF2nPY.Bin.bin_divide(p1.get_value_bin(), p2.get_value_bin()) == ["1", "1001"] else "Test bin_divide() ERROR.\n"
        result += "Test bin_mod() OK.\n" if GF2nPY.Bin.bin_mod(p1.get_value_bin(), p2.get_value_bin()) == "1001" else "Test bin_mod() ERROR.\n"
        result += "Test bin_gcd() OK.\n" if GF2nPY.Bin.bin_gcd(p1.get_value_bin(), p2.get_value_bin()) == "11" else "Test bin_gcd() ERROR.\n"
        result += "Test bin_extend_euclid() OK.\n" if GF2nPY.Bin.bin_extend_euclid("100011011", "10000011") == ['1000111', '10000000'] else "Test bin_extend_euclid() ERROR.\n"
        return result


if __name__ == "__main__":
    t = Test()
    print(t.test_Polynomial())
    print(t.test_Bin())