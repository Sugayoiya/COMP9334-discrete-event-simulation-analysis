import random,math
from collections import defaultdict
from collections import Counter

class job():
    def __init__(self,t,num,m):
        self.state = str(m)
        self.num = str(num)
        self.time = t

# --- support functions starts ---
        
## read file method
def read_para_trace(para_file,arrival_file,service_file):  
    with open(para_file,'r') as para:
        para_list = []
        for i in para:
            para_list.append(i.strip())
        servers,setup,delayoff = para_list[:] 
#         print('servers,setup,delayoff:',servers,setup,delayoff)
    para.close()
    
    with open(arrival_file,'r') as arr:
        arr_list =[]
        for i in arr:
            arr_list.append(int(i.strip()))
#         print('arrival:',arr_list)
    arr.close()
    
    with open(service_file,'r') as service:
        ser_list = []
        for i in service:
            ser_list.append(int(i.strip()))
#         print('service:',ser_list)
    service.close()
    return servers,setup,delayoff,arr_list,ser_list

def read_para_random(para_file,arrival_file,service_file):  
    with open(para_file,'r') as para:
        para_list = []
        for i in para:
            para_list.append(i.strip())
        servers,setup,delayoff,time_end = para_list[:] 
#         print('servers,setup,delayoff,time_end:',servers,setup,delayoff,time_end)
    para.close()
    
    with open(arrival_file,'r') as arr:
        for i in arr:
            arr_list = (float(i.strip()))
#         print('arrival:',arr_list)
    arr.close()
    
    with open(service_file,'r') as service:
        for i in service:
            ser_list = (float(i.strip()))
#         print('service:',ser_list)
    service.close()
    return servers,setup,delayoff,time_end,arr_list,ser_list

## read file method ends

def nextTime(rateParameter):
    return -math.log(1.0 - random.random()) / rateParameter

def generate_exp(T_end, arrival, service, fix = 0, seed = 0):
    arrival_list = []
    service_list = []
    arr , ser = 0.0, 0.0 
    fix = int(fix)
    seed = int(seed)
    if fix == 1:
        random.seed(seed)
    arr += nextTime(arrival)
    while arr<= T_end:
        arrival_list.append(arr)
        ser = nextTime(service)+nextTime(service)+nextTime(service)
        service_list.append(ser)
        arr += nextTime(arrival)
    return arrival_list,service_list
    print(len(arrival_list) == len(service_list))

def check_server(server_state): # check number of each state of servers
        count = []
        for  i in server_state:
            count.append(server_state[i][0])
        return Counter(count)
        
def check_job(depatcher_queue): # check jobs two states
    count = []
    for i in depatcher_queue:
        count.append(i.state)
    return Counter(count)

def find_server_num(server_state,time): 
    for i in server_state:
        if server_state[i][1] == time:
            return i
        
def find_longest_setup(server_state):
    time = 0
    num = 0
    for i in server_state:
        if server_state[i][0] == '1':
            if server_state[i][1] > time:
                time = server_state[i][1]
                num = i
    return num

def find_longest_delayedoff(server_state,master_clock):
    num = 0
    time = 0
    real_time = 0
    for i in server_state:
        if server_state[i][0] == '3':
#             print(i,server_state[i][1],master_clock)
            if server_state[i][1] - master_clock > time:
                time = server_state[i][1] - master_clock
                num = i
                real_time = server_state[i][1]
#     print(num,real_time)
    return num,real_time

def find_delayedoff_server(server_state,time):
    for i in server_state:
        if server_state[i][1] == time:
            return i
        
def combine_list(a,c,mode,T_end = 0.0):
    arrival_complete = []
#     print(len(a) == len(c))
    for i in range(len(a)):
        if mode == 'random':
            if c[i]<T_end:
                arrival_complete.append((a[i],c[i]))
        else:
            arrival_complete.append((a[i],c[i]))
    arrival_complete.sort(key = lambda x: x[1],reverse = False)
    return arrival_complete
    

# === support functions ends ===
        
# --- simulation main function ---

