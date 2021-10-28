# -*- coding: utf-8 -*-
"""
Created on Thu Feb 25 02:45:49 2021

@author: kevin
"""

#this is the agent based simulation of the temporal dimension of medical treatment project.

#each agent consists of a list ["first attempt", "second attempt","attribution"]. The second attempt may be empty
#if the agent is not aware of it. "attribution" is which treatment the individual subjective attribute the effec to. It can also be ampty.


from itertools import product
import pandas
import numpy as np
from scipy.stats import norm
import random
N=500 #population size
mu_1=5; sigma_1=1
mu_2=5; sigma_2=1

method="conformist"

s1=7 #patience threshold for T1
s2=7 #patience threshold for T2. If s2 is chance recovery then s2 should be smaller (s1 is larger because people are more patient with a actual treatment)
D=0.0
T1_prop_ini=0.5
generation=100
model_num=9

repeat=200
def ind_freq(agent_type,pop): #the frequency of different types of agents
    if agent_type=="T1_T2":
        return pop.count(["T1","T2"])/N
    if agent_type=="T1_none":
        return pop.count(["T1","none"])/N
    if agent_type=="T2_T1":
        return pop.count(["T2","T1"])/N
    if agent_type=="T2_none":
        return pop.count(["T2","none"])/N

def take_treatment(pop,mu_2,sigma_1,sigma_2,s1,s2): #all individuals in pop performs 
    global pop_behavior
    global pop_attribution
    pop_behavior=[]
    pop_attribution=[]
    for ind in pop: #for each ind, he will sample from a normal distribution for the effect timing
        if ind[0]=="T1":
            pop_behavior.append("T1") 
            #print("T1_appended_first",pop_behavior)
            if np.random.normal(mu_1,sigma_1)<s1: #if the effect takes place within patience threshold
                pop_attribution.append("T1")
            else:#if the effect does not take place within patience threshold, 
                if ind[1]=="T2": #if agent has the alternative treatment in mind, 
                    pop_behavior.append("T2") #he'll attempt it
                    #print("T2_appended_second",pop_behavior)
                    if np.random.normal(mu_2,sigma_2)<s2: #if the second treatment effect timing is within threshold
                        pop_attribution.append("T2") #he'll attribute the effect to T2
                    else: #if the effect timing is above the threshold
                        pop_attribution.append("none") #he'll think neither treatment is effective
                else: #if the agent does not have the alternative treatment in mind
                    pop_attribution.append("none") #he does not attempt it, and think neither works
        elif ind[0]=="T2": #the complete opposite of above
            pop_behavior.append("T2")
            #print("T2_appended_first",pop_behavior)
            if np.random.normal(mu_2,sigma_2)<s2: #if the effect takes place within patience threshold
                pop_attribution.append("T2")
            else:#if the effect does not take place within patience threshold, 
                if ind[1]=="T1": #if agent has the alternative treatment in mind,
                    
                    pop_behavior.append("T1") #he'll attempt it
                    if np.random.normal(mu_1,sigma_1)<s1: #if the second treatment effect timing is within threshold
                        pop_attribution.append("T1") #he'll attribute the effect to T1
                        #print("T1_appended_second",pop_behavior)
                    else: #if the effect timing is above the threshold
                        pop_attribution.append("none") #he'll think neither treatment is effective
                else: #if the agent does not have the alternative treatment in mind
                    pop_attribution.append("none") #he does not attempt it, and think neither works
        if ind[0]=="none": #when the individual has no solution to a problem
            pop_attribution.append("none") #thinks neither works
    #print ("pop_beh_T1=",pop_behavior.count("T1"),"pop_beh_T2=",pop_behavior.count("T2"),"pop_attr_T1=",pop_attribution.count("T1"),"pop_attr_T2=",pop_attribution.count("T2"))

