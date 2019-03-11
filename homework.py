# -*- coding: utf-8 -*-
'''
密码工程第二次作业
'''
import GF2nPY

if __name__ == "__main__":
    file = open("output.txt", "w", encoding="UTF8")
    file.seek(0)
    file.truncate()

    gf28 = GF2nPY.GF2nField(8, "100011011")
    progress = 4 * 256 * 256

    file.writelines("-----加法-----\n")
    for i in range(256):
        for j in range(256):
            file.writelines(bin(i)[2:] + "+" + bin(j)[2:] + "=" + gf28.add(bin(i)[2:], bin(j)[2:]) + "\n")
        p = (256 * i) / progress * 100
        print("%.2f%%" % p)

    file.writelines("-----减法-----\n")
    for i in range(256):
        for j in range(256):
            file.writelines(bin(i)[2:] + "-" + bin(j)[2:] + "=" + gf28.add(bin(i)[2:], bin(j)[2:]) + "\n")
        p = (256 * (256 + i)) / progress * 100
        print("%.2f%%" % p)

    file.writelines("-----乘法-----\n")
    for i in range(256):
        for j in range(256):
            file.writelines(bin(i)[2:] + "*" + bin(j)[2:] + "=" + gf28.multiply(bin(i)[2:], bin(j)[2:]) + "\n")
        p = (256 * (256 * 2 + i)) / progress * 100
        print("%.2f%%" % p)

    file.writelines("-----除法-----\n")
    for i in range(256):
        for j in range(256):
            try:
                result = gf28.divide(bin(i)[2:], bin(j)[2:])
            except ValueError:
                result = "-"
            file.writelines(bin(i)[2:] + "\\" + bin(j)[2:] + "=" + result + "\n")
        p = (256 * (256 * 3 + i)) / progress * 100
        print("%.2f%%" % p)

    file.close()
    print("Done!")
