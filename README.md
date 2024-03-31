# Code and dataset repository.

# Folder descriptions

- The "codes" folder contains the codes used for collecting and processing the data collected from RNP.

- The "datasets" folder contains the datasets collected so far within a 6-month interval, including throughput, traceroute and delay.

- In the "processed datasets" folder are the data generated after filtering and processing the data contained in the "datasets" folder.

- The "correlation" folder ...

# Basic execution guide

## Collecting data
### First step:
- Begin by running the code named 'data_collector.py' in the 'codes' folder.
- 
*Note: Due to instabilities, data collection may stop, requiring a restart from where it left off. To resume, simply edit within the loop at the end of the code, updating the last number displayed on the screen.*

### Second step:
With the collected data, you should perform filtering to separate high latency or low throughput (if applicable).
- Then, run the code 'high delay filtering - low flow.py' located in the 'codes' folder. It will create a new set of datasets containing only high latencies or low throughputs.
  
*Note: You should edit the comments in the code to choose whether you want to filter by latency or throughput.*

### Third step:
- Run the code 'select all delay - traceroute - matrix.py'. This code will generate the matrices that will be used for correlation, which can be found in the 'correlation' folder.
  
*Note: You should edit the comments in the code to choose whether you want to filter by latency.*

### Fourth step:
- 
