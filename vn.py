import tabula
import pandas as pd

# Reading specific pages from the PDF
dfs = tabula.read_pdf("MC_Academic_Calendar_2024-25.pdf", pages=[1, 2, 3], columns= [0,1,2],stream=True, lattice=True)

# Combine all data frames into a single data frame
df_combined = pd.concat(dfs) # [1:115] specifies no of rows to be extracted

# Save the filtered DataFrame to an Excel file
df_combined.to_excel("D:/subs/SEM5/Python/BunkCalc/output3.xlsx",index=False)
df_from_xl = pd.read_excel("D:/subs/SEM5/Python/BunkCalc/raw_cal.xlsx", index_col=False)[0:114]
df = pd.DataFrame(df_from_xl)

# print the calender with desired column
df1 = df.iloc[:,0:3] #df remains the same
def is_alpha_or_whitespace(s):
    # Check if all characters in the string are alphabetic or whitespace
    return all(c.isalpha() or c.isspace() for c in s)
tot = 0
col_name = 'B.Tech./\nM.Tech. (Intg.)/\nB.Optom./\nM.Tech./\nM.B.A./ M.C.A./\nM.Optom./\nM.Sc./\nM.Sc. (Intg. IV &\nV Year)'
cias = ['CIA I','CIA II']
for ind in df1.index:
    s = df1[col_name][ind]
    if(type(s) == float):
        pass
    elif (s in cias):
        tot = tot+1
    elif(type(s) == str and is_alpha_or_whitespace(s)):
        pass
    else:
        tot = tot+1
    print(type(s),"\t",s,"\t\t\t\t\t", tot)

print(tot)

# print only the working days
count_day = {'Mon': 0, 'Tue': 0, 'Wed': 0, 'Thu': 0, 'Fri': 0}
cnt = 0
col_name = 'B.Tech./\nM.Tech. (Intg.)/\nB.Optom./\nM.Tech./\nM.B.A./ M.C.A./\nM.Optom./\nM.Sc./\nM.Sc. (Intg. IV &\nV Year)'
for ind in df1.index:
    s = df1['Day'][ind]
    t = df1[col_name][ind]
    if (s in count_day and type(t) != float): # eliminated NaN and only weekdays are seen
        if(type(t) == str and is_alpha_or_whitespace(t) == False):
            count_day[s] += 1
            cnt += 1
        elif(type(t) == int):
            count_day[s] += 1
            cnt += 1 
        print(s,cnt,count_day[s])
    elif(s == 'Sat'):
        k = df1[col_name][ind]
        if (type(k) == str and k not in cias and is_alpha_or_whitespace(k) == False):
            cnt += 1
            count_day[k.split()[2]] += 1
            print(k,cnt,count_day[k.split()[2]])

print(list(count_day.values()))

# get the time table

time_table = 'D:/subs/SEM5/Python/BunkCalc/ICT_5__SEM.pdf'

dftt = tabula.read_pdf(time_table,pages='all',stream = True, lattice = True)

dftt_combined = pd.concat(dftt)

dftt_combined.to_excel('D:/subs/SEM5/Python/BunkCalc/tt.xlsx',index=False)
dftt_from_xl = pd.read_excel("D:/subs/SEM5/Python/BunkCalc/raw.xlsx", index_col=False)
dftt_new = pd.DataFrame(dftt_from_xl)


# get the number of classes in each subject per week
subs_week = {'ECE104':0,'ICT301':0,'ECE211':0, 'CSE314R02':0,'CSE304':0,'CSE304 (SOCLAB4)':0,'CSE315R02':0,'ICT302':0,'CSE304':0,'TNP101R01':0}
classes = 0
for p in range(1,9,1):
    for x in dftt_new.index:
        s = dftt_new[p][x]
        if(s == 'CSE315R02 (SOCLAB3A)\nICT302 (EEELAB1)' and subs_week['CSE315R02'] < 2 and subs_week['ICT302'] < 2):
            subs_week['CSE315R02'] += 1
            subs_week['ICT302'] += 1
            classes += 2

        elif(s in subs_week):
            classes += 1
            subs_week[s] +=1

print(classes)
print(subs_week)

print(count_day, '\n',subs_week)


# count total classes for each year
count = 11
total = 0
temp = 0
week = ['MON','TUE','WED','THU','FRI']
subs = {'ECE104':0,'ICT301':0,'ECE211':0, 'CSE314R02':0,'CSE304':0,'CSE304 (SOCLAB4)':0,'CSE315R02':0,'ICT302':0,'CSE304':0,'TNP101R01':0}

for i, j in dftt_new.iterrows():
    if(i>=1): # itr starts from 1st index ; monday - friday
        data1 = list(j) # i - column number, j : value of the column
        for k in range(count): # traverse through the data1 list : monday timetable
            if(k > 0):
                #print(type(data1[k]))
                if(type(data1[k]) == float or data1[k] == 'LUNCH' or data1[k]=='Minor' or data1[k] == '--'):
                    continue
                if(data1[k] in subs):
                    subs[data1[k]] += count_day[data1[0].capitalize()]
                if(data1[k] == 'CSE315R02 (SOCLAB3A)\nICT302 (EEELAB1)' and temp <2):
                    l = list(p.split())
                    subs[l[0]] += count_day[data1[0].capitalize()]
                    print(subs[l[0]])
                    subs[l[2]] += count_day[data1[0].capitalize()]
                    print(subs[l[2]])
                    temp += 1
                total += count_day[data1[0].capitalize()]
                print(data1[0],data1[k], count_day[data1[0].capitalize()])
                print(total)
        #total = 0
        print()

print(subs)


#

a80 = total*0.80
print(a80)

bunk = total - a80

# get bunks for each period

tot = 0
for i in subs: # i : key
    temp1 = subs[i] # use key to find the value
    print('Total',i,'classes: ',temp1)
    temp80 = temp1*0.80
    print('80% classes =',temp80)
    bunkt = temp1 - temp80
    print('Total classes bunk = ',bunkt)
    tot += bunkt
    print()

print('Overall classes to attend = ',total)
print('Overall Bunks = ',tot)