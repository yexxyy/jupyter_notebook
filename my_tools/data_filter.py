import datetime
import csv

read_file_path = '/Users/yetongxue/Downloads/0089.csv'
statistic_file_path = '/Users/yetongxue/Downloads/统计.csv'
statistic_column_names = ['Test_Items', 'Upper Limit', 'Lower Limit', 'Upper_Limit_NG', 'Lower_Limit_NG']
ng_detail_file_path = '/Users/yetongxue/Downloads/不良记录.csv'
start = '2020/2/10 01:03'
end = '2020/2/13 01:03'
time_fmt = '%Y/%m/%d %H:%M'
config = 'E2T'

start_time = datetime.datetime.strptime(start, time_fmt)
end_time = datetime.datetime.strptime(end, time_fmt)

upper_limts = []  # 记录表格第一行数据
lower_limts = []  # 记录表格第二行数据
column_names = []  # 记录表格第三行数据
upper_ng_dict = {}  # 统计检测项目超过上限数量
lower_ng_dict = {}  # 统计检测项目超过下限数量
name_limit_map_upper = {}  # 检测项目名称与上限值对应关系
name_limit_map_lower = {}  # 检测项目名称与下限值对应关系
total_input = 0  # 记录符合条件（start_time, end_time, config）的输入记录条数
ng_count = 0  # Test Pass/Fail Status == FAIL

read_f = open(read_file_path, 'r')
reader = csv.reader(read_f)
read_f.close()

ng_write_f = open(ng_detail_file_path, 'a+')
ng_writer = csv.writer(ng_write_f)

for i, line in enumerate(reader):
    # i 代表第几行，line 代表csv文件的一行数据，整个for循环会遍历所有数据
    if i == 0:
        upper_limts = line
    elif i == 1:
        lower_limts = line
    elif i == 2:
        column_names = line
        for name_index, name in enumerate(column_names):
            name_limit_map_upper.update({name: upper_limts[name_index]})
            name_limit_map_lower.update({name: lower_limts[name_index]})

    else:
        # line 输出内容样例如下（数组）：
        """
        ['2020/2/12 03:40', '2020/2/12 03:57', 'PASS', '4NITS_LL LL red_crush;MP9 DMX2_Result', 'GVH0065000WLQHM7Q+P2E29Y7D003AA7CU1E2T+FXR9487ALUAPFF...', 'GVH007100LRLQHM74', '12134.7312', '0.049812', '0.151119', '0.454217', '0.241179', '0.322182', '0.042581', '6499.568021', '0.004699', '0.200551', '0.465467', '0.313588', '0.323475', '0.108588', '6411.441216', '0.00443', '0.201206', '0.466196', '0.315035', '0.111495', '0.324418', '6507.934901', '0.00436', '0.200224', '0.465688', '0.313376', '0.323938', '0.112509', '6810.07131
        """
        line_start = datetime.datetime.strptime(line[0], time_fmt)
        line_end = datetime.datetime.strptime(line[1], time_fmt)
        LCM_FULL_SN = line[4]  # GVH0065000WLQHM7Q+P2E29Y7D003AA7CU1E2T+FXR9487A.....
        LCM_FULL_SN_arr = LCM_FULL_SN.split('+')  # [GVH0065000WLQHM7Q, P2E29Y7D003AA7CU1E2T, FXR9487A...]
        if line_start > start_time and line_end < end_time and LCM_FULL_SN_arr[1][-3:] == config:
            total_input += 1
            if line[2] == 'FAIL':
                ng_count += 1

            ng_items = []
            for index, column_name in enumerate(column_names):
                if index < 6:
                    # 前6列分别是StartTime, EndTime, Test Pass/Fail Status, List of Failing Tests, LCM_FULL_SN, SerialNumber，所以略过
                    continue

                # 统计超过上下限的项目
                ok = True
                try:
                    if float(upper_limts[index]) < float(line[index]):
                        upper_ng_dict.update(
                            {column_names[index]: upper_ng_dict.get(column_names[index], 0) + 1})
                        ok = False
                except:
                    pass
                # 统计超过下限的项目
                try:
                    if float(lower_limts[index]) > float(line[index]):
                        lower_ng_dict.update(
                            {column_names[index]: lower_ng_dict.get(column_names[index], 0) + 1})
                        ok = False
                except:
                    pass

                if ok == False:
                    ng_items.append('{}:{}'.format(column_name, line[index]))

        if ng_items:
            ng_writer.write_row([line[5], ';'.join(ng_items)])

out_data = []
for name in column_names:
    if upper_ng_dict.get(name) or lower_ng_dict.get(name):
        out_data.append(
            '{},{},{},{},{}'.format(name, name_limit_map_upper.get(name), name_limit_map_lower.get(name),
                                    upper_ng_dict.get(name, 0), lower_ng_dict.get(name, 0)))

with open(statistic_column_names, 'w') as f:
    f.write('\n'.join(out_data))
ng_write_f.close()
