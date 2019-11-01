# COMP9334 report

usage：

```$python3

\>> import wrapper

\>> wrapper.run_series()
```


##  Generate inter-arrival probability distribution and service time distribution



### Cumulative distribution function

If 6 jobs arrive every hour, it means that, on average one job arrives every  10 minutes. Let's define a variable <a href="https://www.codecogs.com/eqnedit.php?latex=\lambda$&space;=$\frac{1}{10}" target="_blank"><img src="https://latex.codecogs.com/gif.latex?\lambda$&space;=$\frac{1}{10}" title="\lambda$ =$\frac{1}{10}" /></a> being the rate parameter. This rate parameter <a href="https://www.codecogs.com/eqnedit.php?latex=\lambda" target="_blank"><img src="https://latex.codecogs.com/gif.latex?\lambda" title="\lambda" /></a> is a measure of frequency: the average rate of events (in this case, jobs) per unit of time (in this case, minutes).

Knowing this, the question that what the probability of a next job arrive within a curtain time is answered by a well-known function called **cumulative distribution function** of **exponential distribution**, and it looks like this:

​						<div align=center><a href="https://www.codecogs.com/eqnedit.php?latex=$F(x)&space;=&space;1&space;-&space;e^{-\lambda&space;x}$" target="_blank"><img src="https://latex.codecogs.com/gif.latex?$F(x)&space;=&space;1&space;-&space;e^{-\lambda&space;x}$" title="$F(x) = 1 - e^{-\lambda x}$" /></a></div>


<div align=center><img src="https://lh3.googleusercontent.com/PIgF2hr0o2OQ3NNWqdscVrTNloKFJTz_BQUDWJ-BgAm87RXU4I8pCCAUGdg2O8g2KcanSm_wEBAB" alt="cumulative distribution function"></div>

As time passes, the probability of arrival increases towards one.



### Generate random number from cumulative distribution function

A method to generate random number from a particular distribution is the *inverse transform method*:
* generate random floating point value **n** between **0** and **1** ( *uniformly distribution*).
* compute the <a href="https://www.codecogs.com/eqnedit.php?latex=F^{-1}(n)" target="_blank"><img src="https://latex.codecogs.com/gif.latex?F^{-1}(n)" title="F^{-1}(n)" /></a>

For **exponential distribution**, its **cumulative distribution function** *(CDF)* is 

<div align=center><a href="https://www.codecogs.com/eqnedit.php?latex=$F(x)&space;=&space;1&space;-&space;e^{-\lambda&space;x}$" target="_blank"><img src="https://latex.codecogs.com/gif.latex?$F(x)&space;=&space;1&space;-&space;e^{-\lambda&space;x}$" title="$F(x) = 1 - e^{-\lambda x}$" /></a></div>

 so the inverse of this *CDF* is 

<div align=center><a href="https://www.codecogs.com/eqnedit.php?latex=$F^{-1}(x)=-log(1-x)/\lambda$" target="_blank"><img src="https://latex.codecogs.com/gif.latex?$F^{-1}(x)=-log(1-x)/\lambda$" title="$F^{-1}(x)=-log(1-x)/\lambda$" /></a></div>

**x** is uniformly distributed between **(0,1)**



### Generate exponential distributed random number using python

Here is one way to implement in python:
```python
import math
import random

def nextTime(rateParameter):
    return -math.log(1.0 - random.random()) / rateParameter
```


Here is some sample output:

```python
>>> nextTime(1/10.0)
6.579616062844679
>>> nextTime(1/10.0)
0.8496748345865709
>>> nextTime(1/10.0)
1.6038624255006428
>>> nextTime(1/10.0)
24.828638903932053
```


Let's run enough times to make sure that the average time arrival by this function really is **10**

```python 
>>>sum([nextTime(1/10) for i in range(1000000)]) / 1000000
9.999013076811442
>>>sum([nextTime(1/10) for i in range(1000000)]) / 1000000
9.98838071976749
>>>sum([nextTime(1/10) for i in range(1000000)]) / 1000000
9.996894414471212
```
It very closes to what we want.



Another thing we can do is:

