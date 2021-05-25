import sqlite3
from sqlite3 import dbapi2
import numpy
import matplotlib
import matplotlib.pyplot as plt 
import matplotlib.dates as mdates
import math
from matplotlib import style
from numpy import log as ln
style.use ('fivethirtyeight')

conn = sqlite3.connect('banco_de_dados_termo.db')
c = conn.cursor()

print('')
print('Bem vindo(a) ao termoSolver, é um prazer ajuda-lo')
print('Por favor, selecione o número da opção que deseja:')
print('')
print('1 - Diagrama P-xy ou T-xy por Raoult')
print('2 - Calculo de ponto de bolha ou orvalho')
print('3 - Calculo de Flash')
resposta = input()

if resposta == "1":
    print('')
    print('Qual a mistura de compostos que você quer montar a curva de equilibrio liq/vap?')
    print('Digite a primeira, aperte o enter, então repita para a segunda')
    molecula1 = input()
    molecula2 = input()
    print('')
    print('Você quer montar um gráfico(binário) P-xy ou T-xy?')
    print('1 - P-xy')
    print('2 - T-xy')
    grafico = input()

    if grafico == "1":
        print("Qual a temperatura(°C) do sistema?")
        temperatura = input()
        def leitura():
            c.execute("SELECT * FROM stuffToPlot WHERE molecula = '" + molecula1 + "' OR molecula = '" + molecula2 + "'")
            P1sat = 0
            P2sat = 0
            for linha in c.fetchall():
                print(linha)
                temp = math.exp(linha[1] - (linha[2]/(float(temperatura) + linha[3])))
                if (linha[0] == molecula1):
                    P1sat = temp
                else:
                    P2sat = temp
        
            print(P1sat,P2sat)
        
            x1 = 0.0
            output = []
            output1 = []
            output2 = []
            while x1 <= 1:
                P = P2sat + (P1sat - P2sat)*x1
                y1 = (x1*P1sat)/P
                output.append(x1)
                x1 = x1 + 0.2
                output1.append(y1)
                output2.append(P)
            print(output,output1,output2)
        
            plt.ylabel('P/kPa')
            plt.xlabel('x1,y1')
            plt.plot(output,output2,output1,output2)
            plt.show()
            
    elif grafico == '2':
        print("Qual a Pressão do sistema, em kPa?")
        pressao = input()
        def leitura():
            c.execute("SELECT * FROM stuffToPlot WHERE molecula = '" + molecula1 + "' OR molecula = '" + molecula2 + "'")
            T1sat = 0.0
            T2sat = 0.0
            for linha1 in c.fetchall():
                temp1 = (((linha1[2])/(linha1[1]-math.log(float(pressao))))-linha1[3])
                if (linha1[0] == molecula1):
                    T1sat = temp1
                elif(linha1[0] == molecula2):
                    T2sat = temp1
                    
                print(T1sat,T2sat,linha1)
                
            if (T1sat < T2sat):
                P1sat = 0.0
                P2sat = 0.0
                output = []
                output1 = []
                output2 = []
                while T1sat < T2sat:
                    c.execute("SELECT * FROM stuffToPlot WHERE molecula = '" + molecula1 + "' OR molecula = '" + molecula2 + "'")
                    for linha1 in c.fetchall():
                        temp2 = math.exp(linha1[1]-(linha1[2]/(T1sat + linha1[3])))
                        if (linha1[0] == molecula1):
                            P1sat = temp2
                        else:
                            P2sat = temp2
                    x1 = (float(pressao) - P2sat)/(P1sat - P2sat)
                    output.append(x1)
                    y1 = (x1*P1sat)/float(pressao)
                    
                    output1.append(y1)
                    output2.append(T1sat) 
                    T1sat = T1sat + 2           
                output.append(0)
                output1.append(0)
                output2.append(T2sat)
                print(output,output1,output2)            
                
                plt.ylabel('t/°C')    
                plt.xlabel('x1,y1')
                plt.plot(output,output2,output1,output2)
                plt.show()
                
            elif (T1sat > T2sat):
                P1sat = 0.0
                P2sat = 0.0
                output3 = []
                output4 = []
                output5 = []
                while T2sat < T1sat:
                    c.execute("SELECT * FROM stuffToPlot WHERE molecula = '" + molecula1 + "' OR molecula = '" + molecula2 + "'")
                    for linha1 in c.fetchall():
                        temp2 = math.exp(linha1[1]-(linha1[2]/(T1sat + linha1[3])))
                        if (linha1[0] == molecula1):
                            P1sat = temp2
                        else:
                            P2sat = temp2
                    x1 = (float(pressao) - P2sat)/(P1sat - P2sat)
                    output3.append(x1)
                    y1 = (x1*P1sat)/float(pressao)
                    
                    output4.append(y1)
                    output5.append(T1sat)  
                    T1sat = T1sat - 2
                                
                output3.append(0)
                output4.append(0)
                output5.append(T1sat)
                print(output3,output4,output5)            
                
                plt.ylabel('t/°C')    
                plt.xlabel('x1,y1')
                plt.plot(output3,output5,output4,output5)
                plt.show()
    leitura()
    c.close()
    conn.close()    

