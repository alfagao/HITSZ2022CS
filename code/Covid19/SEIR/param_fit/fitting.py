"""
使用 深圳的数据 对 m-SEIR 中的参数(beta1, beta2)进行 拟合
取alpha = 1/7, gamma = 1/14
"""
import time
from SEIR.param_fit.fitclass import SeirSelfFit
from SEIR.param_fit.modelclass import RMSELoss, MAELoss, SEIR

fit_log = open("logs/"+time.strftime('%m%d_%H%M%S', time.localtime(time.time()))+".log", 'w', encoding="utf-8")

def prdt_mseir(seir):
    actual_data = seir.load_actual_data()
    print("In model m-SEIR", file=fit_log)
    weights = [0., 0., 0.8, 0.2]
    beta1, beta2 = seir.train(weights, log=fit_log)
    print(f"beta1={beta1}, beta2={beta2}", file=fit_log)
    print("weights= ", weights, file=fit_log)
    prdT, prdS, prdE, prdI, prdR = seir.predict([beta1, beta2], 0)
    # 真实数据 I, R
    seir.plot(
        path="img/mseir_" + time.strftime('%m%d_%H%M%S', time.localtime(time.time())) + ".png",
        # title=f"mSEIR Model fitting on SZ-CovData(b1={round(beta1, 2)}, b2={round(beta2, 2)})",
        title=f"mSEIR Model fitting on SZ-CovData(b1=0.00159, b2=0.00197)",
        choice=[2, 3, 6, 7],
        t=prdT,
        y=[actual_data[0], actual_data[1], actual_data[2], actual_data[3], prdS, prdE, prdI, prdR],
        styles=["-", "--", "-^", "-.", "--", "--", "-", "-"],
        labels=["S_actual", "E_actual", "I_actual", "R_actual", "prd of S", "prd of E", "prd of I", "prd of R"]
    )
    return RMSELoss(actual_data, [prdS, prdE, prdI, prdR], weights), \
           MAELoss(actual_data, [prdS, prdE, prdI, prdR], weights)

def prdt_seir(seir):
    actual_data = seir.load_actual_data()
    print("In model SEIR", file=fit_log)
    weights = [0., 0., 0.49, 0.51]
    arg = seir.train(weights, log=fit_log)
    print(f"beta={arg[0]}", file=fit_log)
    print("weights= ", weights, file=fit_log)
    prdT, prdS, prdE, prdI, prdR = seir.predict(arg, 0)
    # 真实数据 I, R
    seir.plot(
        path="img/seir_" + time.strftime('%m%d_%H%M%S', time.localtime(time.time())) + ".png",
        title=f"SEIR Model fitting on SZ-CovData(beta={arg[0]})",
        choice=[2, 3, 6, 7],
        t=prdT,
        y=[actual_data[0], actual_data[1], actual_data[2], actual_data[3], prdS, prdE, prdI, prdR],
        styles=["-", "--", "-^", "-.", "--", "--", "-", "-"],
        labels=["S_actual", "E_actual", "I_actual", "R_actual", "prd of S", "prd of E", "prd of I", "prd of R"]
    )
    return RMSELoss(actual_data, [prdS, prdE, prdI, prdR], weights), \
           MAELoss(actual_data, [prdS, prdE, prdI, prdR], weights)


def main():
    N0 = 430
    I0 = 4
    mseir = SeirSelfFit(
        Y0=[N0-I0, 0, I0, 0],
        args=[0.12, 0.04],
        path="../../data/sz_sa.csv",
        N0=N0
    )
    print(prdt_mseir(mseir), file=fit_log)

    # seir = SeirSelfFit(
    #     Y0=[N0 - I0, 0, I0, 0],
    #     args=0.3,
    #     path="../../data/sz_sa.csv",
    #     N0=N0,
    #     model=SEIR
    # )
    # print(prdt_seir(seir), file=fit_log)

    fit_log.close()

if __name__ == '__main__':
    main()

"""
beta1=0.24974118114331306, beta2=-0.126141058570981
weights=  [0.0, 0.0, 0.8, 0.2]
(34.334343114199925, 27.573588408434535)
"""