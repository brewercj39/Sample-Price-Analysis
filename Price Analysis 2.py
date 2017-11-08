#Corey Brewer Sample Price Analysis
#11/7/17

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import math

#import the csv file (First I saved the file into the same
#directory as this python script
xl = pd.ExcelFile('Price_Data_Corey_Edited1.xlsx')

df = xl.parse(0)
print(df.head())

#find out the unique currencies
print(df['CCY'].unique())
#AUSUSD USDJPY USDINR

# Need a stated index column for the regression
df['Index'] = df.index
print(df.head())

#group by currency
audusd_df = df.groupby(['CCY']).get_group('AUDUSD')
usdjpy_df = df.groupby(['CCY']).get_group('USDJPY')
usdinr_df = df.groupby(['CCY']).get_group('USDINR')

#Since I can tell there are missing values,
# and each set is a line, I
# can use linear regression to fill in the NaNs
#Need to also ignore Nans during polyfit

id1 = np.isfinite(audusd_df['Index']) & np.isfinite(audusd_df['Price'])
regaudusd = np.polyfit(audusd_df['Index'][id1], audusd_df['Price'][id1], 1)

id2 = np.isfinite(usdjpy_df['Index']) & np.isfinite(usdjpy_df['Price'])
regusdjpy = np.polyfit(usdjpy_df['Index'][id2], usdjpy_df['Price'][id2], 1)

id3 = np.isfinite(usdinr_df['Index']) & np.isfinite(usdinr_df['Price'])
regusdinr = np.polyfit(usdinr_df['Index'][id3], usdinr_df['Price'][id3], 1)

#replace all NaNs with 0s
audusd_df = audusd_df.fillna(0.0)
usdjpy_df = usdjpy_df.fillna(0.0)
usdinr_df = usdinr_df.fillna(0.0)

print(regaudusd)

print(audusd_df.head())
#Now I fill in the missing points... Note selecting with .at....
# all other methods yielded errors(loc, iloc, ix)
for ind in audusd_df['Index']:
    if audusd_df.at[ind, 'Price'] == 0:
        audusd_df.at[ind, 'Price'] = regaudusd[0] * ind + regaudusd[1]

for ind in usdjpy_df['Index']:
    if usdjpy_df.at[ind, 'Price'] == 0:
        usdjpy_df.at[ind, 'Price'] = regusdjpy[0] * ind + regusdjpy[1]

for ind in usdinr_df['Index']:
    if usdinr_df.at[ind, 'Price'] == 0:
        usdinr_df.at[ind, 'Price'] = regusdinr[0] * ind + regusdinr[1]

#create plot
plt.plot(audusd_df['Date'], audusd_df['Price'], 'r--',
         usdjpy_df['Date'], usdjpy_df['Price'], 'bs',
         usdinr_df['Date'], usdinr_df['Price'], 'g^')
plt.title('Currency Converion Rate')
plt.xlabel('Date')
plt.ylabel('Price')
plt.legend(('AUDUSD', 'USDJPY', 'USDINR'))

plt.show()