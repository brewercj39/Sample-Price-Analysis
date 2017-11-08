#Corey Brewer Sample Price Analysis
#11/7/17

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

#import the csv file (First I saved the file into the same
#directory as this python script
xl = pd.ExcelFile('Price_Data_Corey.xlsx')

df = xl.parse(0)
print(df.head())

#find out the unique currencies
print(df['CCY'].unique())
#AUSUSD USDJPY USDINR

#group by currency
audusd_df = df.groupby(['CCY']).get_group('AUDUSD')
usdjpy_df = df.groupby(['CCY']).get_group('USDJPY')
usdinr_df = df.groupby(['CCY']).get_group('USDINR')

#create plot
plt.plot(audusd_df['Date'], audusd_df['Price'], 'r--',
         usdjpy_df['Date'], usdjpy_df['Price'], 'bs',
         usdinr_df['Date'], usdinr_df['Price'], 'g^')
plt.title('Currency Converion Rate')
plt.xlabel('Date')
plt.ylabel('Price')
plt.legend(('AUDUSD', 'USDJPY', 'USDINR'))

plt.show()