if resposta == "2":
    print('')
    print('Para o calculo dos pontos de bolha ou orvalho, você possui qual das opções abaixo?')
    print('Por favor, selecione o número da opção e aperte o enter')
    print('1 - x1')
    print('2 - y1')
    resposta3 = input()
    print('')
    print('1 - Pressão')
    print('2 - Temperatura')
    resposta4 = input()

    if resposta3 == '1' and resposta4 == '2':    
        print('Quais os compostos da mistura que você tem?')
        molecula1 = input()
        molecula2 = input()
        print('Qual a fração molar de liquido do componente mais leve? (x1)')
        x1 = input()
        print('Qual a Temperatura(°C)?')
        temperatura = input()
        def leitura():
            c.execute("SELECT * FROM stuffToPlot WHERE molecula = '" + molecula1 + "' OR molecula = '" + molecula2 + "'")
            P1sat = 0
            P2sat = 0
            for linha in c.fetchall():
                print(linha)
                temp = math.exp(linha[1] - (linha[2]/(float(temperatura) + linha[3])))
                if (linha[0] == molecula1):
                    P1sat = temp
                else:
                    P2sat = temp                   
            Pressao = float(x1)*P1sat + (1-float(x1))*P2sat
            y1 = float(x1)*P1sat/float(Pressao)
            print ('O calculo de Bolha P foi concluido:')
            print('o y1 é ' + str(y1))
            print('O Pressão é ' + str(Pressao))

    if resposta3 == '2' and resposta4 == '2':
        print('Quais os compostos da mistura que você tem?')
        molecula1 = input()
        molecula2 = input()
        print('Qual a fração molar do vapor do componente mais leve? (y1)')
        y1 = input()
        print('Qual a Temperatura(°C)?')
        temperatura = input()        
        def leitura():
            c.execute("SELECT * FROM stuffToPlot WHERE molecula = '" + molecula1 + "' OR molecula = '" + molecula2 + "'")
            P1sat = 0
            P2sat = 0
            for linha in c.fetchall():
                temp = math.exp(linha[1] - (linha[2]/(float(temperatura) + linha[3])))
                if (linha[0] == molecula1):
                    P1sat = temp
                else:
                    P2sat = temp                   
            Pressao = 1/((float(y1)/P1sat)+(1-float(y1))/P2sat)
            x1 = float(y1)*Pressao/P1sat
            print ('O calculo de Orvalho P foi concluido:')
            print('o valor de x1 é ' + str(x1))
            print('A Pressão é ' + str(Pressao) + 'kPa')
    
    if resposta3 == '2' and resposta4 == '1':
        print('Quais os compostos da mistura que você tem?')
        molecula1 = input()
        molecula2 = input()
        print('Qual a fração molar de vapor do componente mais leve? (y1)')
        y1 = input()
        print('Qual a Pressão(kPa)?')
        pressao = input()
        def leitura():
            c.execute("SELECT * FROM stuffToPlot WHERE molecula = '" + molecula1 + "' OR molecula = '" + molecula2 + "'")
            T1sat = 0
            T2sat = 0
            for linha in c.fetchall():
                temp = (linha[2]/(linha[1]-ln(float(pressao)))) - linha[3]
                if (linha[0] == molecula1):
                    T1sat = temp
                else:
                    T2sat = temp
            T = float(y1)*T1sat + (1-float(y1))*T2sat
            def leitura1():
                c.execute("SELECT * FROM stuffToPlot WHERE molecula = '" + molecula1 + "' OR molecula = '" + molecula2 + "'")
                P1sat = 0
                P2sat = 0
                for linha in c.fetchall():
                    temp = math.exp(linha[1] - (linha[2]/(float(T) + linha[3])))
                    if (linha[0] == molecula1):
                        P1sat = temp
                        A = linha[1]
                        B = linha[2]
                        C = linha[3]
                    else:
                        P2sat = temp
                alfa = P1sat/P2sat
                P1sat_novo = float(pressao)*(float(y1) + (1-float(y1))*alfa)
                T2novo = B/(A-ln(float(P1sat_novo))) - C                                    
                def leitura2():
                    c.execute("SELECT * FROM stuffToPlot WHERE molecula = '" + molecula1 + "' OR molecula = '" + molecula2 + "'")
                    P1sat1 = 0
                    P2sat1 = 0
                    for linha in c.fetchall():
                        temp = math.exp(linha[1] - (linha[2]/(float(T2novo) + linha[3])))
                        if (linha[0] == molecula1):
                            P1sat1 = temp
                            A = linha[1]
                            B = linha[2]
                            C = linha[3]
                        else:
                            P2sat1 = temp
                    alfa = P1sat1/P2sat1
                    P1sat_novo1 = float(pressao)*(float(y1) + (1-float(y1))*alfa)
                    T2novo1 = B/(A-ln(float(P1sat_novo1))) - C
                    def leitura3():
                        c.execute("SELECT * FROM stuffToPlot WHERE molecula = '" + molecula1 + "' OR molecula = '" + molecula2 + "'")
                        P1sat2 = 0
                        P2sat2 = 0
                        for linha in c.fetchall():
                            temp = math.exp(linha[1] - (linha[2]/(float(T2novo1) + linha[3])))
                            if (linha[0] == molecula1):
                                P1sat2 = temp
                                A = linha[1]
                                B = linha[2]
                                C = linha[3]
                            else:
                                P2sat2 = temp
                        alfa = P1sat2/P2sat2
                        P1sat_novo2 = float(pressao)*(float(y1) + (1-float(y1))*alfa)
                        T2novo2 = B/(A-ln(float(P1sat_novo2))) - C
                        def leitura4():
                            c.execute("SELECT * FROM stuffToPlot WHERE molecula = '" + molecula1 + "' OR molecula = '" + molecula2 + "'")
                            P1sat3 = 0
                            P2sat3 = 0
                            for linha in c.fetchall():
                                temp = math.exp(linha[1] - (linha[2]/(float(T2novo2) + linha[3])))
                                if (linha[0] == molecula1):
                                    P1sat3 = temp
                                    A = linha[1]
                                    B = linha[2]
                                    C = linha[3]
                                else:
                                    P2sat3 = temp

                            alfa = P1sat3/P2sat3
                            P1sat_novo3 = float(pressao)*(float(y1) + (1-float(y1))*alfa)
                            T2novo3 = B/(A-ln(float(P1sat_novo3))) - C
                            def leitura5():
                                c.execute("SELECT * FROM stuffToPlot WHERE molecula = '" + molecula1 + "' OR molecula = '" + molecula2 + "'")
                                P1sat4 = 0
                                P2sat4 = 0
                                for linha in c.fetchall():
                                    temp = math.exp(linha[1] - (linha[2]/(float(T2novo3) + linha[3])))
                                    if (linha[0] == molecula1):
                                        P1sat4 = temp
                                        A = linha[1]
                                        B = linha[2]
                                        C = linha[3]
                                    else:
                                        P2sat4 = temp
                                alfa = P1sat4/P2sat4
                                P1sat_novo4 = float(pressao)*(float(y1) + (1-float(y1))*alfa)
                                T2novo4 = B/(A-ln(float(P1sat_novo4))) - C
                                def leitura6():
                                    c.execute("SELECT * FROM stuffToPlot WHERE molecula = '" + molecula1 + "' OR molecula = '" + molecula2 + "'")
                                    P1sat5 = 0
                                    P2sat5 = 0
                                    for linha in c.fetchall():
                                        temp = math.exp(linha[1] - (linha[2]/(float(T2novo4) + linha[3])))
                                        if (linha[0] == molecula1):
                                            P1sat5 = temp
                                            A = linha[1]
                                            B = linha[2]
                                            C = linha[3]
                                        else:
                                            P2sat5 = temp
                                    alfa = P1sat5/P2sat5
                                    P1sat_novo5 = float(pressao)*(float(y1) + (1-float(y1))*alfa)
                                    T2novo5 = B/(A-ln(float(P1sat_novo5))) - C
                                    def leitura7():
                                        c.execute("SELECT * FROM stuffToPlot WHERE molecula = '" + molecula1 + "' OR molecula = '" + molecula2 + "'")
                                        P1sat6 = 0
                                        P2sat6 = 0
                                        for linha in c.fetchall():
                                            temp = math.exp(linha[1] - (linha[2]/(float(T2novo5) + linha[3])))
                                            if (linha[0] == molecula1):
                                                P1sat6 = temp
                                                A = linha[1]
                                                B = linha[2]
                                                C = linha[3]
                                            else:
                                                P2sat6 = temp
                                        alfa = P1sat6/P2sat6
                                        P1sat_novo6 = float(pressao)*(float(y1) + (1-float(y1))*alfa)
                                        T2novo6 = B/(A-ln(float(P1sat_novo6))) - C
                                        def leitura8():
                                            c.execute("SELECT * FROM stuffToPlot WHERE molecula = '" + molecula1 + "' OR molecula = '" + molecula2 + "'")
                                            P1sat7 = 0
                                            P2sat7 = 0
                                            for linha in c.fetchall():
                                                temp = math.exp(linha[1] - (linha[2]/(float(T2novo6) + linha[3])))
                                                if (linha[0] == molecula1):
                                                    P1sat7 = temp
                                                    A = linha[1]
                                                    B = linha[2]
                                                    C = linha[3]
                                                else:
                                                    P2sat7 = temp
                                            alfa = P1sat7/P2sat7
                                            P1sat_novo7 = float(pressao)*(float(y1) + (1-float(y1))*alfa)
                                            T2novo7 = B/(A-ln(float(P1sat_novo7))) - C
                                            x1 = float(y1)*float(pressao)/P1sat_novo7
                                            print('O valor de x1 é ' + str(x1) + ' e o valor da temperatura é ' + str(T2novo7))                
                                        leitura8()
                                    leitura7()
                                leitura6()
                            leitura5()
                        leitura4()
                    leitura3()                    
                leitura2()                                      
            leitura1()
                                                
    if resposta3 == '1' and resposta4 == '1':
        print('Quais os compostos da mistura que você tem?')
        molecula1 = input()
        molecula2 = input()
        print('Qual a fração molar de liquido do componente mais leve? (x1)')
        x1 = input()
        print('Qual a Pressão(kPa)?')
        pressao = input() 
        def leitura():
            c.execute("SELECT * FROM stuffToPlot WHERE molecula = '" + molecula1 + "' OR molecula = '" + molecula2 + "'")
            T1sat = 0
            T2sat = 0
            for linha in c.fetchall():
                temp = (linha[2]/(linha[1]-ln(float(pressao)))) - linha[3]
                if (linha[0] == molecula1):
                    T1sat = temp
                else:
                    T2sat = temp
            T = float(x1)*T1sat + (1-float(x1))*T2sat
            def leitura1():
                c.execute("SELECT * FROM stuffToPlot WHERE molecula = '" + molecula1 + "' OR molecula = '" + molecula2 + "'")
                P1sat = 0
                P2sat = 0
                for linha in c.fetchall():
                    temp = math.exp(linha[1] - (linha[2]/(float(T) + linha[3])))
                    if (linha[0] == molecula1):
                        P1sat = temp
                    else:
                        P2sat = temp
                        A = linha[1]
                        B = linha[2]
                        C = linha[3]
                alfa = P1sat/P2sat
                P2sat_novo = float(pressao)/(float(x1)*alfa + (1-float(x1)))
                T2novo = B/(A-ln(float(P2sat))) - C                                      
                def leitura2():
                    c.execute("SELECT * FROM stuffToPlot WHERE molecula = '" + molecula1 + "' OR molecula = '" + molecula2 + "'")
                    P1sat1 = 0
                    P2sat1 = 0
                    for linha in c.fetchall():
                        temp = math.exp(linha[1] - (linha[2]/(float(T2novo) + linha[3])))
                        if (linha[0] == molecula1):
                            P1sat1 = temp
                        else:
                            P2sat1 = temp
                            A = linha[1]
                            B = linha[2]
                            C = linha[3]
                    alfa = P1sat1/P2sat1
                    P2sat_novo1 = float(pressao)/(float(x1)*alfa + (1-float(x1)))
                    T2novo1 = B/(A-ln(float(P2sat_novo1))) - C
                    def leitura3():
                        c.execute("SELECT * FROM stuffToPlot WHERE molecula = '" + molecula1 + "' OR molecula = '" + molecula2 + "'")
                        P1sat2 = 0
                        P2sat2 = 0
                        for linha in c.fetchall():
                            temp = math.exp(linha[1] - (linha[2]/(float(T2novo1) + linha[3])))
                            if (linha[0] == molecula1):
                                P1sat2 = temp
                            else:
                                P2sat2 = temp
                                A = linha[1]
                                B = linha[2]
                                C = linha[3]
                        alfa = P1sat2/P2sat2
                        P2sat_novo2 = float(pressao)/(float(x1)*alfa + (1-float(x1)))
                        T2novo2 = B/(A-ln(float(P2sat_novo2))) - C
                        def leitura4():
                            c.execute("SELECT * FROM stuffToPlot WHERE molecula = '" + molecula1 + "' OR molecula = '" + molecula2 + "'")
                            P1sat3 = 0
                            P2sat3 = 0
                            for linha in c.fetchall():
                                temp = math.exp(linha[1] - (linha[2]/(float(T2novo2) + linha[3])))
                                if (linha[0] == molecula1):
                                    P1sat3 = temp
                                else:
                                    P2sat3 = temp
                                    A = linha[1]
                                    B = linha[2]
                                    C = linha[3]
                            alfa = P1sat3/P2sat3
                            P2sat_novo3 = float(pressao)/(float(x1)*alfa + (1-float(x1)))
                            T2novo3 = B/(A-ln(float(P2sat_novo3))) - C
                            def leitura5():
                                c.execute("SELECT * FROM stuffToPlot WHERE molecula = '" + molecula1 + "' OR molecula = '" + molecula2 + "'")
                                P1sat4 = 0
                                P2sat4 = 0
                                for linha in c.fetchall():
                                    temp = math.exp(linha[1] - (linha[2]/(float(T2novo3) + linha[3])))
                                    if (linha[0] == molecula1):
                                        P1sat4 = temp
                                    else:
                                        P2sat4 = temp
                                        A = linha[1]
                                        B = linha[2]
                                        C = linha[3]
                                alfa = P1sat4/P2sat4
                                P2sat_novo4 = float(pressao)/(float(x1)*alfa + (1-float(x1)))
                                T2novo4 = B/(A-ln(float(P2sat_novo4))) - C
                                def leitura6():
                                    c.execute("SELECT * FROM stuffToPlot WHERE molecula = '" + molecula1 + "' OR molecula = '" + molecula2 + "'")
                                    P1sat5 = 0
                                    P2sat5 = 0
                                    for linha in c.fetchall():
                                        temp = math.exp(linha[1] - (linha[2]/(float(T2novo4) + linha[3])))
                                        if (linha[0] == molecula1):
                                            P1sat5 = temp
                                        else:
                                            P2sat5 = temp
                                            A = linha[1]
                                            B = linha[2]
                                            C = linha[3]
                                    alfa = P1sat5/P2sat5
                                    P2sat_novo5 = float(pressao)/(float(x1)*alfa + (1-float(x1)))
                                    T2novo5 = B/(A-ln(float(P2sat_novo5))) - C
                                    def leitura7():
                                        c.execute("SELECT * FROM stuffToPlot WHERE molecula = '" + molecula1 + "' OR molecula = '" + molecula2 + "'")
                                        P1sat6 = 0
                                        P2sat6 = 0
                                        for linha in c.fetchall():
                                            temp = math.exp(linha[1] - (linha[2]/(float(T2novo5) + linha[3])))
                                            if (linha[0] == molecula1):
                                                P1sat6 = temp
                                            else:
                                                P2sat6 = temp
                                                A = linha[1]
                                                B = linha[2]
                                                C = linha[3]
                                        alfa = P1sat6/P2sat6
                                        P2sat_novo6 = float(pressao)/(float(x1)*alfa + (1-float(x1)))
                                        T2novo6 = B/(A-ln(float(P2sat_novo6))) - C
                                        def leitura8():
                                            c.execute("SELECT * FROM stuffToPlot WHERE molecula = '" + molecula1 + "' OR molecula = '" + molecula2 + "'")
                                            P1sat7 = 0
                                            P2sat7 = 0
                                            for linha in c.fetchall():
                                                temp = math.exp(linha[1] - (linha[2]/(float(T2novo6) + linha[3])))
                                                if (linha[0] == molecula1):
                                                    P1sat7 = temp
                                                else:
                                                    P2sat7 = temp
                                                    A = linha[1]
                                                    B = linha[2]
                                                    C = linha[3]
                                            alfa = P1sat7/P2sat7
                                            P2sat_novo7 = float(pressao)/(float(x1)*alfa + (1-float(x1)))
                                            T2novo7 = B/(A-ln(float(P2sat_novo7))) - C
                                            y2 = (1-float(x1))*P2sat_novo7/float(pressao) 
                                            y1 = 1 - y2
                                            print('O valor de y1 é ' + str(y1) + ' e o valor da temperatura é ' + str(T2novo7))   
                                        leitura8()
                                    leitura7()
                                leitura6()
                            leitura5()
                        leitura4()
                    leitura3()                    
                leitura2()                                      
            leitura1()
    leitura()
    c.close()
    conn.close()
    
