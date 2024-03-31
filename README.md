# Correlation Analysis of Network Monitoring Data

Made by the Laboratory of Computer Networks and Security of Universidade Estadual do Ceará (LARCES/UECE).
## Proposal summary

Currently, several companies and Internet Service Providers (ISPs) offer network monitoring services that encompass regular performance assessments, with the main focus on delivering crucial information about the current state of the network infrastructure and consequently the services running on it. However, these monitoring tools require continuous development to incorporate more complex tasks, such as performance issue detection. Within this context, this article introduces a mechanism for identifying high latencies and network communication links that may be the cause of these performance issues, utilizing an Impact Score formulated considering temporal aspects. This Score is based on data correlation techniques applied to information collected by monitoring tools. Experiments conducted with real data from RNP demonstrate the effectiveness of the proposed mechanism in identifying network links that impact data communication, resulting in high end-to-end latencies.

## Description Project

The proposed mechanism for identifying causes of delays in network infrastructures requires two pieces of information: end-to-end latency and the set of links used in communication. It performs activities such as data collection, identification of cases of high and low latency, generation of correlation matrices, and calculation of the Impact Score. After organizing the data, correlation matrices are calculated for cases of high and low latency, followed by the calculation of the Impact Index of a link. This approach allows for assessing the impact of links in different latency scenarios, aiding in the identification of potential causes of network underperformance.

## Technologies used:

- [Git](https://github.com/LarcesUece/Correlation-Analysis-of-Network-Monitoring-Data/tree/develop) - Git is a free and open source distributed version control system designed to handle everything from small to very large projects with speed and efficiency.
- [Python](https://www.python.org/) - Open source programming language.

## Participants:

### Project Coordinator:

- Rafael Lopes [Curriculum Lattes](http://lattes.cnpq.br/5212299313885086)

### Members:

- Francisco Valderlan Jorge Nobre [Curriculum Lattes](http://lattes.cnpq.br/8242344331454843)
- Danielle dos Santos Silva [Curriculum Lattes](https://lattes.cnpq.br/5639924024679664)
- Maria Clara Mesquita Moura Ferreira [Curriculum Lattes](http://lattes.cnpq.br/3456660001349261)
- Silvio Eduardo Sales de Britto R. [Curriculum Lattes](http://lattes.cnpq.br/7251244319067731)

