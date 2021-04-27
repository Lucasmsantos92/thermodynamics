import sqlite3
import matplotlib
import matplotlib.pyplot as plt 
import matplotlib.dates as mdates
import math
from matplotlib import style
style.use ('fivethirtyeight')

conn = sqlite3.connect('banco_de_dados_termo.db')
c = conn.cursor()

print('Qual a mistura de compostos que você quer montar a curva de equilibrio liq/vap?')
molecula1 = input()
molecula2 = input()
print('Você quer montar uma curva a pressão ou temperatura constante?')
print("")
print('1 - Pressão')
print('2 - Temperatura')
resposta0 = input()

if resposta0 == "1":
    print("Qual a temperatura do sistema, em °C?")
    resposta1 = input()
    def leitura():
        c.execute("SELECT * FROM stuffToPlot WHERE molecula = '" + molecula1 + "' OR molecula = '" + molecula2 + "'")
        P1sat = 0
        P2sat = 0
        for linha in c.fetchall():
            print(linha)
            temp = math.exp(linha[1] - (linha[2]/(float(resposta1) + linha[3])))
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
        
elif resposta0 == '2':
    print("Qual a Pressão do sistema, em kPa?")
    resposta2 = input()
    def leitura():
        c.execute("SELECT * FROM stuffToPlot WHERE molecula = '" + molecula1 + "' OR molecula = '" + molecula2 + "'")
        T1sat = 0.0
        T2sat = 0.0
        for linha1 in c.fetchall():
            temp1 = (((linha1[2])/(linha1[1]-math.log(float(resposta2))))-linha1[3])
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
                x1 = (float(resposta2) - P2sat)/(P1sat - P2sat)
                output.append(x1)
                y1 = (x1*P1sat)/float(resposta2)
                
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
                x1 = (float(resposta2) - P2sat)/(P1sat - P2sat)
                output3.append(x1)
                y1 = (x1*P1sat)/float(resposta2)
                
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