def simulate(mode,arr_list,ser_list,servers,setup_time,delayoff_time,time_end = 0.0):
    server_state = defaultdict(list)  # { server num:['state',time] } 
    event = [] # sorted by time -includes setup, arrival and complete
    master_clock = 0.0
    # arrival = [1.0, 2.0, 3.2, 3.3] 
    # service = [.1, .2, .3, .4]
    time_end = float(time_end)
    if mode =='trace':
        arrival,service = arr_list,ser_list
    elif mode == 'random_fix':
        arrival,service = generate_exp(time_end,arr_list,ser_list,1)
    else:
        arrival,service = generate_exp(time_end,arr_list,ser_list)
    respose_time = 0 # response time
    delayedoff  = float(delayoff_time)  # delayedoff time to off state (Tc)
    depatcher_queue = []  # jobs in the queue
    check_state = 0  
    job_num = 1
    setup_time = float(setup_time) # the time needed setting up an off server to process a job
    complete_time = [0.0]*len(arrival) # ordered by arrival time
    mrt = 0.0
    arrival_complete = [] # final list
    
    m = int(servers) # num of servers
    for i in range(1, m+1): # initialize servers
        server_state[i].append('0')
        server_state[i].append(0)

    # arrival = [11, 11.2, 11.3, 13] 
    # service = [1, 1.4, 5, 1]
    # # initialize
    # server_state[1].append('3')
    # server_state[1].append(20) 
    # server_state[2].append('3')
    # server_state[2].append(17) 
    # server_state[3].append('0')
    # server_state[3].append(0) 
        
    # ll=server_state # test
    server_state # server num:[ state, time(default = 0)]
    for x in arrival:
        event.append((x,'arrival'))
                     
    # print('event:',event,'\n')

    while len(event)!=0:
        event.sort(key = lambda x: x[0],reverse = False) # sorted event list by time
        event_now = event.pop(0)
        time_passed = event_now[0] - master_clock
        master_clock = event_now[0]
    #     print('-----------------------  -----------------------')
    #     print('event:',event,'\n')

        if event_now[1] =='arrival':
        #     print('arrival')

            check_server_state = check_server(server_state)
    #         print(check_server_state)
        #     print(set(check_state)) 
            check_job_state = check_job(depatcher_queue)
    #         print(check_job_state)
            
            if '3' in set(check_server_state): # at least one delayedoff server
                depatcher_queue.append(job(event_now[0],job_num,'Delayed'))
                delayedoff_to_busy,time = find_longest_delayedoff(server_state,master_clock)
                server_state[delayedoff_to_busy][0] = '4'
                temp = master_clock + service[job_num-1]
                
    #             print(len(event))
                for i in range(len(event)):
    #                 print(i)
                    if event[i] == (time,'delayedoff'):
                        event.pop(i)
                        break
                complete_time[int(depatcher_queue.pop().num)-1] = temp
                server_state[delayedoff_to_busy][1] = temp
                event.append((temp,'completed'))
                
    #             print('server_state:\n',server_state,'\n\ndepatcher_queue:\n',
    #                   [(i.num,i.state) for i in depatcher_queue],'\n\nmaster_clock:',master_clock,'\n')
    #             print('event:',event,'\n')
                job_num += 1
                continue
            
            elif '0' in set(check_server_state): # random choose one off server to setup
                depatcher_queue.append(job(event_now[0],job_num,'MARKED'))
                job_num += 1
    #             print(server_state)
                off_servers = [] # off state
                for i in server_state:
                    if server_state[i][0] =='0':
                        off_servers.append(i)
                temp = off_servers[random.randint(0,len(off_servers)-1)]
                server_state[temp][0]= '1'
                server_state[temp][1] = master_clock+setup_time
                event.append((master_clock+setup_time,'setup')) # what time setup finished
                
    #             print('server_state:\n',server_state,'\n\ndepatcher_queue:\n',
                      
    #                   [(i.num,i.state) for i in depatcher_queue],'\n\nmaster_clock:',master_clock,'\n')
    #             print('event:',event,'\n')

                continue
                
            else: # all busy (need to be inplemented)
                depatcher_queue.append(job(event_now[0],job_num,'UNMARKED'))
    #             print('server_state:\n',server_state,'\n\ndepatcher_queue:\n',
    #                   [(i.num,i.state) for i in depatcher_queue],'\n\nmaster_clock:',master_clock,'\n')
    #             print('event:',event,'\n')
                job_num += 1
                continue

        
        if event_now[1] =='setup': # time for this server to do job
    #         print('setup server is :',find_server_num(server_state, master_clock))
            temp = find_server_num(server_state, master_clock)
            server_state[temp][0]= '2'
            num = int(depatcher_queue.pop(0).num)-1
            busy_time = master_clock+service[num]
            complete_time[num] = busy_time
            server_state[temp][1] = busy_time
            
            event.append((busy_time,'completed')) # what time job completed
    #         print('event(setup):',event,'\n','\n\ndepatcher_queue:\n',
    #               [(i.num,i.state) for i in depatcher_queue],
    #               'server_state:\n',server_state,'\n\nmaster_clock:',master_clock,'\n')
            continue
        
        if event_now[1] =='completed':
            temp = find_server_num(server_state, master_clock) # num of server which completed job
            
            check_job_state = check_job(depatcher_queue)
    #         print('completed a job,',check_job_state,'\n')
            if 'MARKED' in check_job_state:
    #             print('\nthere are still marked jobs in queue\n')
                server_state[temp][0]= '2'
                num = int(depatcher_queue.pop(0).num)-1
                busy_time = master_clock+service[num] # job in the front 
                complete_time[num] = busy_time
                server_state[temp][1] = busy_time           
                
                event.append((busy_time,'completed')) # what time job completed
                
                if 'UNMARKED' in check_job_state:
                    # still some unmarked remain --> unmarked changed to marked
                    for i in depatcher_queue:
                        if i.state =='UNMARKED':
                            i.state = 'MARKED'
                            break
                else:
                    # no unmarked remain --> marked -1 setup -1
                    server_to_off = int(find_longest_setup(server_state))
    #                 print('server_to_off:',server_to_off,'\n',server_state)
                    for i in range(len(event)):
    #                     print(event[i],server_state[server_to_off])
                        if event[i] == (server_state[server_to_off][1],'setup'):
        #                     event.pop((server_state[server_to_off][1],'setup'))
                            event.pop(i)
                            break
                    server_state[server_to_off][0]= '0'
                    server_state[server_to_off][1]= 0
                
    #             print('event(complete,marked):',event,'\n','\n\ndepatcher_queue:\n',
    #                   [(i.num,i.state) for i in depatcher_queue],'server_state:\n',server_state,
    #                   '\n\nmaster_clock:',master_clock,'\n')
                continue
            elif 'UNMARKED' in check_job_state:
    #             print('\nthere are unmarked jobs in queue\n')
                server_state[temp][0]= '2'
                num = int(depatcher_queue.pop(0).num)-1
                busy_time = master_clock+service[num]
                complete_time[num] = busy_time
                server_state[temp][1] = busy_time
                event.append((busy_time,'completed')) # what time job completed
    #             print('\nprocessing job {} server time is {}'.format(depatcher_queue [0].num,busy_time-master_clock))
    #             print('event(complete,unmarked):',event,'\n','\n\ndepatcher_queue:\n',
    #                   [(i.num,i.state) for i in depatcher_queue],'server_state:\n',server_state,
    #                   '\n\nmaster_clock:',master_clock,'\n')
                continue
            else:
    #             print('\nno jobs in queue\n')
                server_state[temp][0]= '3'
                delayedoff_time = master_clock+delayedoff
                server_state[temp][1] = delayedoff_time
                event.append((delayedoff_time,'delayedoff')) # delayedoff
    #             print('\n processing job {} server time is {}'.format(depatcher_queue[0].num,busy_time-master_clock))
    #             print('event(complete,else):',event,'\n','\n\ndepatcher_queue:\n',
    #                   [(i.num,i.state) for i in depatcher_queue],'server_state:\n',server_state,
    #                   '\n\nmaster_clock:',master_clock,'\n')
                continue
        if event_now[1] =='delayedoff':
            temp = find_delayedoff_server(server_state, master_clock)
    #         print(temp)
            server_state[temp][0]= '0'
            server_state[temp][1]= 0
            
    # mean response time
    if time_end != 0.0:
        arrival_complete = combine_list(arrival,complete_time,'random',float(time_end))
    else:
        arrival_complete = combine_list(arrival,complete_time,mode)
    for i in range(len(arrival_complete)):
