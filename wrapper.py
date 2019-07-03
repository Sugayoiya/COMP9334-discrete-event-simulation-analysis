import simulate

# how to run this code:
# just put files needed in current directory and run wrapper.run_series()


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
                    servers,setup_time,delayoff_time,arr_list,ser_list = simulate.read_para_trace(para_file,arrival_file,service_file)
                    print('mode,servers,setup_time,delayoff_time,arr_list,ser_list:\n',
                          j,servers,setup_time,delayoff_time,arr_list,ser_list)
                    # do trace simulation
                    a_c = simulate.simulate(j,arr_list,ser_list,servers,setup_time,delayoff_time)
#                     arrival_complete = combine_list(a,c,j)
                elif j=='random':
                    servers,setup_time,delayoff_time,time_end,arr_list,ser_list = simulate.read_para_random(para_file,arrival_file,service_file)
                    print('mode,servers,setup_time,delayoff_time,time_end,arr_list,ser_list:\n',
                          j,servers,setup_time,delayoff_time,time_end,arr_list,ser_list)
                    # do random simulation
                    a_c = simulate.simulate(j,arr_list,ser_list,servers,setup_time,delayoff_time,time_end)
#                     arrival_complete = combine_list(a,c,j,float(time_end))
                else:
                    servers,setup_time,delayoff_time,time_end,arr_list,ser_list = simulate.read_para_random(para_file,arrival_file,service_file)
                    print('mode,servers,setup_time,delayoff_time,time_end,arr_list,ser_list:\n',
                          j,servers,setup_time,delayoff_time,time_end,arr_list,ser_list)
                    # do random simulation
                    a_c = simulate.simulate(j,arr_list,ser_list,servers,setup_time,delayoff_time,time_end)
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