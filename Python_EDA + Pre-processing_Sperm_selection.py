#Importing necessary libraries:
import pandas as pd
import numpy as np

#Reading the CSV file through pandas:
icsi_df = pd.read_csv("C:\\360DIGITmg\\Project 1\\Dataset\\Sperm_Selection_Dataset_DA_only_icsi.csv")

#Drawing data insights:
icsi_df.info()   #Gives the basic information of the dataset.
icsi_df.isnull().sum()  #Gives nulls if any and summing them up by column wise.

#Checking correlation between variables
df_corr = icsi_df.corr(numeric_only = True)


''' Insights drawn from the given code are:
    1 - Datatype - Of all the 25 columns only Selection_Date column type is object 
    which is incorrect, and is to be changed to Date type.
    2 - Formatting - In embryologist_id and patient_id there is formatting issue.
    3 - Typing error - In motility_pattern column, typing error identified.
    4 - Missing values - Out of 25 columns, 6 columns have missing or NAN values.
    5 - Duplicates - Found 18 duplicates in patient-oocyte-date.
    6 - Error - Some error entries in day3_grade, despite no fertilization there are some values existing.'''


'''Drawing Statistical Insights of the given dataset.'''
''' 1st moment business decision: '''
# Mean
mean = icsi_df.mean(numeric_only = True)

# Median
median = icsi_df.median(numeric_only = True)

# Mode
mode = icsi_df.mode(numeric_only = False) #####

'''2nd moment business decision: '''
# Variance
var = icsi_df.var(numeric_only = True)

# Standard Deviation
std = icsi_df.std(numeric_only = True)

# Range
numeric_icsi = icsi_df.select_dtypes(include = 'number')
range_icsi = numeric_icsi.max() - numeric_icsi.min()

'''3rd & 4th moment business decision: '''
# Skewness
skew = numeric_icsi.skew()

#Kurtosis
kurt = numeric_icsi.kurtosis()

# Representing this in table format:
moment_4 = pd.DataFrame({
    'skewness': numeric_icsi.skew(),
    'kurtosis': numeric_icsi.kurtosis()
    })

#-------------------------------------------------------------------------------------------------------#

#Data Cleaning/Data Preparation/Data Munging or Wrangling:
#Changing the datatype:
icsi_df['Selection_Date'] = pd.to_datetime(icsi_df['Selection_Date'])
icsi_df.info()

#Fixing formatting issues
icsi_df['Embryologist_ID'].unique()
icsi_df['Embryologist_ID'] = icsi_df['Embryologist_ID'].str.replace('EMBA','EMB_A')
icsi_df['Embryologist_ID'].unique()

#Fixing formatting issues in pateint_id column
icsi_df['Patient_ID'] = icsi_df['Patient_ID'].str.replace(r'^P-','PT-', regex = True)

#Rectifying typo
icsi_df['Motility_Pattern'].value_counts()
icsi_df['Motility_Pattern'] = icsi_df['Motility_Pattern'].str.replace('Progresive','Progressive')

#-------------------------------------------------------------------------------------------------------#
###  Treating Duplicates:

#Creating the subset for these 3 columns for duplicates
subset_cols = ['Patient_ID','Oocyte_ID','Selection_Date']

#Identifying duplicates
duplicate_mask = icsi_df.duplicated(subset = subset_cols, keep= False)
duplicates_df = icsi_df[duplicate_mask].sort_values(by= subset_cols)

#Dropping the duplicates
icsi_df.drop_duplicates(subset = subset_cols, keep = 'first', inplace = True)
final_Shape = icsi_df.shape

#-------------------------------------------------------------------------------------------------------#
###  Treating Missing values:
'''We have 6 colunms in total with missing values. 1 numerical & 5 categorical'''


icsi_df.loc[icsi_df['Fertilization_Success'] == 0,'Day3_Grade'] = 0 
'''Rectified some errors, where fertilization_success was 0 but day3_grade showed some values. And 
treated the missing values of Day3_grade with 0'''
icsi_df.isnull().sum()

#Treating missing values for categorical values by mode imputer and constant 
icsi_df['Day5_Blastocyst_Grade'] = icsi_df['Day5_Blastocyst_Grade'].fillna('Not_Reached')
icsi_df.isnull().sum()
'''Here, we treated missing values of column "Day5_Blastocyst_Grade" which had 830 missing values around
60% missing values, by using Numpy's .fillna feature by filling with not_reached as most fertilization
success was 0, so leading to not_reached conclusion.'''

icsi_df['Vacuoles_Present'] = icsi_df['Vacuoles_Present'].fillna('Unknown')
icsi_df.isnull().sum()
'''Here, vacuoles_present column had 289 missing values. As it is a categorical column, it can be either treated
with MODE or Constant/Fillna. Treating it with mode would be biased as we had too many missing values. So treated
it with Fillna.'''

#Importing necessary library
from sklearn.impute import SimpleImputer

mode_imputer = SimpleImputer(strategy= 'most_frequent')
cols_to_impute = ['Midpiece_Assessment','Tail_Assessment','Magnification_Used']
icsi_df[cols_to_impute] = mode_imputer.fit_transform(icsi_df[cols_to_impute])
icsi_df.isnull().sum()
'''Here, treating 3 categorical columns altogether using sklearn imputing mode method.'''

#-------------------------------------------------------------------------------------------------------#
### Outlier Analysis:
#Importing neccessary libraries
import seaborn as sns
import matplotlib.pyplot as plt

