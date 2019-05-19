import nGF2nPY
import time
class Test:
    @staticmethod
    def efficent_test(func,*args,round=100,**kagrs):
        tmp=0
        
        if "ex_func" in kagrs:
            print(func(*args).get())
        else:
            print(func(*args))
        for i in range(round):
            start = time.process_time()
            func(*args)
            end = time.process_time()
            tmp+=end - start
        print("After "+str(round)+" rounds, the "+str(func)+" average excute time is: "+str(tmp/round))
            


def compare_PMRP_and_reg_mod():
    D_x = [789, 720, 567, 520, 433, 120, 98, 67, 19, 10, 1, 0]
    W_x = [163, 7, 6, 3, 0]
    W = 32

    a = nGF2nPY.Polynomial(D_x).get()
    b = nGF2nPY.Polynomial(W_x).get()

    Test.efficent_test(nGF2nPY.PloynomialComputation.reg_mod,a,b)
    Test.efficent_test(nGF2nPY.PMRP.PMRP,D_x, W_x, W,ex_func=1)

if __name__ == "__main__":
    compare_PMRP_and_reg_mod()