* Generate $50000$ uniformly distributed numbers in **(0,1)**, 
* then compute <a href="https://www.codecogs.com/eqnedit.php?latex=$-log(1-x)/\lambda​$" target="_blank"><img src="https://latex.codecogs.com/gif.latex?$-log(1-x)/\lambda​$" title="$-log(1-x)/\lambda​$" /></a> ,<a href="https://www.codecogs.com/eqnedit.php?latex=$\lambda&space;=&space;10​$" target="_blank"><img src="https://latex.codecogs.com/gif.latex?$\lambda&space;=&space;10​$" title="$\lambda = 10​$" /></a>, 
* the plot shows below:

<div align=center><img src="https://lh3.googleusercontent.com/Q8JLR6Jqf59UjoyDXs3qUYL_Gv7FhXbjpM9TBNcFPyTXuQWicnjvB1bhiAyT8rDJ52rMjMWsjmUG" alt="plot"></div>

The histogram of the numbers generated in step 2 in many **bins**. The dots in graph show the expected number of *exponential distributed numbers* in each bin.

Now we can use this function to generate the *arrival time list* and *service time list* for the random mode test:
```python
def generate_exp(T_end, arrival, service):
    arrival_list = []
    service_list = []
    arr , ser = 0.0, 0.0 
    # next time = previous time + inter-arrival time generated
    arr += nextTime(arrival) 
    while arr<= T_end:
        arrival_list.append(arr)
        # service time = sum fo three independent exponentially distributed numbers 
        ser = nextTime(service)+nextTime(service)+nextTime(service)
        service_list.append(ser)
        arr += nextTime(arrival)
    return arrival_list,service_list
```



## Simulation code verified

Using the example given in the project
* example 1:

**m** (*number of servers*) is **3** , <a href="https://www.codecogs.com/eqnedit.php?latex=$T_c$" target="_blank"><img src="https://latex.codecogs.com/gif.latex?$T_c$" title="$T_c$" /></a> (*delayed off time*) is **100** and the **setup time** is **50**. Here is the *arrival time* and *service time* table:

Arrival time | Service time
----------- | -----------
10  | 1
20  | 2
32  | 3
33  | 4

```python
mrt is : 41.250
```
* example 2:

**m** (number of servers) is **3** , <a href="https://www.codecogs.com/eqnedit.php?latex=$T_c$" target="_blank"><img src="https://latex.codecogs.com/gif.latex?$T_c$" title="$T_c$" /></a> (delayed off time) is **10** and the **setup time** is **5**. Here is the *arrival time* and *service time* table:

Arrival time | Service time
----------- | -----------
11  | 1
11.2  | 1.4
11.3  | 5
13  | 1
```python
 mrt is : 2.275
```

Here is the two log files of simulation of these two examples:
>log1.txt    log2.txt



## Reproducibility

