# created by Yang Meng

# read in percentile number


import os.path
if not os.path.exists("./output"): os.makedirs("./output")
input1 = "./input/itcont.txt"
input2 = "./input/percentile.txt"
output1 = "./output/repeat_donors.txt"

with open(input2,'r') as file:
    percentile_read = file.readline()

percentile = int(percentile_read)


all_donors = {}
all_distinct_records = {}
count = 0

sequence = 0
total_amount = 0


with open(input1,'r') as file:
    for line in file:
        line = line.strip().split('|')
        sequence += 1
        CMTE_ID = line[0]
        NAME = line[7]
        ZIP_CODE = line[10][:5]
        TRANSACTION_DT = line[13][-4:]
        TRANSACTION_AMT = line[14]
        OTHER_ID = line[15]

        if(len(OTHER_ID) == 0):

            if((NAME, ZIP_CODE) in all_donors):
                all_distinct_records[(CMTE_ID, NAME, ZIP_CODE)] = [CMTE_ID, NAME, ZIP_CODE, TRANSACTION_DT, TRANSACTION_AMT, sequence]

            else:
                all_donors[(NAME, ZIP_CODE)] = [CMTE_ID]

distinct_donation_list = []
for val in all_distinct_records.values():
    distinct_donation_list.append(val)

distinct_donation_list = sorted(distinct_donation_list, key = lambda x:x[5])


def cal_percentile(all_amount, percentile):
    all_amount = sorted(all_amount)
    percentile_seq = round((1+len(all_amount)) * percentile * 0.01)
    return all_amount[percentile_seq-1]


client_dict = {}
file = open(output1,"w")

for records in distinct_donation_list:
    records_key = (records[0], records[2], records[3])
    if(records_key in client_dict):
        client_dict[records_key][0].append(int(records[4]))
        client_dict[records_key][1]+=1

    else:
        client_dict[records_key] = [[int(records[4])],1]

    percentile_amount = cal_percentile(client_dict[records_key][0], percentile)
    total_amount = sum(client_dict[records_key][0])
    file.write(records[0]+'|'+ records[2]+'|'+ records[3]+'|'+str(percentile_amount)+'|'+str(total_amount)+'|'+str(client_dict[records_key][1]) +"\n")

file.close()
