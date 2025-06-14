# app/services/simulation_service.py

import simpy
import numpy as np
import pandas as pd
import io
import base64
from concurrent.futures import ThreadPoolExecutor, as_completed
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def run_simulation_once(params: dict):
    """
    Corre una sola réplica de la simulación, devuelve la lista de dicts con los datos de cada paciente.
    """
    SIM_DURATION = 1440  # minutos en 24h
    WARM_UP = params.get('warm_up', 120)

    # Tasas de llegada variables
    PEAK_HOURS = [
        (18*60, 24*60, params['peak_lambda']),
        (0*60, 6*60,  params['night_lambda']),
        (6*60, 18*60, params['day_lambda'])
    ]
    TRIAGE_TIME = (params['triage_mean'], params['triage_std'])
    CONSULT_TIME = (params['consult_mean'], params['consult_std'])
    DIAG_TIME = {'xray': params['diag_xray'], 'lab': params['diag_lab']}
    TREAT_TIME = (params['treat_mean'], params['treat_std'])

    RES = {
        'day': {
            'doctors': params['doctors_day'],
            'nurses':  params['nurses_day'],
            'beds':    params['beds'],
            'xray':    params['xray'],
            'ultrasound': params['ultrasound']
        },
        'night': {
            'doctors': params['doctors_night'],
            'nurses':  params['nurses_night'],
            'beds':    params['beds'],
            'xray':    params['xray'],
            'ultrasound': params['ultrasound']
        }
    }
    PRIORITY_PROBS = [
        params['priority_critical'],
        params['priority_urgent'],
        params['priority_non_urgent']
    ]
    DIAG_PROB = params['diag_prob']
    ADMIT_PROB = params['admit_prob']

    # Helpers
    def get_arrival_rate(now):
        t = now % (24*60)
        for start, end, lam in PEAK_HOURS:
            if start <= t < end:
                return lam
        return PEAK_HOURS[-1][2]

    # Procesos SimPy
    def patient_process(env, pid, priority, resources, shift_sched):
        arrival = env.now
        data = {'patient_id': pid, 'priority': priority, 'arrival_time': arrival}

        # Triage
        with resources['triage'].request(priority=priority) as req:
            yield req
            d = max(0, np.random.normal(*TRIAGE_TIME))
            yield env.timeout(d)
            data['triage_wait'] = env.now - arrival
            data['triage_end'] = env.now

        # Consultation
        with resources['doctors'].request(priority=priority) as req:
            yield req
            yield shift_sched['active_doctors'].get(1)
            d = max(0, np.random.lognormal(np.log(CONSULT_TIME[0]), CONSULT_TIME[1]/CONSULT_TIME[0]))
            yield env.timeout(d)
            yield shift_sched['active_doctors'].put(1)
            data['consult_wait'] = env.now - data['triage_end']
            data['consult_end'] = env.now

        # Diagnostics
        if np.random.random() < DIAG_PROB:
            diag_type = 'xray' if np.random.random() < 0.6 else 'lab'
            with resources[diag_type].request(priority=priority) as req:
                yield req
                d = max(0, np.random.exponential(DIAG_TIME[diag_type]))
                yield env.timeout(d)
                data['diag_wait'] = env.now - data['consult_end']
                data['diag_end'] = env.now
        else:
            data['diag_wait'] = 0
            data['diag_end'] = data['consult_end']

        # Treatment
        with resources['beds'].request(priority=priority) as req_bed:
            yield req_bed
            with resources['nurses'].request(priority=priority) as req_nurse:
                yield req_nurse
                yield shift_sched['active_nurses'].get(1)
                d = max(0, np.random.lognormal(np.log(TREAT_TIME[0]), TREAT_TIME[1]/TREAT_TIME[0]))
                yield env.timeout(d)
                yield shift_sched['active_nurses'].put(1)
                data['treat_wait'] = env.now - data['diag_end']
                data['treat_end'] = env.now

        data['los'] = env.now - arrival
        data['admitted'] = np.random.random() < ADMIT_PROB
        data['completion_time'] = env.now

        return data

    def patient_generator(env, resources, shift_sched, results):
        pid = 0
        while env.now < SIM_DURATION:
            lam = get_arrival_rate(env.now)
            inter = np.random.exponential(60/lam)
            yield env.timeout(inter)
            pr = np.random.choice([0,1,2], p=PRIORITY_PROBS)
            res = yield env.process(patient_process(env, pid, pr, resources, shift_sched))
            results.append(res)
            pid += 1

    def manage_shifts(env, shift_sched):
        while True:
            t = env.now % (24*60)
            if 0 <= t < 6*60:
                d_target = max(1, RES['night']['doctors'])
                n_target = max(1, RES['night']['nurses'])
            else:
                d_target = max(1, RES['day']['doctors'])
                n_target = max(1, RES['day']['nurses'])

            # Ajusta contenedores
            curr_d = shift_sched['active_doctors'].level
            if curr_d < d_target:
                yield shift_sched['active_doctors'].put(d_target-curr_d)
            elif curr_d > d_target:
                yield shift_sched['active_doctors'].get(curr_d-d_target)

            curr_n = shift_sched['active_nurses'].level
            if curr_n < n_target:
                yield shift_sched['active_nurses'].put(n_target-curr_n)
            elif curr_n > n_target:
                yield shift_sched['active_nurses'].get(curr_n-n_target)

            yield env.timeout(60)

    # Prepara entorno
    env = simpy.Environment()
    resources = {
        'triage': simpy.PriorityResource(env, capacity=4),
        'doctors': simpy.PriorityResource(env, capacity=max(RES['day']['doctors'], RES['night']['doctors'])),
        'nurses':  simpy.PriorityResource(env, capacity=max(RES['day']['nurses'], RES['night']['nurses'])),
        'beds':    simpy.PriorityResource(env, capacity=RES['day']['beds']),
        'xray':    simpy.PriorityResource(env, capacity=RES['day']['xray']),
        'lab':     simpy.PriorityResource(env, capacity=1),
        'ultrasound': simpy.PriorityResource(env, capacity=RES['day']['ultrasound'])
    }
    shift_sched = {
        'active_doctors': simpy.Container(env, init=RES['day']['doctors'], capacity=max(RES['day']['doctors'], RES['night']['doctors'])),
        'active_nurses':  simpy.Container(env, init=RES['day']['nurses'],  capacity=max(RES['day']['nurses'], RES['night']['nurses']))
    }

    run_results = []
    # Inicia procesos
    env.process(manage_shifts(env, shift_sched))
    env.process(patient_generator(env, resources, shift_sched, run_results))
    env.run(until=SIM_DURATION)

    return run_results


