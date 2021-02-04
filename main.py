import streamlit as st
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
import matplotlib as mpl
from scipy.integrate import odeint

# setto stile dei grafici
mpl.style.use('seaborn')

# titolo della pagina e menù laterale
st.markdown("<h1 style='text-align: center; color: #b30000;'>Modello di Lokta-Volterra</h1>",
            unsafe_allow_html=True)

st.sidebar.title('Menù\n')
pagina = st.sidebar.radio(
    '', ['HOME', 'CASO DI STUDIO: lupi e conigli', 'CODICE'], index=0)


if pagina == 'HOME':  # pagina home
    # testo iniziale di spiegazione del modello preso da: https://it.wikipedia.org/wiki/Equazioni_di_Lotka-Volterra
    st.write(''' 
    In matematica le equazioni di Lotka-Volterra, note anche come equazioni o modello preda predatore, sono un sistema di equazioni differenziali non lineari
    del primo ordine che forniscono un modello matematico in grado di descrivere la dinamica di un ecosistema in cui interagiscono soltanto
    due specie animali: una delle due come predatore, l'altra come la sua preda. Questa modellizzazione matematica è stata proposta indipendentemente
    da Alfred J. Lotka nel 1925 e Vito Volterra nel 1926.Le equazioni hanno la forma:
    ''')

    st.latex(r'{\displaystyle \displaystyle {\begin{cases}{\dfrac {\mathrm {d} x}{\mathrm {d} t}}=(A-By)x,\\{\dfrac {\mathrm {d} y}{\mathrm {d} t}}=(Cx-D)y,\end{cases}}}')

    st.write('''\n
    dove le derivate:  **dx/dt** e **dy/dt** sono i tassi di crescita nel tempo delle popolazioni di prede e predatori, mentre i numeri 
    **A**, **B**, **C** e **D** sono parametri positivi che descrivono l'interazione tra le due specie. Lo studio del sistema dinamico definito da tale sistema di equazioni differenziali consente di individuare tutti i tipi di evoluzione che è possibile avere a partire da una qualsiasi situazione iniziale.
    ''')

    # creo slider nella barra laterale per ogni parametro
    st.sidebar.title('Simulazione\n')
    st.sidebar.write('**1.Impostazioni grafici**')
    grafico_pop = st.sidebar.radio('Grafico popolazioni', [
                                   'Unico', 'Doppio'], index=0)
    grafico_orbite = st.sidebar.checkbox('Grafico orbite',)

    st.sidebar.write('**2.Impostazioni parametri**')
    pesci = st.sidebar.number_input('N° iniziale di pesci', step=1, value=10)
    orsi = st.sidebar.number_input('N° iniziale di orsi', step=1, value=3)

    # tasso di crescita pesci
    alpha = st.sidebar.slider(
        'A: tasso di crescita dei pesci (x)', max_value=2.0, min_value=0.0, value=1.1)
    # tasso di mortalita pesci
    beta = st.sidebar.slider(
        'B: tasso di mortalità dei pesci (x)', max_value=2.0, min_value=0.0, value=0.4)
    # tasso di mortalità orsi se no pesci
    delta = st.sidebar.slider(
        'C: fattore pesci (x) necessari per nuovo orso (y)', max_value=1.0, min_value=0.0, value=0.05)
    # fattore n pesci per nuovo orso
    gamma = st.sidebar.slider(
        'D: tasso di mortalità degli orsi(y)', max_value=2.0, min_value=0.0, value=0.1)

    # simulazione: spiegazione dei parametri
    st.write('''
        \n
        # **Simulazione** \n
        ### 1. Applicazione del modello\n
        Consideriamo un sistema (isolato) popolato da due popolazioni: quella dei pesci (prede) e quella degli orsi (predatori).
        La simulazione di seguito proposta basandosi sul modello di Lokta-Volterra mostra graficamente l'andamento in funzione del tempo delle due popolazioni (pesci e orsi)
        che abitano il sistema preso in considerazione. Possiamo quindi ipotizzare che il comportamento di prede e predatori è il seguente:\n
        - I pesci crescono secondo il loro tasso di crescita
        - Gli orsi crescono secondo il loro tasso di crescita
        - Gli orsi mangiano i pesci (se ci sono)\n
        Inoltre:
        - I pesci diminuiscono se gli orsi aumentano (vengono mangiati)
        - I pesci aumentano se gli orsi diminuiscono (sopravvivono di più)
        - Gli orsi aumentano se i pesci aumentano (hanno più cibo)
        - Gli orsi diminuiscono se i pesci diminuiscono (non possono mangiare)\n

        ### 2.Regolazione dei parametri\n
        Detti:\n
        - x = numero di pesci\n
        - y = numero di orsi \n
        
        Il significato dei parametri è il seguente:\n
        - A: tasso di crescita dei pesci (x) quando non ci sono orsi (y)
        - B: tasso di mortalità dei pesci (x) dovuto agli orsi (y)
        - C: fattore che descrive quanti pesci (x) sono necessari per la nascita di un nuovo orso (y)
        - D: tasso di mortalità degli orsi(y) quando non ci sono i pesci (x) 
        

        Nella barra laterale è possibile regolare i parametri e impostare le condizoni iniziali ossia il numero iniziale di orsi e di pesci che popolano il sistema al tempo $$t_0$$
        \n
        ### 3.Situazioni particolari\n
        - Condizione di equilibrio
        - Simulazione di epidemia

    ''')

    # CALCOLI PER SIMULAZIONE

    # definisco situazione iniziale
    y0 = [pesci, orsi]  # [fish, bears] units in hundreds

    t = np.linspace(0, 50, num=1000)  # tempo

    # steady state initial conditions EQUILIBRIO
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

    # calcoli
    y = odeint(sim, y0, t, args=(params,))

    # grafici
    if grafico_pop == 'Doppio':
        f, (ax1, ax2) = plt.subplots(2)

        line1, = ax1.plot(t, y[:, 0], color="b")
        line2, = ax2.plot(t, y[:, 1], color="r")

        ax1.set_ylabel("Pesci *100")
        ax2.set_ylabel("Orsi *100")
        ax2.set_xlabel("Tempo")

        f.suptitle('Andamento della popolazione\n', size=18)

        st.set_option('deprecation.showPyplotGlobalUse', False)
        st.pyplot()
    elif grafico_pop == 'Unico':

        plt.plot(t, y[:, 0], color="b", label='Pesci')
        plt.plot(t, y[:, 1], color="r", label='Orsi')

        plt.title('\nAndamento della popolazione\n', size=18)
        plt.ylabel("Pesci & Orsi *100")
        plt.xlabel("Tempo")
        plt.legend()

        st.set_option('deprecation.showPyplotGlobalUse', False)
        st.pyplot()

    if grafico_orbite == True:
        plt.plot(y[:, 1], y[:, 0], color="black")

        plt.title('\nGrafico delle traiettorie\n', size=18,)
        plt.ylabel("Orsi *100")
        plt.xlabel("Pesci *100")

        st.set_option('deprecation.showPyplotGlobalUse', False)
        st.pyplot()


