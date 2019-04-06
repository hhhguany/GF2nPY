'''
Polynomial modular reduction for pentanomials
'''
import NewPolynomial as NP

D_x = [789, 720, 567, 520, 433, 120, 98, 67, 19, 10, 1, 0]
W_x = [163, 7, 6, 3, 0]
W = 32


class PMRP:
    @staticmethod
    def pre_proc(W_x, W=32):
        k = [int(W_x[0] / W)]
        kr = [W_x[0] % W]
        for i in W_x:
            if i != W_x[0]:
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
        d = NP.NewPolynomial(D_x)
        w = NP.NewPolynomial(W_x)
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

if __name__ == "__main__":
    print(PMRP.PMRP(D_x, W_x, W).get())
