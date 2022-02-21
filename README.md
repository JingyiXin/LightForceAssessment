# LightForceAssessment
This short exercise uses a database library and tabulates and returns a list of items that must be printed today in order to ship on time.

### Requirements for Virtual Environment
First, a virtual environment must be setup. To do this, create a virtual environment on the command line inside of the repository folder. Install the necessary modules using the command ```pip install -r requirements.txt```.
### Data Processing
In order to input data, change line 177 to import a new csv file to process the data into the cloud database. Line 181 can be changed to the desired latest print time. The output file "to_print.csv" should then contain a list of all products that must be printed.
