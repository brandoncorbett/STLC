import matplotlib.pyplot as plt

from stlc import grm


def main():
    cm = 1e-2
    minute = 60
    zl = 10.0 * cm  #[cm]
    rp = 0.004 * cm  #[cm]
    ec = 0.50
    ep = 0.4
    kf = 0.01 * cm  #[cm]
    Dax = 0.000002 * cm**2 / minute  #[cm^2 min^-1]
    Dp = 3.003 * 1e-5 * cm**2 / minute  #[cm^2 min^-1]
    Ds = 0.  #[cm^2 min^-1]
    u = 3. * cm / minute  #[cm min^-1]
    ka = 2.5  #[s^-1]
    kd = 1  #[s^-1]
    tinj = 20 * minute  #[min]
    cinj = 0.5  #[mol /m^-3]
    tmax = 100 * minute  #[min]
    qm = 5.
    nr = 10
    nz = 25
    dt = 1

    def step(t: float, tinj: float) -> float:
        return float(t <= tinj)

    parameters0 = grm.ModelParameters(c0=cinj,
                                          Dax=Dax,
                                          Dp=Dp,
                                          Ds=Ds,
                                          ka=ka,
                                          kd=kd,
                                          kf=kf,
                                          qm=qm,
                                          ip=lambda t: step(t, tinj))

    parameters1 = grm.ModelParameters(c0=cinj,
                                          Dax=Dax,
                                          Dp=Dp,
                                          Ds=Ds,
                                          ka=1,
                                          kd=kd,
                                          kf=kf,
                                          qm=qm,
                                          ip=lambda t: step(t, tinj))

    model = grm.GeneralRateModel(
        u=u,
        ep=ep,
        ec=ec,
        zl=zl,
        rp=rp,
        nz=nz,
        nr=nr,
        component_parameters=[parameters0, parameters1])
    model.init_solution(tmax, dt)
    grm.solve(model, tmax, dt)
    model.sol.build_results()

    plt.plot(model.sol.t / minute,
             model.sol.c[0, -1, :],
             'r-',
             linewidth=0.2,
             label='STLC')

    plt.plot(model.sol.t / minute,
             model.sol.c[1, -1, :],
             'b-',
             linewidth=0.2,
             label='STLC')
    plt.legend()
    plt.grid()
    plt.savefig("grm_multi_component.pdf")


if __name__ == '__main__':
    main()