if pagina == 'CODICE':
    st.write('''
    ## Codice sorgente:\n
    E' possibile scaricare e modificare il codice sorgente dalla seguente GitHub repo (file: main.py):\n  https://github.com/tommaso-dognini/modello_LotkaVolterra.git \n

    \n
    ## Altri link utili:\n
    - Video che ho seguito per per scrivere il programma: https://www.youtube.com/watch?v=Zg9k9ijiYPA \n
    - Link alla pagina di Streamlit framework utilizzato per creazione webapp: https://www.streamlit.io/ \n
    - Link alla pagina Wikipedia: https://it.wikipedia.org/wiki/Equazioni_di_Lotka-Volterra \n
    ''')

if pagina == 'CASO DI STUDIO: lupi e conigli':
    st.write('''
    ### Caso di studio: lupi e conigli
    Si consiglia di visionare la seguente simulazione:\n
    http://www.shodor.org/interactivate/activities/RabbitsAndWolves/\n

    \n Si tratta di una simulazione preda-predatore secondo il Modello Lokta-Volterra **implementato su una situazione reale**.\n 
    La simulazione infatti introduce altri raparametri
    che permettono di simulare la realtà con maggiore precisione; il modello Lokta-Volterra infatti analizza una situazione ideale di un sistema isolato con solo due popolazioni 
    senza considerare per esempio possibili epidemie o la variabilità della disponibilità di cibo.\n
    ''')