if resposta == '3':
    print('')
    print('Seu sistema é:')
    print('1 - Binário')
    print('2 - Ternário')
    print('3 - Quaternário')
    flash = input()

    if flash == '1':
        print('')
        print('Quais os compostos que compõem a mistura?')
        molecula1 = input()
        molecula2 = input()
        print('')
        print('Qual a fração de cada um na composição global? (z1,z2,z3)')
        z1 = input()
        z2 = input()
        print('')
        print('Qual a temperatura(°C) do sistema?')
        temperatura = input()
        print('')
        print('Qual a pressão do sistema?')
        pressao = input()
        def leitura():
            c.execute("SELECT * FROM stuffToPlot WHERE molecula = '" + molecula1 + "' OR molecula = '" + molecula2 + "'")
            P1sat = 0
            P2sat = 0
            for linha in c.fetchall():
                temp = math.exp(linha[1] - (linha[2]/(float(temperatura) + linha[3])))
                if (linha[0] == molecula1):
                    P1sat = temp
                if (linha[0] == molecula2):
                    P2sat = temp
            Pbol = float(z1)*P1sat + float(z2)*P2sat 
            Porv = 1/((float(z1)/P1sat)+(float(z2)/P2sat))
            k1 = P1sat/float(pressao)
            k2 = P2sat/float(pressao)
            v = 0.1
            for i in range(100):
                primeiro_termo = (float(z1)*k1/(1+(k1-1)*v))
                segundo_termo = (float(z2)*k2/(1 + v*(k2-1)))
                derivada_primeiro_termo = (float(k1)-1)*k1*float(z1)/(((k1-1)*v+1)**2)
                derivada_segundo_termo = (float(k2)-1)*k2*float(z2)/(((k2-1)*v+1)**2)
                vnew = v - (primeiro_termo + segundo_termo - 1)/(- derivada_primeiro_termo - derivada_segundo_termo)
                if abs(vnew - v) < 0.01: break
                v = vnew
            l = 1 - vnew
            y1 = float(z1)*k1/(1+vnew*(k1-1))
            y2 = float(z2)*k2/(1+vnew*(k2-1))
            x1 = y1/k1
            x2 = y2/k2
            x = x1+x2
            y = y1+y2
            total = v + l
            print('')
            print('Os resultados são:')
            print('')
            print('x1 = ' + str(x1))
            print('x2 = ' + str(x2))
            print('y1 = ' + str(y1))
            print('y2 = ' + str(y2))
            print('L = ' + str(l))
            print('V = ' + str(v))
            print('Lembrando que o somatorio das frações molares tem que dar 1(ou bem próximo), assim como o somatorio da parte vapor e líquida, então confira:')
            print('')
            print('x1 + x2 = ' + str(x))
            print('y1 + y2 = ' + str(y))
            print('V + L = ' + str(total))
            print('')

    if flash == '2':
        print('')
        print('Quais os compostos que compõem a mistura?')
        molecula1 = input()
        molecula2 = input()
        molecula3 = input()
        print('')
        print('Qual a fração de cada um na composição global? (z1,z2,z3)')
        z1 = input()
        z2 = input()
        z3 = input()
        print('')
        print('Qual a temperatura(°C) do sistema?')
        temperatura = input()
        print('')
        print('Qual a pressão do sistema?')
        pressao = input()
        def leitura():
            c.execute("SELECT * FROM stuffToPlot WHERE molecula = '" + molecula1 + "' OR molecula = '" + molecula2 + "' OR molecula = '" + molecula3 + "'")
            P1sat = 0
            P2sat = 0
            P3sat = 0
            for linha in c.fetchall():
                temp = math.exp(linha[1] - (linha[2]/(float(temperatura) + linha[3])))
                if (linha[0] == molecula1):
                    P1sat = temp
                if (linha[0] == molecula2):
                    P2sat = temp
                if (linha[0] == molecula3):
                    P3sat = temp
            Pbol = float(z1)*P1sat + float(z2)*P2sat + float(z3)*P3sat
            Porv = 1/((float(z1)/P1sat)+(float(z2)/P2sat)+(float(z3)/P3sat))
            k1 = P1sat/float(pressao)
            k2 = P2sat/float(pressao)
            k3 = P3sat/float(pressao)
            v = 0.1
            for i in range(100):
                primeiro_termo = (float(z1)*k1/(1+(k1-1)*v))
                segundo_termo = (float(z2)*k2/(1 + v*(k2-1)))
                terceiro_termo = (float(z3)*k3/(1 + v*(k3-1)))
                derivada_primeiro_termo = (float(k1)-1)*k1*float(z1)/(((k1-1)*v+1)**2)
                derivada_segundo_termo = (float(k2)-1)*k2*float(z2)/(((k2-1)*v+1)**2)
                derivada_terceiro_termo = (float(k3)-1)*k3*float(z3)/(((k3-1)*v+1)**2)
                vnew = v - (primeiro_termo + segundo_termo + terceiro_termo -1)/(- derivada_primeiro_termo - derivada_segundo_termo - derivada_terceiro_termo)
                if abs(vnew - v) < 0.01: break
                v = vnew
            l = 1 - vnew
            y1 = float(z1)*k1/(1+vnew*(k1-1))
            y2 = float(z2)*k2/(1+vnew*(k2-1))
            y3 = float(z3)*k3/(1+ vnew*(k3-1))
            x1 = y1/k1
            x2 = y2/k2
            x3 = y3/k3
            x = x1+x2+x3
            y = y1+y2+y3
            total = v + l
            print('')
            print('Os resultados são:')
            print('')
            print('x1 = ' + str(x1))
            print('x2 = ' + str(x2))
            print('x3 = ' + str(x3))
            print('y1 = ' + str(y1))
            print('y2 = ' + str(y2))
            print('y3 = ' + str(y3))
            print('L = ' + str(l))
            print('V = ' + str(v))
            print('')
            print('Lembrando que o somatorio das frações molares tem que dar 1(ou bem próximo), assim como o somatorio da parte vapor e líquida, então confira:')
            print('')
            print('x1 + x2 + x3 = ' + str(x))
            print('y1 + y2 + y3 = ' + str(y))
            print('V + L = ' + str(total))
            print('')

    if flash == '3':
        print('')
        print('Quais os compostos que compõem a mistura?')
        molecula1 = input()
        molecula2 = input()
        molecula3 = input()
        molecula4 = input()
        print('')
        print('Qual a fração de cada um na composição global? (z1,z2,z3,z4)')
        z1 = input()
        z2 = input()
        z3 = input()
        z4 = input()
        print('')
        print('Qual a temperatura(°C) do sistema?')
        temperatura = input()
        print('')
        print('Qual a pressão do sistema?')
        pressao = input()
        def leitura():
            c.execute("SELECT * FROM stuffToPlot WHERE molecula = '" + molecula1 + "' OR molecula = '" + molecula2 + "' OR molecula = '" + molecula3 + "' OR molecula = '" + molecula4 + "'")
            P1sat = 0
            P2sat = 0
            P3sat = 0
            P4sat = 0
            for linha in c.fetchall():
                temp = math.exp(linha[1] - (linha[2]/(float(temperatura) + linha[3])))
                if (linha[0] == molecula1):
                    P1sat = temp
                if (linha[0] == molecula2):
                    P2sat = temp
                if (linha[0] == molecula3):
                    P3sat = temp
                if (linha[0] == molecula4):
                    P4sat = temp
            Pbol = float(z1)*P1sat + float(z2)*P2sat + float(z3)*P3sat + float(z4)*P4sat
            Porv = 1/((float(z1)/P1sat)+(float(z2)/P2sat)+(float(z3)/P3sat)+(float(z4)/P4sat))
            k1 = P1sat/float(pressao)
            k2 = P2sat/float(pressao)
            k3 = P3sat/float(pressao)
            k4 = P4sat/float(pressao)
            v = 0.1
            for i in range(100):
                primeiro_termo = (float(z1)*k1/(1+(k1-1)*v))
                segundo_termo = (float(z2)*k2/(1 + v*(k2-1)))
                terceiro_termo = (float(z3)*k3/(1 + v*(k3-1)))
                quarto_termo = (float(z4)*k4/(1 + v*(k4-1)))
                derivada_primeiro_termo = (float(k1)-1)*k1*float(z1)/(((k1-1)*v+1)**2)
                derivada_segundo_termo = (float(k2)-1)*k2*float(z2)/(((k2-1)*v+1)**2)
                derivada_terceiro_termo = (float(k3)-1)*k3*float(z3)/(((k3-1)*v+1)**2)
                derivada_quarto_termo = (float(k4)-1)*k4*float(z4)/(((k4-1)*v+1)**2)
                vnew = v - (primeiro_termo + segundo_termo + terceiro_termo + quarto_termo - 1)/(- derivada_primeiro_termo - derivada_segundo_termo - derivada_terceiro_termo - derivada_quarto_termo)
                if abs(vnew - v) < 0.01: break
                v = vnew
            l = 1 - vnew
            y1 = float(z1)*k1/(1+vnew*(k1-1))
            y2 = float(z2)*k2/(1+vnew*(k2-1))
            y3 = float(z3)*k3/(1+vnew*(k3-1))
            y4 = float(z4)*k4/(1+vnew*(k4-1))
            x1 = y1/k1
            x2 = y2/k2
            x3 = y3/k3
            x4 = y4/k4
            x = x1+x2+x3+x4
            y = y1+y2+y3+y4
            total = v + l
            print('')
            print('Os resultados são:')
            print('')
            print('x1 = ' + str(x1))
            print('x2 = ' + str(x2))
            print('x3 = ' + str(x3))
            print('x4 = ' + str(x4))
            print('y1 = ' + str(y1))
            print('y2 = ' + str(y2))
            print('y3 = ' + str(y3))
            print('y4 = ' + str(y4))
            print('L = ' + str(l))
            print('V = ' + str(v))
            print('Lembrando que o somatorio das frações molares tem que dar 1(ou bem próximo), assim como o somatorio da parte vapor e líquida, então confira:')
            print('')
            print('x1 + x2 + x3 + x4 = ' + str(x))
            print('y1 + y2 + y3 + y4 = ' + str(y))
            print('V + L = ' + str(total))
            print('')

    leitura()
    c.close()
    conn.close()