#now we set up the recursion
def main(mu_2,sigma_1,sigma_2,s1,s2,D,T1_prop_ini,model_num):
    pop=[]
    for i in range(N): #set up the initial population
        if i<T1_prop_ini*N:
            pop.append(["T1","T2"])
        else: 
            pop.append(["T2","T1"])
    for gen in range(generation):
        take_treatment(pop,mu_2,sigma_1,sigma_2,s1,s2)
        pop_new=[]
        for i in range(N):
            pop_new.append([[],[]])#create a population of naive individuals
        
        for ind in pop_new:
            if method=="conformist":
                model_list=np.random.choice(pop_behavior,model_num,replace=False)
                if "T1" not in model_list and "T2" in model_list: #all all sampled behaviors are T2
                    ind[0]="T2"
                    ind[1]="none"
                if "T2" not in model_list and "T1" in model_list:
                    ind[0]="T1"
                    ind[1]="none"
                if "T1" in model_list and "T2" in model_list: #both T1 and T2 in the model set
                    if np.count_nonzero(model_list=="T1")>(model_num/(np.count_nonzero(model_list=="T1"))+np.count_nonzero(model_list=="T2"))/2: #if T1 is the more frequent treatment
                        prob_T1_adopt=(np.count_nonzero(model_list=="T1")+D)/(np.count_nonzero(model_list=="T1")+np.count_nonzero(model_list=="T2"))
                        if prob_T1_adopt>random.random(): #with this probability
                            ind[0]="T1"
                            ind[1]="T2"
                        else:
                            ind[0]="T2"
                            ind[1]="T1"
                    else: #if T2 models are more than T1 models
                        prob_T2_adopt=(np.count_nonzero(model_list=="T2")+D)/(np.count_nonzero(model_list=="T1")+np.count_nonzero(model_list=="T2"))
                        if prob_T2_adopt>random.random(): #with this probability
                            ind[0]="T2"
                            ind[1]="T1"
                        else:
                            ind[0]="T1"
                            ind[1]="T2"
            if method=="payoff":
                model_list=np.random.choice(pop_attribution,model_num,replace=False)
                if "T1" not in model_list and "T2" not in model_list:
                    ind[0]="none"
                    ind[1]="none"
                elif "T1" in model_list and "T2" not in model_list:
                    ind[0]="T1"
                    ind[1]="none"
                elif "T2" in model_list and "T1" not in model_list:
                    ind[0]="T2"
                    ind[1]="none"
                else: #both T1 and T2 are in model_list
                    prob_T1_adopt=np.count_nonzero(model_list=="T1")/(np.count_nonzero(model_list=="T1")+np.count_nonzero(model_list=="T2"))
                    if prob_T1_adopt>random.random():
                        ind[0]="T1"
                        ind[1]="T2"
                    else:
                        ind[0]="T2"
                        ind[1]="T1"
                
        pop=pop_new
        global final_T1_T2;global final_T1_none;global final_T2_T1;global final_T2_none
        final_T1_T2=ind_freq("T1_T2",pop)
        final_T1_none=ind_freq("T1_none",pop)
        final_T2_T1=ind_freq("T2_T1",pop)
        final_T2_none=ind_freq("T2_none",pop)
        #print ("T1_T2=",ind_freq("T1_T2",pop),"T1_none=",ind_freq("T1_none",pop),"T2_T1=",ind_freq("T2_T1",pop),"T2_none=",ind_freq("T2_none",pop))

    
mu_2_set=[5,6,7,8,9]
model_num_set=[3,7]
s_set=[2,5,7]

df_T1_T2=pandas.DataFrame.from_records( list( i for i in product(mu_2_set, model_num_set, s_set  ) ) ,columns=['mu_2', 'model_num', 's'] )
df_T1_none=pandas.DataFrame.from_records( list( i for i in product(mu_2_set, model_num_set, s_set  ) ) ,columns=['mu_2', 'model_num', 's'] )
df_T2_T1=pandas.DataFrame.from_records( list( i for i in product(mu_2_set, model_num_set, s_set  ) ) ,columns=['mu_2', 'model_num', 's'] )
df_T2_none=pandas.DataFrame.from_records( list( i for i in product(mu_2_set, model_num_set, s_set  ) ) ,columns=['mu_2', 'model_num', 's'] )

for re in range(repeat):
    print ("repeat=", re)
    output_T1_T2=[]
    output_T1_none=[]
    output_T2_T1=[]
    output_T2_none=[]
    
    for i in range(len(df_T1_T2)):
        print ("repeat=", re, "run=", i)
        row_list=list(df_T1_T2.loc[i,:])
        main(row_list[0],sigma_1,sigma_2,(row_list[2]),(row_list[2]),D,T1_prop_ini,int(row_list[1]))
        output_T1_T2.append(final_T1_T2)
        output_T1_none.append(final_T1_none)
        output_T2_T1.append(final_T2_T1)
        output_T2_none.append(final_T2_none)
    df_T1_T2["T1_T2_"+str(re)]=output_T1_T2
    df_T1_none["T1_none_"+str(re)]=output_T1_none
    df_T2_T1["T2_T1_"+str(re)]=output_T2_T1
    df_T2_none["T2_none_"+str(re)]=output_T2_none

#automatically computes 
T1_T2_ave=df_T1_T2.iloc[:,3:repeat+5].mean(axis=1)
T1_T2_std=df_T1_T2.iloc[:,3:repeat+5].std(axis=1)
T1_none_ave=df_T1_none.iloc[:,3:repeat+5].mean(axis=1)
T1_none_std=df_T1_none.iloc[:,3:repeat+5].std(axis=1)
T2_T1_ave=df_T2_T1.iloc[:,3:repeat+5].mean(axis=1)
T2_T1_std=df_T2_T1.iloc[:,3:repeat+5].std(axis=1)
T2_none_ave=df_T2_none.iloc[:,3:repeat+5].mean(axis=1)
T2_none_std=df_T2_none.iloc[:,3:repeat+5].std(axis=1)

df_summary=pandas.DataFrame.from_records( list( i for i in product(mu_2_set, model_num_set, s_set  ) ) ,columns=['mu_2', 'model_num', 's'] )
df_summary["T1_T2_ave"]=T1_T2_ave
df_summary["T1_T2_std"]=T1_T2_std
df_summary["T1_none_ave"]=T1_none_ave
df_summary["T1_none_std"]=T1_none_std
df_summary["T2_T1_ave"]=T2_T1_ave
df_summary["T2_T1_std"]=T2_T1_std
df_summary["T2_none_ave"]=T2_none_ave
df_summary["T2_none_std"]=T2_none_std

import csv
df_summary.to_csv ("abc_auto_conformist_fixed_D00_summary.csv")