The *generate_exp()* function given before will generate different list each time because no fixed seed provided. In order to prove reproducibility, the function is changed a little bit as follow:
```python
def generate_exp(T_end, arrival, service, fix = 0, seed = 0):
    arrival_list = []
    service_list = []
    arr , ser = 0.0, 0.0 
    fix = int(fix)
    seed = int(seed)
    if fix == 1: # provide fixed seed so can generate same list each time
        random.seed(seed)
    arr += nextTime(arrival)
    while arr<= T_end:
        arrival_list.append(arr)
        ser = nextTime(service)+nextTime(service)+nextTime(service)
        service_list.append(ser)
        arr += nextTime(arrival)
    return arrival_list,service_list
```
Here is some sample output for a small test in *random_fix* mode, which is random mode with fixed seed so that *(arrive list, service list)* is the same:
```python 
>>> a_c = simulate('random_fix',0.35,1,5,5,0.1,100)
mrt is :6.178
>>> a,c = simulate('random_fix',0.35,1,5,5,0.1,100)
mrt is :6.178
>>> a,c = simulate('random_fix',0.35,1,5,5,0.1,100)
mrt is :6.178
```
and the *arrival list* and *complete list* ( list contains the time each job completes) is:
```python
>>>a_c = simulate('random_fix',0.35,1,5,5,0.1,100)
mrt is :6.178
>>>print(a_c[0])
[(5.31602031732921, 12.580004928056379), (7.361605316663926, 14.773651993798376), (9.211329515387648, 16.545350137177063), (10.157214921039806, 16.872772968246686), (19.915320911285267, 26.53481111463993), (18.089808550628085, 27.84151606174097), (17.029015485363168, 30.077375136240455), (27.754591813021236, 32.522036216576836), (26.892390103029264, 33.89387752016058), (31.388624785005998, 35.876068715550026), (31.391891850235623, 36.875806842326725), (32.515735831882246, 38.97015807567017), (33.86419138414459, 39.696058449854995), (33.53426059528607, 40.18737605462384), (33.294642561652694, 42.03599429971047), (38.67711075082986, 43.99135180993523), (41.207976194899594, 44.01778468515373), (43.65711643059906, 44.75096772296489), (46.36781545662845, 53.17824288655225), (50.416907469906725, 59.68893634723434), (56.94399654391793, 63.52821450493707), (60.43468529209289, 67.41371241551136), (66.87515990939391, 72.16264116103065), (73.09078713903698, 79.79191829937795), (68.58619235358327, 81.31847161055705), (81.12387307843734, 82.77898958665679), (76.288594988652, 83.16868100413538), (75.9326459104134, 83.25005237827565), (81.25612755210626, 86.80410922647263), (84.51691903565222, 88.77129019842613), (87.51776827040938, 93.41440995079586), (86.9680929164618, 93.6680237958128), (88.23069710817259, 94.18891906380902), (87.07400933105534, 95.43949567834447), (87.4519222450316, 96.6877706664429), (90.86722677020244, 97.24950347678353), (90.23197358892396, 98.00360851372253)]
```
```python
>>>a_c = simulate('random_fix',0.35,1,5,5,0.1,100)
mrt is :6.178
>>>print(a_c[0])
[(5.31602031732921, 12.580004928056379), (7.361605316663926, 14.773651993798376), (9.211329515387648, 16.545350137177063), (10.157214921039806, 16.872772968246686), (19.915320911285267, 26.53481111463993), (18.089808550628085, 27.84151606174097), (17.029015485363168, 30.077375136240455), (27.754591813021236, 32.522036216576836), (26.892390103029264, 33.89387752016058), (31.388624785005998, 35.876068715550026), (31.391891850235623, 36.875806842326725), (32.515735831882246, 38.97015807567017), (33.86419138414459, 39.696058449854995), (33.53426059528607, 40.18737605462384), (33.294642561652694, 42.03599429971047), (38.67711075082986, 43.99135180993523), (41.207976194899594, 44.01778468515373), (43.65711643059906, 44.75096772296489), (46.36781545662845, 53.17824288655225), (50.416907469906725, 59.68893634723434), (56.94399654391793, 63.52821450493707), (60.43468529209289, 67.41371241551136), (66.87515990939391, 72.16264116103065), (73.09078713903698, 79.79191829937795), (68.58619235358327, 81.31847161055705), (81.12387307843734, 82.77898958665679), (76.288594988652, 83.16868100413538), (75.9326459104134, 83.25005237827565), (81.25612755210626, 86.80410922647263), (84.51691903565222, 88.77129019842613), (87.51776827040938, 93.41440995079586), (86.9680929164618, 93.6680237958128), (88.23069710817259, 94.18891906380902), (87.07400933105534, 95.43949567834447), (87.4519222450316, 96.6877706664429), (90.86722677020244, 97.24950347678353), (90.23197358892396, 98.00360851372253)]
```



Given the same *arrival list*, it will output the same answer. The reproducibility is proven.

Here are three more reproducibility tests:
```python
test 3: 
mode,servers,setup_time,delayoff_time,time_end,arr_list,ser_list: 
random_fix 3 50 100 1000 0.35 1.0 
finished! 
mrt is :5.908 

test 4: 
mode,servers,setup_time,delayoff_time,time_end,arr_list,ser_list: 
random_fix 4 30 50 5000 0.7 1.0 
finished! 
mrt is :3.572 

test 5: 
mode,servers,setup_time,delayoff_time,time_end,arr_list,ser_list: 
random_fix 5 5 10 1000 0.5 1.0
finished! 
mrt is :3.922
```



##  Determining a suitable value of <a href="https://www.codecogs.com/eqnedit.php?latex=$T_c$" target="_blank"><img src="https://latex.codecogs.com/gif.latex?$T_c$" title="$T_c$" /></a> 

#### determining a suitable value of <a href="https://www.codecogs.com/eqnedit.php?latex=$T_{end}$" target="_blank"><img src="https://latex.codecogs.com/gif.latex?$T_{end}$" title="$T_{end}$" /></a>( *length of simulation* ):

