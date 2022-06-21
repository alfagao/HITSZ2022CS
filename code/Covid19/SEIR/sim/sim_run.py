import time
from SEIR.sim.seir_sim import SeirSim
from SEIR.sim.model_series import SI, SIR, SEIR, mSEIR

if __name__ == '__main__':
    N0 = 1e3
    days = [70, 120, 200, 200]
    In0 = 7
    beta1 = 0.127
    beta2 = 0.145
    beta = 0.272
    alpha = 0.0715
    gama = 0.0910
    root_path = "imgs/" + time.strftime('%Y_%m_%d_%H_%M_%S_', time.localtime(time.time()))
    # SI Model Sim Run
    # si = SeirSim(model=SI, Y0=[N0 - In0, In0], days=days[0], args=(beta,))
    # si.plot(styles=[{"line": "--", "label": "Susceptible"},
    #                 {"line": "-.", "label": "Infected"},
    #                 ],
    #         title=f"SI Model Simulate(beta={beta})",
    #         savePath=root_path + f"SI_{beta}.png"
    #         )
    # SIR Model Sim Run
    # sir = SeirSim(model=SIR, Y0=[N0 - In0, In0, 0], days=days[1], args=([beta, gama],))
    # sir.plot(styles=[{"line": "--", "label": "Susceptible"},
    #                  {"line": "-.", "label": "Infected"},
    #                  {"line": "-", "label": "Recovered"},
    #                  ],
    #          title=f"SIR Model Simulate(beta={beta}, gama={gama})",
    #          savePath=root_path + f"SIR_{beta}_{gama}.png"
    #          )
    # SEIR Model Sim Run
    # seir = SeirSim(model=SEIR, Y0=[N0 - In0, 0, In0, 0], days=days[2], args=([beta, alpha, gama],))
    # seir.plot(styles=[{"line": "--", "label": "Susceptible"},
    #                   {"line": ":", "label": "Exposed"},
    #                   {"line": "-.", "label": "Infected"},
    #                   {"line": "-", "label": "Recovered"},
    #                   ],
    #           title=f"SEIR Model Simulate(beta={beta}, alpha={alpha}, gama={gama})",
    #           savePath=root_path + f"SEIR_{beta}_{alpha}_{gama}.png"
    #           )
    # modified SEIR Model Sim Run
    mSeir = SeirSim(model=mSEIR, Y0=[N0 - In0, 0, In0, 0], days=days[3], args=([beta1, beta2, alpha, gama],))
    mSeir.plot(styles=[{"line": "--", "label": "Susceptible"},
                       {"line": ":", "label": "Exposed"},
                       {"line": "-.", "label": "Infected"},
                       {"line": "-", "label": "Recovered"},
                       ],
               title=f"Modified SEIR Model Simulate(args={beta1}, {beta2}, {alpha}, {gama})",
               savePath=root_path + f"mSEIR_{beta1}_{beta2}_{alpha}_{gama}.png"
               )
