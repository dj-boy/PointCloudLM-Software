import serial
import matplotlib.pyplot as plt
import numpy as np
import time

def open_port():
    ser = serial.Serial('COM27', 115200)

    return ser

def close_port(port):
    port.close()

def detect_data(port):
    #port.reset_input_buffer()
    flag = True

    while flag:
        anuncio = port.read(1)
        anuncio = ord(anuncio[0]) # convertir en entero

        if (anuncio & 0xf0)  == 0xf0: # Se detecta el byte de anuncio de trama
                n_canales = anuncio & 0x0f # Numero de canales a leer
                return  n_canales

def main():
    port = open_port()
    i = 0.00
    y = 0.00
    Amplitud_matrix = np.array([])
    Time_matrix = np.array([])
    T_Inicio = time.time()
    T_Final = time.time()
    Dif = T_Final-T_Inicio
    while(Dif < 10):  # Contar 10 segundos
        n_canales = detect_data(port)
        data_in = port.read(2*n_canales)
        canal_n1 = (2**7)*ord(data_in[0])+ord(data_in[1])
        echo = (2**15)*ord(data_in[2])+(2**8)*ord(data_in[3])+(2**7)*ord(data_in[4])+ ord(data_in[5])
        step1 = (2**7)*ord(data_in[6])+ord(data_in[7])
        step2 = (2**7)*ord(data_in[8])+ord(data_in[9])
        y = canal_n1*3.2/(2**12-1) # Escalamiento
        i += 1
        #Amplitud_matrix = np.append(Amplitud_matrix, [y])
        #Time_matrix = np.append(Time_matrix, [i])
        T_Final = time.time()
        Dif = T_Final - T_Inicio
        print("echo = {}, step1 = {}, step2 = {}".format(echo/58.0, step1, step2))

    close_port(port)
    # plt.plot(Time_matrix, Amplitud_matrix)
    # plt.show()


if __name__ == "__main__": main()