choose the given value in the project document:
the *number of servers* is **5**, *setup time* is **5**, <a href="https://www.codecogs.com/eqnedit.php?latex=$\lambda=&space;0.35$" target="_blank"><img src="https://latex.codecogs.com/gif.latex?$\lambda=&space;0.35$" title="$\lambda= 0.35$" /></a>, <a href="https://www.codecogs.com/eqnedit.php?latex=$\mu&space;=&space;1$" target="_blank"><img src="https://latex.codecogs.com/gif.latex?$\mu&space;=&space;1$" title="$\mu = 1$" /></a>, assume  <a href="https://www.codecogs.com/eqnedit.php?latex=$T_c&space;=&space;0.1$" target="_blank"><img src="https://latex.codecogs.com/gif.latex?$T_c&space;=&space;0.1$" title="$T_c = 0.1$" /></a>. 
<a href="https://www.codecogs.com/eqnedit.php?latex=$T_{end}$" target="_blank"><img src="https://latex.codecogs.com/gif.latex?$T_{end}$" title="$T_{end}$" /></a> starts from **100** to **20100** 

| $T_{end}$ | 100   | 2100  | 4100  | 6100  | 8100  | 10100 | 12100 | 14100 | 16100 | 18100 | 20100 |
| --------- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | :---: |
| $res$     | 5.480 | 6.072 | 6.026 | 5.931 | 6.064 | 6.110 | 6.049 | 6.072 | 6.036 | 6.112 | 6.129 |

It shows that after <a href="https://www.codecogs.com/eqnedit.php?latex=$T_{end}&space;=&space;8100$" target="_blank"><img src="https://latex.codecogs.com/gif.latex?$T_{end}&space;=&space;8100$" title="$T_{end} = 8100$" /></a>, the response time is around **6.06** stably.
So we choose <a href="https://www.codecogs.com/eqnedit.php?latex=$T_{end}=20000$" target="_blank"><img src="https://latex.codecogs.com/gif.latex?$T_{end}=20000$" title="$T_{end}=20000$" /></a> in case.



#### determining the  *number of replications* ( n ):

<a href="https://www.codecogs.com/eqnedit.php?latex=$T_{end}=20000$" target="_blank"><img src="https://latex.codecogs.com/gif.latex?$T_{end}=20000$" title="$T_{end}=20000$" /></a>, considering the running time of the simulation, just starting from  **n=10**.



#### determining  the *end of transient* ( l ):

without removing the transient, one of simulation graph is this:

​	<div align=center><img src="https://lh3.googleusercontent.com/lktMBfEj_FwosmyOgApEse3-cWY2UpWuQicoSjve-kKYAfs4nOymr0z2ZH-MB4_ZLpp9L64Vf6fn" alt="t_end - response time graph"></div>

x-axis is the <a href="https://www.codecogs.com/eqnedit.php?latex=$T_{end}$" target="_blank"><img src="https://latex.codecogs.com/gif.latex?$T_{end}$" title="$T_{end}$" /></a> and y-axis is **mrt** *( mean response time )*

Using a program that implements the transient removal procedure by **Law** and **Kelton**. A parameter <a href="https://www.codecogs.com/eqnedit.php?latex=$\omega$" target="_blank"><img src="https://latex.codecogs.com/gif.latex?$\omega$" title="$\omega$" /></a> can be varied to get a smoothed curve.

* when <a href="https://www.codecogs.com/eqnedit.php?latex=$\omega=1$" target="_blank"><img src="https://latex.codecogs.com/gif.latex?$\omega=1$" title="$\omega=1$" /></a>, the curve shows:

  <div align=center><img src="https://lh3.googleusercontent.com/mQ48ZyFPmrk1iGZvKJTatDpttlLppo-gtDpCNoEJqjb5BQutblZCfhiaUUPdDsAbHBdvQngIcj2d" alt="\omega = 1"></div>

There are some oscillation in the graph so <a href="https://www.codecogs.com/eqnedit.php?latex=$\omega$" target="_blank"><img src="https://latex.codecogs.com/gif.latex?$\omega$" title="$\omega$" /></a> still need to be bigger.

* when <a href="https://www.codecogs.com/eqnedit.php?latex=$\omega=5$" target="_blank"><img src="https://latex.codecogs.com/gif.latex?$\omega=5$" title="$\omega=5$" /></a>, the curve shows: 

  

  <div align=center><img src="https://lh3.googleusercontent.com/3ph3gv5GpKoxrqcvRqYxa1cwiXI5RWM4H21LQJ8gvu7fiirK1Eig0n0xy6WLuzmGvSxGoWo7iaXa" alt="\omega = 5"></div>

