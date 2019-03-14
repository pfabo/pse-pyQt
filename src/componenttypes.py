# Typy komponentov editora
TYPE_DECORATION = 0         # nesimulovanu komponent
TYPE_SCHEMATICS = 16        # graficky komponent schemy
TYPE_SPICE = 32             # generator pre spice - simulator

TYPE_SIMULATOR = 100        # komponenty simulacie - maska

TYPE_CONNECTION = 101       # komponent prepojenia medzi sietami (bod)
TYPE_CONN_VIRTUAL = 102     # neviditelny komponent prepojenia medzi sietami
TYPE_NET_TERM = 103         # komponent prepojenia medzi sietami
TYPE_BLOCK_TERM = 104       # interny komponent prepojenia v ramci bloku, zmena typu pri parsovani bloku

TYPE_SIM_CONTINUOUS = 1000  # linearne komponenty
TYPE_SIM_DISCRETE = 1001    # diskretne nespojite komponenty
TYPE_SIM_CLOCK = 1002       # casovace a hodiny
TYPE_SIM_CONTROL = 1003     # algoritmy riadenia
TYPE_SIM_INTEGRAL = 1004    # komponenty s charakteristikou popisanou diff rovnicou
TYPE_SIM_AGREGAT = 1005     # zlozeny komponent, obsahuje virtualne komponenty
TYPE_SIM_BLOCK = 1006       # blok, odkazuje sa na diagram v samostatnom subore

# Stavy simulatora v metode Component.sim
SIM_INIT = 1                # inicializacia komponentu (otvorenie kom. portov, suborov, vytvorenie poli ..)
SIM_STEP = 4                # priebezny vypocet pocas kroku simulacie
SIM_FINISH = 16             # ukoncenie simulacie (zatvorenie suborov, portov ...)
SIM_DERIVE = 32             # prva derivacia vstupnej hodnoty komponentu
SIM_UPDATE = 64             # nastavenie hodnoty komponentu na konci simulacneho kroku
SIM_RESET = 128             # reset komponentov pocas prebiehajucej / ukoncenej simulacie