#         print(complete_time[i],type(complete_time[i]),arrival[i],type(arrival[i]))
        mrt += arrival_complete[i][1]-arrival_complete[i][0]
    mrt = ('%.3f' %(mrt/len(arrival))) # mean response time

# #     print('\nfinished!\n','each jobs finished at:',complete_time,'mrt is :',mrt)
    print('\n{} jobs finished!\nmrt is :{}\n'.format(len(arrival_complete),mrt))
    return arrival_complete,mrt


# run a series of tests
def run_series():   
    a = [] # arrival list
    c = [] # complete list
    arrival_complete = []
    mean_time = 0.0
    
    # read num_tests file
    with open('num_tests.txt','r') as num:
        for i in num:
            tests = int(i.strip())
            # print('num of tests:',tests)
        num.close()

    # read other files according to num_tests.txt
    for i in range(1,tests+1):
        arrival_complete = [] # initialize
        mean_time = 0.0 # initialize
        
        mode_file = 'mode_{}.txt'.format(i) 
        para_file = 'para_{}.txt'.format(i)
        arrival_file = 'arrival_{}.txt'.format(i)
        service_file = 'service_{}.txt'.format(i)
    #     print(mode_file,para_file,arrival_file,service_file)
        
        with open(mode_file,'r') as mode:
            for j in mode:
                print('test {}:'.format(i))
                j = j.strip()
                if j=='trace':
                    servers,setup_time,delayoff_time,arr_list,ser_list = read_para_trace(para_file,arrival_file,service_file)
                    print('mode,servers,setup_time,delayoff_time,arr_list,ser_list:\n',
                          j,servers,setup_time,delayoff_time,arr_list,ser_list)
                    # do trace simulation
                    a_c = simulate(j,arr_list,ser_list,servers,setup_time,delayoff_time)
