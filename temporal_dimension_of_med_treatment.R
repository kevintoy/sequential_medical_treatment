raw_data<-read.csv("~/temporal dimension of medical treatment/payoff_analytic_result.csv",fileEncoding="UTF-8-BOM")
raw_data$T1_prop_ini<-factor(raw_data$T1_prop_ini)
#this code is for visualizing the analytic result of payoff transmission

library(ggplot2)
library(directlabels)

  
plot1 <- ggplot(raw_data, aes(x = mu_2, y = p_equi)) +
  geom_point(position=position_dodge(width = 0.0), alpha =1) +
  facet_grid(sigma ~ s,  labeller = label_bquote(cols = s~"="~.(s),rows = sigma ~"="~.(sigma))) + #here, specify the labels of the facet_grid
  theme_grey()+
  labs(x=expression(mu[2]),y="p*",color="Initial T1 proportion")+
  ylim(0,1)+
  theme(axis.text=element_text(size=14),
        axis.title=element_text(size=14))+
  theme(strip.text.x = element_text(size = 12, colour = "black", angle = 0),strip.text.y=element_text(size = 12, colour = "black", angle = 0))
plot1


#this code is for visualizing the analytic result of conformist transmission
raw_data<-read.csv("~/temporal dimension of medical treatment/conformist_analytic_result_D_00.csv",fileEncoding="UTF-8-BOM")
raw_data$T1_prop_ini<-factor(raw_data$T1_prop_ini)

library(ggplot2)
library(directlabels)

plot2 <- ggplot(raw_data, aes(x = mu_2, y = p_equi)) +
  geom_point(position=position_dodge(width = 0.2), alpha =1) +
  facet_grid(sigma ~ s,  labeller = label_bquote(cols = s~"="~.(s),rows = sigma ~"="~.(sigma))) + #here, specify the labels of the facet_grid
  theme_grey()+
  labs(x=expression(mu[2]),y="p*'",color="Initial T1 proportion")+
  ylim(-0.05,1.05)+
  theme(axis.text=element_text(size=14),
        axis.title=element_text(size=14))+
  theme(strip.text.x = element_text(size = 12, colour = "black", angle = 0),strip.text.y=element_text(size = 12, colour = "black", angle = 270))
plot2

#for visualizing the analytic result of RTM
raw_data<-read.csv("~/temporal dimension of medical treatment/RTM_analytic_result.csv",fileEncoding="UTF-8-BOM")
raw_data$sigma<-factor(raw_data$sigma)
library(ggplot2)

plot3 <- ggplot(raw_data, aes(x = s2, y = p_equi, color=sigma))+
  geom_point(position=position_dodge(width = 0.05), alpha =1)+
  theme_grey()+
  labs(x=expression(s[2]),y="equilibrium p",color=expression(sigma))+
  ylim(0,1)+
  theme(axis.text=element_text(size=14),
        axis.title=element_text(size=14))+
  theme(strip.text.x = element_text(size = 12, colour = "black", angle = 0),strip.text.y=element_text(size = 12, colour = "black", angle = 270))
plot3 

#-------visualizing result from agent based simulation----#
raw_data<-read.csv("~/temporal dimension of medical treatment/abc_payoff_result.csv",fileEncoding="UTF-8-BOM")
melted_data<-reshape(raw_data, direction='long', 
                     varying=c('T1_T2', 'T1_none', 'T2_T1', 'T2_none'), 
                     timevar=('var'),
                     times=c('T1_T2','T1_none',"T2_T1","T2_none"),
                     v.names=c('value'),
                     idvar='sbj')

plot3.5 <- ggplot(melted_data, aes(x = mu_2, y = value, color=var)) +
  geom_point(position=position_dodge(width = 0.0), alpha =1) +
  facet_grid(model_num ~ s,  labeller = label_bquote(cols = s~"="~.(s),rows = n ~"="~.(model_num))) + #here, specify the labels of the facet_grid
  theme_grey()+
  labs(x=expression(mu[2]),y="frequency",color="type of individuals")+
  ylim(-0.05,1.05)+
  theme(axis.text=element_text(size=14),
        axis.title=element_text(size=14))+
  theme(strip.text.x = element_text(size = 12, colour = "black", angle = 0),strip.text.y=element_text(size = 12, colour = "black", angle = 270))
plot3.5


#-------visualizing result from agent based simulation with repeats----------#

raw_data<-read.csv("~/temporal dimension of medical treatment/updated_model/abc_auto_conformist_fixed_D_09_summary.csv",fileEncoding="UTF-8-BOM")
melted_data<-reshape(raw_data, direction='long', 
        varying=c('T1_T2_ave', 'T1_T2_std', 'T1_none_ave', 'T1_none_std','T2_T1_ave','T2_T1_std','T2_none_ave','T2_none_std'), 
        timevar=('var'),
        times=c('[T1,T2]','[T1,none]',"[T2,T1]","[T2,none]"),
        v.names=c('avg', 'sd'),
        idvar='sbj')

plot4 <- ggplot(melted_data, aes(x = mu_2, y = avg, color=var)) +
  geom_point(position=position_dodge(width = 0.2), alpha =1) +
  geom_errorbar(aes(ymin=avg-sd, ymax=avg+sd), width=.2,
                position=position_dodge(0.2)) +
  facet_grid(model_num ~ s,  labeller = label_bquote(cols = s~"="~.(s),rows = n ~"="~.(model_num))) + #here, specify the labels of the facet_grid
  theme_grey()+
  labs(x=expression(mu[2]),y="p*",color="type of individuals")+
  ylim(-0.1,1.06)+
  theme(axis.text=element_text(size=14),
        axis.title=element_text(size=14))+
  theme(strip.text.x = element_text(size = 12, colour = "black", angle = 0),strip.text.y=element_text(size = 12, colour = "black", angle = 270))
plot4


