# GEIRINA_EV_Project_June_2020
 project files
1. References:
Includes three parts:
(1) DP Models
(2) Time series prediction
(3) EV demand prediction

2. Program Data
-> Data_crawiling \n
    : crawl the basic information and historical visits of EV charging station in the state of Utah_location_id \n
-> address_to_coordinates \n
    : Transform the EV locations' address to coordinates \n
-> basic_info_txt_to_csv_file \n
    : process the text file, extract info from it and transform to csv files
-> Historical_visit_to_time_matrix_csv
    : process the text file (historical visit) to extract the visit_time-station ID A_matrix
-> AP_Cluster
    : A toy example to show how to conduct AP Cluster algorithm
-> ARIMA_toy_example
    : As name suggested.
