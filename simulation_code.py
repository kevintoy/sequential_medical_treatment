# -*- coding: utf-8 -*-
"""
Created on Wed Feb 17 01:52:49 2021

@author: kevin
"""

from itertools import product
import pandas

from scipy.stats import norm

method="conformist"
generation=300

mu_1=5; sigma_1=3
mu_2=5; sigma_2=3

s1=5 #patience threshold for T1
s2=10 #patience threshold for T2. If s2 is chance recovery then s2 should be smaller (s1 is larger because people are more patient with a actual treatment)
D=0.2
T1_prop_ini=0.9
def main(mu_2,sigma_1,sigma_2,s1,s2,D,T1_prop_ini):
    def eff_prop(T,prop_T1_first):
        if T=="T1": #return proportion of individuals who think T1 is effective
            return prop_T1_first*norm.cdf(s1,mu_1,sigma_1)+(1-prop_T1_first)*(1-norm.cdf(s2,mu_2,sigma_2))*norm.cdf(s1,mu_1,sigma_1)
        else: #return proportion of individuals who think T2 is effective
            return prop_T1_first*(1-norm.cdf(s1,mu_1,sigma_1))*norm.cdf(s2,mu_2,sigma_2)+(1-prop_T1_first)*norm.cdf(s2,mu_2,sigma_2)
        
    def behavior_prop(T,prop_T1_first):
        if T=="T1":
            total_T1_attempt=prop_T1_first+(1-prop_T1_first)*(1-norm.cdf(s2,mu_2,sigma_2))
            total_T1_T2_attempt=1+prop_T1_first*(1-norm.cdf(s1,mu_1,sigma_1))+(1-prop_T1_first)*(1-norm.cdf(s2,mu_2,sigma_2))
            
            if total_T1_attempt>total_T1_T2_attempt/2: #T1 is the majority behavioral variant
                if (total_T1_attempt+D)/total_T1_T2_attempt>1:
                    return 1
                else:    
                    return (total_T1_attempt+D)/total_T1_T2_attempt
            elif total_T1_attempt<total_T1_T2_attempt/2:
                if (total_T1_attempt-D)/total_T1_T2_attempt<0:
                    return 0
                else:
                    return (total_T1_attempt-D)/total_T1_T2_attempt
            else:
                return (total_T1_attempt)/total_T1_T2_attempt
        


    global prop_T1_first
    prop_T1_first=T1_prop_ini #set up initial condition
    for gen in range(generation):
        print (prop_T1_first)
        if method=="payoff":
            prop_T1_first_raw=eff_prop("T1",prop_T1_first) 
            prop_T2_first_raw=eff_prop("T2",prop_T1_first)
            prop_T1_first_normalized=prop_T1_first_raw/(prop_T1_first_raw+prop_T2_first_raw)
            prop_T1_first=prop_T1_first_normalized
            
        #here, in the next generation,the proportion of individuals who try T1 first is the same as the normalized proportion
        #of individuals in the parental generation who thinks T1 is effective (because there are individuals who think neither treatment is effective.
        #There are other possibilities:
        #conformist transmission, for example, people who attempt T1 first may be higher than the proportion
        #of the relative amount of T1 practiced in the population.
        elif method=="conformist":
            prop_T1_first=behavior_prop("T1",prop_T1_first)
    print ("mu_2=",mu_2, "sigma=",sigma_1, "s=",s2, prop_T1_first)




#for computing analytic results for payoff
mu_2_set=[5,6,7,8,9]
sigma_set=[1,5]
s_set=[2,5,7]
T1_prop_ini_set=[0.1,0.5,0.9]



df = pandas.DataFrame.from_records( list( i for i in product(mu_2_set, sigma_set, s_set ,T1_prop_ini_set  ) ) ,columns=['mu_2', 'sigma', 's','T1_prop_ini'] )

output = []
for i in range(len(df)):
    row_list=list(df.loc[i,:])
    main(float(row_list[0]),float(row_list[1]),float(row_list[1]),float(row_list[2]),float(row_list[2]),D,float(row_list[3]))
    output.append(prop_T1_first)
df["p_equi"]=output
import csv
df.to_csv ("payoff_analytic_result.csv")

#for computing analytic results for conformist
mu_2_set=[5,6,7,8,9]
sigma_set=[1,5]
s_set=[2,4,6]
T1_prop_ini_set=[0.1,0.5,0.9]

df = pandas.DataFrame.from_records( list( i for i in product(mu_2_set, sigma_set, s_set, T1_prop_ini_set ) ) ,columns=['mu_2', 'sigma', 's', 'T1_prop_ini'] )

output = []
for i in range(len(df)):
    row_list=list(df.loc[i,:])
    main(float(row_list[0]),float(row_list[1]),float(row_list[1]),float(row_list[2]),float(row_list[2]), D, float(row_list[3]))
    output.append(prop_T1_first)
df["p_equi"]=output
import csv
df.to_csv ("conformist_analytic_result_D_02.csv")

#for computing analytic results for "get better anyway" effect, in particular when individuals 
#are have higher patience threshold for the ineffective treatment than chance
s2_set=[1,2,3,4,5] # T1 is chance recovery (s1 is set to be 5)
sigma_set=[1,5] 


df = pandas.DataFrame.from_records( list( i for i in product(s2_set, sigma_set) ) ,columns=['s2', 'sigma'] )
output = []

for i in range(len(df)):
    row_list=list(df.loc[i,:])
    main(mu_2,float(row_list[1]),float(row_list[1]),s1,float(row_list[0]), D, T1_prop_ini)
    output.append(prop_T1_first)
df["p_equi"]=output
import csv
df.to_csv ("RTM_analytic_result.csv")

