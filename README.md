# GEIRINA_EV_Project_June_2020
 project files
1. References:
Includes three parts:
(1) DP Models
(2) Time series prediction
(3) EV demand prediction

2. Program Code
-> Data_crawiling
    : crawl the basic information and historical visits of EV charging station in the state of Utah_location_id

-> address_to_coordinates
    : Transform the EV locations' address to coordinates

-> basic_info_txt_to_csv_file
    : process the text file, extract info from it and transform to csv files

-> Historical_visit_to_time_matrix_csv
    : process the text file (historical visit) to extract the visit_time-station ID A_matrix

-> AP_Cluster
    : A toy example to show how to conduct AP Cluster algorithm

-> ARIMA_toy_example
    : As name suggested.


3. Data
-> UTAH.rar: Include the raw basic information and historical visit text files for each charging station.

-> Basic_Info_utah.csv : Include the basic information for each charging station. (extracted from the txt file)

-> Date_matrix_utah.csv: Time series-station ID Matrix

-> coordinates.txt: [address, lat, lon] for each charging station

-> Basic_Info_utah_2.csv: An extended form based on Basic Info Utah. Coordinates, number of historical visits for each charging station are added. There are three additional sheets (Time_trend, Time_ID_Matrix, ID_trend).
