import pandas as pd
df = pd.read_csv('fintech_output_most_updated.csv')
df1 = df.drop(columns=['Unnamed: 0'])
df1 = df1[df1['Company MSA'].isin(['San Francisco, CA','San Jose, CA','Boston, MA-NH','New York, NY','Chicago, IL','San Diego, CA','Los Angeles-Long Beach, CA','Washington, DC-MD-VA-WV','Seattle-Bellevue-Everett, WA','Dallas, TX'])]
df2 = df1.groupby(['Company MSA','Year'])['CPI Adjusted Round Amount'].sum()

df1['Round Date'] = pd.to_datetime(df1['Round Date'])
df1['Year'] = df1['Round Date'].dt.year
df1 = df.drop(columns=['Unnamed: 0', 'First', 'Common'])
df1.loc[(df1['Fintech'] == True), 'Industry'] = 'Fintech'
df1.loc[(df1['Fintech'] == False) & (df1['Company Industry Class'] == 'Medical/Health/Life Science'), 'Industry'] = "Healthcare"
df1.loc[(df1['Fintech'] == False) & (df1['Company Industry Class'] == 'Information Technology'), 'Industry'] = "Information Technology"
df1.loc[(df1['Fintech'] == False) & (df1['Company Industry Class'] != 'Information Technology') & (df1['Company Industry Class'] != 'Medical/Health/Life Science'), 'Industry'] = "Others"

df2.to_csv("amt.csv")
