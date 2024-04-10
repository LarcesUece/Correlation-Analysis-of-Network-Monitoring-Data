# Code and dataset repository.

# Folder descriptions

- The "codes" folder contains the codes used for collecting and processing the data collected from RNP.

- The "datasets" folder contains the datasets collected so far within a 6-month interval, including throughput, traceroute and delay.

- In the "processed datasets" folder are the data generated after filtering and processing the data contained in the "datasets" folder.

- The "correlation" folder contains the codes developed to handle the matrices created after data collection. There are also folders for good and bad results, which represent high (considered bad) and low (considered good) delay.

# Basic execution guide

## Data collection to initial data processing.
### First step:
- Begin by running the code named 'data_collector.py' in the 'codes' folder.
  
*Note: Due to instabilities, data collection may stop, requiring a restart from where it left off. To resume, simply edit within the loop at the end of the code, updating the last number displayed on the screen.*

### Second step:
With the collected data, you should perform filtering to separate high latency or low throughput (if applicable).
- Then, run the code 'high delay filtering - low flow.py' located in the 'codes' folder. It will create a new set of datasets containing only high latencies or low throughputs.
  
*Note: You should edit the comments in the code to choose whether you want to filter by latency or throughput.*

### Third step:
- Run the code 'select all delay - traceroute - matrix.py'. This code will generate the matrices that will be used for correlation, which can be found in the 'correlation' folder.
  
*Note: You should edit the comments in the code to choose whether you want to filter by latency.*

## Correlation

### First step:
- First you'll need to enter the "correlation" directory and then enter the "Codes" subdirectory. Finally, start by filling the 'datasets' subdirectory with the desired .csv datasets. 

*Note: We used the datasets in the 'processed datasets' directory for the tests and two of them will be used as an exemple following the next steps.*

### Second step:
- You'll need to run 'pip3 install -r requirements.txt' to make sure all the necessary python packages are installed in your environment.

### Third step:
- Give the correlation script 'correlation_script.sh' permission in your environment by running 'chmod +x correlation_script.sh' and then run the script using './correlation_script.sh'. It will give you feedback as the code is creating the new directorys with Correlation Matrices, Heatmaps and Graphics for the Performance Score.

*Note: The code will only work if the "Codes/datasets" subdirectory is filled with datasets with the same base name as the ones used in example and in the "processed datasets" directory.*