Still some oscillation in the graph so <a href="https://www.codecogs.com/eqnedit.php?latex=$\omega$" target="_blank"><img src="https://latex.codecogs.com/gif.latex?$\omega$" title="$\omega$" /></a> still need to be bigger.

* when <a href="https://www.codecogs.com/eqnedit.php?latex=$\omega=20$" target="_blank"><img src="https://latex.codecogs.com/gif.latex?$\omega=20$" title="$\omega=20$" /></a>, the curve shows: 
<div align=center><img src="https://lh3.googleusercontent.com/2i8FyGnPRC7q54t3t0Zew06b9Lonp68cV2lt-DYRQIWdUxXQiS6Obi9vmbUgMQ5T9fRn_poibMtT" alt="\omega = 20"></div>

This is better but still not enough.

* when <a href="https://www.codecogs.com/eqnedit.php?latex=$\omega=50$" target="_blank"><img src="https://latex.codecogs.com/gif.latex?$\omega=50$" title="$\omega=50$" /></a>, the curve shows: 

  <div align=center><img src="https://lh3.googleusercontent.com/p5UEAXKOykNL8Cr1hkFWwH-3kzO_-kaN6XJWqrz6VAxGks4n2FtumiKhvLPJt3ijWVqh0W8R8mNX" alt="\omega = 50"></div>

Much better but just some more test in case.
* when <a href="https://www.codecogs.com/eqnedit.php?latex=$\omega=100$" target="_blank"><img src="https://latex.codecogs.com/gif.latex?$\omega=100$" title="$\omega=100$" /></a>, the curve shows: 
<div align=center><img src="https://lh3.googleusercontent.com/yiA6N0eZPRd-_VWFvI8ZVw82ieRWHAi9k3tU0PMrvW02WzCB1afcWroYzi8AM6Cx0oH40dl1KroK" alt="\omega = 100"></div>

It's good enough. So the **l** ( *end of transient* ) **= 100**
After transient removal, 
* the *sample mean* of **(n = )** **10** replications **= 6.05788588625563**
* the *sample standard deviation* of **10** replications is **0.01587562344671423**
* to compute the **95%** confidence interval, **a = 0.05**
* Since having done **10** independent experiments and wanting **95%**
confidence interval,  using <a href="https://www.codecogs.com/eqnedit.php?latex=$t_{9,0.975}=2.262$" target="_blank"><img src="https://latex.codecogs.com/gif.latex?$t_{9,0.975}=2.262$" title="$t_{9,0.975}=2.262$" /></a>
* the **95%** *confidence interval* is:
<a href="https://www.codecogs.com/eqnedit.php?latex=[6.05788588625563&space;-&space;2.262\frac{0.01587562344671423}{\sqrt{10}},6.05788588625563&space;&plus;2.262\frac{0.01587562344671423}{\sqrt{10}}]" target="_blank"><img src="https://latex.codecogs.com/gif.latex?[6.05788588625563&space;-&space;2.262\frac{0.01587562344671423}{\sqrt{10}},6.05788588625563&space;&plus;2.262\frac{0.01587562344671423}{\sqrt{10}}]" title="[6.05788588625563 - 2.262\frac{0.01587562344671423}{\sqrt{10}},6.05788588625563 +2.262\frac{0.01587562344671423}{\sqrt{10}}]" /></a>

**95%** *Confidence interval of mean response time <a href="https://www.codecogs.com/eqnedit.php?latex==[6.046529938392863,6.069241834118398]" target="_blank"><img src="https://latex.codecogs.com/gif.latex?=[6.046529938392863,6.069241834118398]" title="=[6.046529938392863,6.069241834118398]" /></a> is small enough.

So the parameters chosen are: 
*number of servers* is **5**, *setup time* is **5**, <a href="https://www.codecogs.com/eqnedit.php?latex=$\lambda=&space;0.35$" target="_blank"><img src="https://latex.codecogs.com/gif.latex?$\lambda=&space;0.35$" title="$\lambda= 0.35$" /></a>, <a href="https://www.codecogs.com/eqnedit.php?latex=$\mu&space;=&space;1$" target="_blank"><img src="https://latex.codecogs.com/gif.latex?$\mu&space;=&space;1$" title="$\mu = 1$" /></a>, <a href="https://www.codecogs.com/eqnedit.php?latex=$T_{end}=20000$" target="_blank"><img src="https://latex.codecogs.com/gif.latex?$T_{end}=20000$" title="$T_{end}=20000$" /></a>, *number of replications* ( **n** ) **=10** .