#                     arrival_complete = combine_list(a,c,j)
                elif j=='random':
                    servers,setup_time,delayoff_time,time_end,arr_list,ser_list = read_para_random(para_file,arrival_file,service_file)
                    print('mode,servers,setup_time,delayoff_time,time_end,arr_list,ser_list:\n',
                          j,servers,setup_time,delayoff_time,time_end,arr_list,ser_list)
                    # do random simulation
                    a_c = simulate(j,arr_list,ser_list,servers,setup_time,delayoff_time,time_end)
#                     arrival_complete = combine_list(a,c,j,float(time_end))
                else:
                    servers,setup_time,delayoff_time,time_end,arr_list,ser_list = read_para_random(para_file,arrival_file,service_file)
                    print('mode,servers,setup_time,delayoff_time,time_end,arr_list,ser_list:\n',
                          j,servers,setup_time,delayoff_time,time_end,arr_list,ser_list)
                    # do random simulation
                    a_c = simulate(j,arr_list,ser_list,servers,setup_time,delayoff_time,time_end)
#                     arrival_complete = combine_list(a,c,j,float(time_end))
        mode.close()
                   
        mrt_file = 'mrt_{}.txt'.format(i)
        departure_file ='departure_{}.txt'.format(i)

        mean_time = ('{0:.3f}'.format(float(a_c[1]))) # mean response time        
        
        with open(mrt_file,'w') as mrt:
            mrt.write('{}\n'.format(mean_time))
        mrt.close()
        
        with open(departure_file,'w') as dep:
            for i in range(len(a_c[0])):
                temp1 = ('{0:.3f}'.format(float(a_c[0][i][0])))
                temp2 = ('{0:.3f}'.format(float(a_c[0][i][1])))
                dep.write('{}\t{}\n'.format(temp1,temp2))
        dep.close()