#Detecting outliers for dataset through creating seperate boxplots of every column:
plt.figure(figsize=(20,15))
for i in range(len(icsi_df.columns)):
    plt.subplot(3,5, i+1)
    sns.boxplot(y= icsi_df.columns[i], data=icsi_df)
    plt.title(icsi_df.columns[i])
plt.tight_layout()
plt.show()

#Checking the skewness of the data for further analysis
print(icsi_df.skew(numeric_only = True))

'''Upon running the boxplot for outlier, we analysed that there are 4 columns which contain 
outliers. Sperm_Concentration_M_per_ml consisting the heavy outliers as it has skewness with 4.01
and Selection_Time_Seconds, Progressive_Motility_Percent & Normal_Morphology_Percent consist of low-moderate outliers.'''

#Outlier treatment for Sperm_concentration column:
#Checking outliers before winsorization
sns.boxplot(x=icsi_df['Sperm_Concentration_M_per_ml'])
plt.title('Checking for outlier before treatment')
plt.show()

#Applying winsorization with IQR as capping method:
from feature_engine.outliers import Winsorizer

winsor = Winsorizer(capping_method = 'iqr',
                    tail = 'both',
                    fold = 1.5,
                    variables = ['Sperm_Concentration_M_per_ml'])

icsi_df[['Sperm_Concentration_M_per_ml']] = winsor.fit_transform(icsi_df[['Sperm_Concentration_M_per_ml']])

icsi_df['Sperm_Concentration_M_per_ml'].max() #39.36
#icsidf_s['Sperm_Concentration_M_per_ml'].max()  #39.36

#Checking outliers after winsorization
sns.boxplot(x=icsi_df['Sperm_Concentration_M_per_ml'])
plt.title('Checking for outlier after treatment')
plt.show()

#Outlier treatment for Selection_Time_Seconds column:
'''Reason we are treating this column is because expected range for selection time is 60-300(in seconds) but 
Some values are <45 seconds (too fast). So in order to treat them we will again use winsorization with IQR method.'''


winsor_3 = Winsorizer(capping_method = 'iqr',
                    tail = 'left',  #We are only treating left tail, which has outlier. right tail is in the range 
                    fold = 1.5,
                    variables = ['Selection_Time_Seconds'])

icsi_df[['Selection_Time_Seconds']] = winsor_3.fit_transform(icsi_df[['Selection_Time_Seconds']])

icsi_df['Selection_Time_Seconds'].min() #45
#icsidf_o['Selection_Time_Seconds'].min() #45

#Checking for column after treatment:
sns.boxplot(x=icsi_df['Selection_Time_Seconds'])
plt.title('Checking for outlier before treatment')
plt.show()
'''The plot is showing outlier on the right tail but as the values are in range, i chose not to treat those as it might
hamper valuable information.'''

#Final output check:
plt.figure(figsize=(20,15))
for i in range(len(icsi_df.columns)):
    plt.subplot(3,5, i+1)
    sns.boxplot(y= icsi_df.columns[i], data=icsi_df)
    plt.title(icsi_df.columns[i])
plt.tight_layout()
plt.show()

#-------------------------------------------------------------------------------------------------------#
###  Discretization
'''Discretization is the process of converting continuous numerical data into discrete categories, bins or interval.
Here, we are discretizing 3 columns - Sperm_concentration, selection_time & embryologist_experience.'''

icsi_df['Concentration_category'] = pd.cut(icsi_df['Sperm_Concentration_M_per_ml'],
                                           bins=[0,15,30,40],
                                           labels= ['Low','Normal','High'],
                                           include_lowest= True)
## Here we are binning the values into 3 category 0-15 = low, 15-30 = normal & 30-40 = high. As we have capped the outliers our highest value is 39.36 which comes under 40.



icsi_df['Selection_category'] = pd.cut(icsi_df['Selection_Time_Seconds'],
                                       bins= [0,60,180,300],
                                       labels= ['Too fast','Optimal','Slow'],
                                       include_lowest= True)

icsi_df['Experience_level'] = pd.cut(icsi_df['Embryologist_Experience_Years'],
                                     bins= [0,5,10,20],
                                     labels= ['Junior','Intermediate','Senior'],
                                     include_lowest= True)

#-------------------------------------------------------------------------------------------------------#
###  Re-arranging the columns:
arranged_cols = [
    'Record_ID','Selection_Date','Patient_ID','Oocyte_ID','Cycle_Number',
    'Embryologist_ID','Embryologist_Experience_Years','Experience_level',
    'Sperm_Concentration_M_per_ml','Concentration_category',
    'Total_Motility_Percent','Progressive_Motility_Percent','Normal_Morphology_Percent',
    'Selection_Time_Seconds','Selection_category','Microscope_Type','Magnification_Used',
    'Lab_Temperature_C','Lab_Humidity_Percent','Fertilization_Success','Day3_Grade',
    'Day5_Blastocyst_Grade','Usable_Embryo','Head_Shape_Score','Acrosome_Status',
    'Midpiece_Assessment','Tail_Assessment','Motility_Pattern','Vacuoles_Present']

icsi_df = icsi_df[arranged_cols]

#-------------------------------------------------------------------------------------------------------#

### Downloaded the pre-processed data as a CSV file
icsi_df.to_csv(r'C:\\360DIGITmg\\Project 1\\EDA\\Pre-processed_sperm_data.csv', index = False)

#-------------------------------------------------------------------------------------------------------#