#### determining a suitable value of T c

For the system with these parameters and <a href="https://www.codecogs.com/eqnedit.php?latex=$T_c&space;=&space;0.1$" target="_blank"><img src="https://latex.codecogs.com/gif.latex?$T_c&space;=&space;0.1$" title="$T_c = 0.1$" /></a>, we infer that the reason of high response time is the low <a href="https://www.codecogs.com/eqnedit.php?latex=$T_c$" target="_blank"><img src="https://latex.codecogs.com/gif.latex?$T_c$" title="$T_c$" /></a> causing the system need to be re-setup frequently. In order to get a improved system, which has lower **mrt**, the <a href="https://www.codecogs.com/eqnedit.php?latex=$T_c$" target="_blank"><img src="https://latex.codecogs.com/gif.latex?$T_c$" title="$T_c$" /></a> need to be higher.

When we use a <a href="https://www.codecogs.com/eqnedit.php?latex=$T_c&space;=&space;1$" target="_blank"><img src="https://latex.codecogs.com/gif.latex?$T_c&space;=&space;1$" title="$T_c = 1$" /></a> system, summarise the data in a table:

 * EMRT = estimated mean response time 


 \ |EMRT System 1(<a href="https://www.codecogs.com/eqnedit.php?latex=$T_c=0.1$" target="_blank"><img src="https://latex.codecogs.com/gif.latex?$T_c=0.1$" title="$T_c=0.1$" /></a>) |EMRT System 2(<a href="https://www.codecogs.com/eqnedit.php?latex=$T_c=1$" target="_blank"><img src="https://latex.codecogs.com/gif.latex?$T_c=1$" title="$T_c=1$" /></a>) |EMRT System 2 - EMRT System 1
-|-|-|-
Rep. 1|6.103755337833227|5.667756688308885|-0.43599864952434153
Rep. 2|6.036903920786047|5.7375017806318835|-0.29940214015416355
Rep. 3|6.01941523556987|5.679789508618821|-0.33962572695104853
Rep. 4|6.059636558900138|5.683994529193845|-0.37564202970629257
Rep. 5|6.1308281500007|5.644545486272564|-0.48628266372813567
Rep. 6|6.062622154824946|5.705916908843001|-0.35670524598194486
Rep. 7|6.061100456436297|5.640056761050419|-0.4210436953858787
Rep. 8|6.0369751961009035|5.723134546912336|-0.3138406491885677
Rep. 9|5.979168710456368|5.690162346478765|-0.28900636397760326
Rep. 10|6.036846181790869|5.668442272176481|-0.36840390961438807

Compute the **95%** confidence interval of for the last column ( difference between 2
systems ) is : 

<div align=center><a href="https://www.codecogs.com/eqnedit.php?latex=[&space;-0.37119130260730415,-0.3659989122351688]" target="_blank"><img src="https://latex.codecogs.com/gif.latex?[&space;-0.37119130260730415,-0.3659989122351688]" title="[ -0.37119130260730415,-0.3659989122351688]" /></a></div>

So we can say System 2 is better than System 1 with probability **95%**.
Our aim is to find a 2 units less than the system with <a href="https://www.codecogs.com/eqnedit.php?latex=$T_c&space;=&space;0.1$" target="_blank"><img src="https://latex.codecogs.com/gif.latex?$T_c&space;=&space;0.1$" title="$T_c = 0.1$" /></a>, so still need to increase <a href="https://www.codecogs.com/eqnedit.php?latex=$T_c$" target="_blank"><img src="https://latex.codecogs.com/gif.latex?$T_c$" title="$T_c$" /></a>.

When <a href="https://www.codecogs.com/eqnedit.php?latex=$T_c&space;=&space;10$" target="_blank"><img src="https://latex.codecogs.com/gif.latex?$T_c&space;=&space;10$" title="$T_c = 10$" /></a>:

\ |EMRT System 1(<a href="https://www.codecogs.com/eqnedit.php?latex=$T_c=0.1$" target="_blank"><img src="https://latex.codecogs.com/gif.latex?$T_c=0.1$" title="$T_c=0.1$" /></a>) |EMRT System 3(<a href="https://www.codecogs.com/eqnedit.php?latex=$T_c=10$" target="_blank"><img src="https://latex.codecogs.com/gif.latex?$T_c=10$" title="$T_c=10$" /></a>) |EMRT System 3 - EMRT System 1
-|-|-|-
Rep. 1|6.103755337833227|4.059404314942124|-2.044351022891103
Rep. 2|6.036903920786047|4.040642601926197|-1.9962613188598501
Rep. 3|6.01941523556987|4.040792035302791|-1.9786232002670792
Rep. 4|6.059636558900138|4.038982217265912|-2.020654341634226
Rep. 5|6.1308281500007|4.053719258290984|-2.077108891709716
Rep. 6|6.062622154824946|4.028697553290952|-2.033924601533994
Rep. 7|6.061100456436297|4.036543042435068|-2.0245574140012295
Rep. 8|6.0369751961009035|4.08661866826957|-1.9503565278313335
Rep. 9|5.979168710456368|4.0869327697588105|-1.8922359406975575
Rep. 10|6.036846181790869|4.033203153386797|-2.0036430284040723

Compute the **95%** confidence interval of for the last column ( difference between 2
systems ) is : 

<div align=center><a href="https://www.codecogs.com/eqnedit.php?latex=[-2.003931854286826,-2.000411403279206]" target="_blank"><img src="https://latex.codecogs.com/gif.latex?[-2.003931854286826,-2.000411403279206]" title="[-2.003931854286826,-2.000411403279206]" /></a></div>

So we can say System 3 is 2 units better than System 1 with probability $95$%.

Still increase <a href="https://www.codecogs.com/eqnedit.php?latex=$T_c$" target="_blank"><img src="https://latex.codecogs.com/gif.latex?$T_c$" title="$T_c$" /></a> up to **20** in case:

\ |EMRT System 1(<a href="https://www.codecogs.com/eqnedit.php?latex=$T_c=0.1$" target="_blank"><img src="https://latex.codecogs.com/gif.latex?$T_c=0.1$" title="$T_c=0.1$" /></a>) |EMRT System 4(<a href="https://www.codecogs.com/eqnedit.php?latex=$T_c=10$" target="_blank"><img src="https://latex.codecogs.com/gif.latex?$T_c=10$" title="$T_c=10$" /></a>) |EMRT System 3 - EMRT System 1
-|-|-|-
Rep. 1|6.103755337833227|3.5659221195190454|-2.5378332183141814
Rep. 2|6.036903920786047|3.5404910115171333|-2.496412909268914
Rep. 3|6.01941523556987|3.517620800474077|-2.5017944350957926
Rep. 4|6.059636558900138|3.586713535421931|-2.472923023478207
Rep. 5|6.1308281500007|3.556310312317443|-2.574517837683257
Rep. 6|6.062622154824946|3.5629866548341043|-2.4996354999908417
Rep. 7|6.061100456436297|3.5756041785043338|-2.4854962779319636
Rep. 8|6.0369751961009035|3.529322491845899|-2.5076527042550043
Rep. 9|5.979168710456368|3.5794976080108256|-2.3996711024455424
Rep. 10|6.036846181790869|3.5413540282355234|-2.495492153555346

Compute the **95%** confidence interval of for the last column ( difference between 2
systems ) is : 

<div align=center><a href="https://www.codecogs.com/eqnedit.php?latex=[-2.4984309802036546,-2.495854852200156]" target="_blank"><img src="https://latex.codecogs.com/gif.latex?[-2.4984309802036546,-2.495854852200156]" title="[-2.4984309802036546,-2.495854852200156]" /></a></div>

System 4 is almost 2.5 units better than System 1 with probability **95%**.

So we can say if our aim is to find a 2 units less than the system with <a href="https://www.codecogs.com/eqnedit.php?latex=$T_c&space;=&space;0.1$" target="_blank"><img src="https://latex.codecogs.com/gif.latex?$T_c&space;=&space;0.1$" title="$T_c = 0.1$" /></a>, **when the system with <a href="https://www.codecogs.com/eqnedit.php?latex=$T_c&space;>&space;10$" target="_blank"><img src="https://latex.codecogs.com/gif.latex?$T_c&space;>&space;10$" title="$T_c > 10$" /></a>, it is improved by 2 units with probability 95%**.



