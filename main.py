import streamlit as st
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
from scipy.integrate import odeint

st.title('''Modello di Lokta-Volterra''')
pagina = st.sidebar.radio('Menù', ['HOME', 'SIMULAZIONE'], index=0)


if pagina == 'HOME':
    st.write(''' 
    In matematica le equazioni di Lotka-Volterra, note anche come equazioni o modello preda-predatore, sono un sistema di equazioni differenziali non lineari
    del primo ordine che forniscono un modello matematico in grado di descrivere la dinamica di un ecosistema in cui interagiscono soltanto
    due specie animali: una delle due come predatore, l'altra come la sua preda. Questa modellizzazione matematica è stata proposta indipendentemente
    da Alfred J. Lotka nel 1925 e Vito Volterra nel 1926.
    ''')

    st.write('''Le equazioni hanno la forma:''')

    r'$${\displaystyle \displaystyle {\begin{cases}{\dfrac {\mathrm {d} x}{\mathrm {d} t}}=(A-By)x,\\{\dfrac {\mathrm {d} y}{\mathrm {d} t}}=(Cx-D)y,\end{cases}}}{\displaystyle \displaystyle {\begin{cases}{\dfrac {\mathrm {d} x}{\mathrm {d} t}}=(A-By)x,\\{\dfrac {\mathrm {d} y}{\mathrm {d} t}}=(Cx-D)y,\end{cases}}}$$'

    st.write('''dove le derivate:  **dx/dt** e **dy/dt** sono i tassi di crescita nel tempo delle popolazioni di prede e predatori, mentre i numeri 
    **A**, **B**, **C** e **D** sono parametri positivi che descrivono l'interazione tra le due specie. Lo studio del sistema dinamico definito da tale sistema di equazioni differenziali consente di individuare tutti i tipi di evoluzione che è possibile avere a partire da una qualsiasi situazione iniziale.
    ''')

    st.write('''
        \n
        ## **Simulazione** \n
        Inserisci i parametri: \n
    ''')
    alpha = st.slider('A', max_value=2.0, min_value=0.0, value=1.1)
    beta = st.slider('B', max_value=2.0, min_value=0.0, value=0.4)
    delta = st.slider('C', max_value=2.0, min_value=0.0, value=0.1)
    gamma = st.slider('D', max_value=2.0, min_value=0.0, value=0.4)


    y0 = [10, 1]  # [fish, bears] units in hundreds

    t = np.linspace(0, 50, num=1000)

    # steady state initial conditions
    # y0 = [gamma/delta , alpha/beta] # [fish, bears] units in hundreds

    params = [alpha, beta, delta, gamma]

    # funzione che definisce il  sistema che descrive il modello
    def sim(variables, t, params):

        # fish population level
        x = variables[0]

        # bear population level
        y = variables[1]

        alpha = params[0]
        beta = params[1]
        delta = params[2]
        gamma = params[3]

        dxdt = alpha * x - beta * x * y
        dydt = delta * x * y - gamma * y

        return([dxdt, dydt])

    # animazione

    # calcoli
    y = odeint(sim, y0, t, args=(params,))

    # grafici
    f, (ax1, ax2) = plt.subplots(2)

    line1, = ax1.plot(t, y[:, 0], color="b")
    line2, = ax2.plot(t, y[:, 1], color="r")

    ax1.set_ylabel("Fish (hundreds)")
    ax2.set_ylabel("Bears (hundreds)")
    ax2.set_xlabel("Time")

    st.set_option('deprecation.showPyplotGlobalUse', False)
    st.pyplot()
if pagina =='SIMULAZIONE':
    st.write('''
    simulazione reale con epidemia nel sistema o qualcosa del genere    
    ''')