def simulate(params: dict):
    """
    Ejecuta múltiples réplicas y devuelve:
      - records: lista de todos los pacientes
      - metrics: métricas agregadas
      - plot_b64: histograma de LOS en base64
    """
    num_runs = params['num_runs']
    all_results = []

    # Concurrencia
    with ThreadPoolExecutor() as ex:
        futures = [ex.submit(run_simulation_once, params) for _ in range(num_runs)]
        for f in as_completed(futures):
            all_results.extend(f.result())

    df = pd.DataFrame(all_results)
    df = df[df['arrival_time'] >= params.get('warm_up', 120)]

    metrics = {
        'avg_wait_triage': df['triage_wait'].mean(),
        'avg_wait_consult': df['consult_wait'].mean(),
        'avg_wait_diag': df['diag_wait'].mean(),
        'avg_wait_treat': df['treat_wait'].mean(),
        'avg_los': df['los'].mean(),
        'throughput': len(df) / num_runs,
        'admission_rate': df['admitted'].mean()
    }

    # Genera histograma
    plt.figure(figsize=(8,5))
    for pr,label in [(0,'critical'),(1,'urgent'),(2,'non-urgent')]:
        subset = df[df['priority']==pr]
        plt.hist(subset['los'], bins=30, alpha=0.6, label=label, density=True)
    plt.title('LOS por prioridad')
    plt.xlabel('Minutos'); plt.ylabel('Densidad'); plt.legend()

    buf = io.BytesIO()
    plt.savefig(buf, format='png', dpi=100)
    buf.seek(0)
    plot_b64 = base64.b64encode(buf.read()).decode('ascii')
    plt.close()

    return df.to_dict(orient='records'), metrics, plot_b64
