import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import numpy.random as ran
import random

fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111)

ARRIVE = 1
DEPART = 0
number_of_events = 100000

avg_queu = []
rhos = []
JOVEN=1
VIEJO=2
a_list = [JOVEN, VIEJO]
distribution = [.7, .3]
random_number= random.choices(a_list,distribution)
for i in random_number:
        X=random_number[i-1]

for i in range(1, 10):
    time_between_arrives = 1
    time_serving = i
    aux_fig = plt.figure(figsize=(10, 8))
    aux_ax = aux_fig.add_subplot(111)

    #Initialize
    clock = 0
    events = [(ARRIVE, ran.exponential(time_between_arrives),X)]
    clients_in_queue1 = 0
    clients_in_queue2=0
    cashier_busy = False

    #report variables
    clients1 = [clients_in_queue1]
    clients2 = [clients_in_queue2]
    times = [clock]
    cashier = [cashier_busy]
    for i in range(number_of_events):
        clock = events[0][1]
        if events[0][0] == ARRIVE:
            events.pop(0)
            events.append((ARRIVE,
                           clock + ran.exponential(time_between_arrives),X))
            if events[0][2] == JOVEN:

                clients_in_queue1 += 1
                if cashier_busy == False:

                    clients_in_queue1 -= 1
                    cashier_busy = True
                    events.append((DEPART, clock + ran.exponential(time_serving),X))
            elif events[0][2] == VIEJO:
                clients_in_queue2 += 1
                if cashier_busy == False:

                    clients_in_queue2 -= 1
                    cashier_busy = True
                    events.append((DEPART, clock + ran.exponential(time_serving),X))


            
            events.sort(key=lambda tup: tup[1])                
     
  
        
        elif events[0][1] == DEPART:
            events.pop(0)


            if clients_in_queue1 > 0 :
                cashier_busy = True
                clients_in_queue1 -= 1
                
                events.append((DEPART, clock + ran.exponential(time_serving),X))
                events.sort(key=lambda tup: tup[1])
            
            if clients_in_queue2 > 0:
                cashier_busy = True
               
                clients_in_queue2 -= 1
                events.append((DEPART, clock + ran.exponential(time_serving),X))
                events.sort(key=lambda tup: tup[1])
            if clients_in_queue1 == 0 and clients_in_queue2 == 0:

                cashier_busy = False

        times.append(clock)
        clients1.append(clients_in_queue1)
        clients2.append(clients_in_queue2)
        cashier.append(cashier_busy)

    #report
    report = open("report.csv", "w")
    for t, cas, cli1, cli2 in zip(times, cashier, clients1, clients2):
        report.write(str(t) + "," + str(cas) + "," + str(cli1) + str(cli2) +"\n")
    report.close()
    avg_queu.append(sum(clients1)+sum(clients2) / len(clients1)+len(clients2))
    rhos.append(time_serving / time_between_arrives)
    aux_ax.plot(clients1)
    aux_ax.plot(clients2)

    aux_fig.savefig('graph' + str(rhos[-1]) + '.png')

ax.plot(rhos, avg_queu)
fig.savefig('graph.png')
