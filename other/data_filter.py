import datetime
import csv

read_file_paths = [
    '/Users/yetongxue/Downloads/v3.csv',
    '/Users/yetongxue/Downloads/v4.csv',
]
statistic_file_path = '/Users/yetongxue/Downloads/statistic.csv'
statistic_column_names = ['Test_Items', 'Upper Limit', 'Lower Limit']
ng_detail_column_names = ['SerialNumber', 'Test_Items_Data', 'Value', 'Upper Limit', 'Lower Limit']
ng_detail_file_path = '/Users/yetongxue/Downloads/ng_detail.csv'
start = '2020/2/10 01:03'
end = '2020/4/13 01:03'
time_fmt = '%Y/%m/%d %H:%M'

start_time = datetime.datetime.strptime(start, time_fmt)
end_time = datetime.datetime.strptime(end, time_fmt)

upper_limts = []  # 记录表格第一行数据
lower_limts = []  # 记录表格第二行数据
column_names = []  # 记录表格第三行数据
upper_ng_dict = {}  # 统计检测项目超过上限数量
lower_ng_dict = {}  # 统计检测项目超过下限数量
name_limit_map_upper = {}  # 检测项目名称与上限值对应关系
name_limit_map_lower = {}  # 检测项目名称与下限值对应关系
total_inputs = {}  # 记录符合条件（start_time, end_time）的输入记录条数
ng_counts = {}  # Test Pass/Fail Status == FAIL
configs = set()

ng_write_f = open(ng_detail_file_path, 'w')
ng_writer = csv.writer(ng_write_f)
ng_writer.writerow(ng_detail_column_names)


def handle(reader):
    global upper_limts
    global lower_limts
    global column_names
    global upper_ng_dict
    global lower_ng_dict
    global name_limit_map_upper
    global name_limit_map_lower
    global total_inputs
    global ng_counts
    global configs

    for i, line in enumerate(reader):
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
            try:
                line_start = datetime.datetime.strptime(line[0], time_fmt)
                line_end = datetime.datetime.strptime(line[1], time_fmt)
            except:
                continue

            if line_end and line_start:
                LCM_FULL_SN = line[4]
                LCM_FULL_SN_arr = LCM_FULL_SN.split('+')
                config = LCM_FULL_SN_arr[1][-3:]
                configs.add(config)
                if line_start > start_time and line_end < end_time:
                    total_inputs.update({config: total_inputs.get(config, 0) + 1})
                    if line[2] == 'FAIL':
                        ng_counts.update({config: ng_counts.get(config, 0) + 1})

                    for index, column_name in enumerate(column_names):
                        if index >= 6:
                            # 统计超过上下限的项目
                            column_name_key = '{}_{}'.format(column_names[index], config)
                            try:
                                if float(upper_limts[index]) < float(line[index]):
                                    upper_ng_dict.update(
                                        {column_name_key: upper_ng_dict.get(column_name_key, 0) + 1})
                                    ng_writer.writerow(
                                        [line[5], column_name, line[index], upper_limts[index], lower_limts[index]])
                            except:
                                pass
                            # 统计超过下限的项目
                            try:
                                if float(lower_limts[index]) > float(line[index]):
                                    lower_ng_dict.update(
                                        {column_name_key: lower_ng_dict.get(column_name_key, 0) + 1})
                                    ng_writer.writerow(
                                        [line[5], column_name, line[index], upper_limts[index], lower_limts[index]])
                            except:
                                pass


for path in read_file_paths:
    read_f = open(path, 'r')
    reader = csv.reader(read_f)
    handle(reader)

out_data = []
configs = list(configs)
for name in column_names[6:]:
    upper_limit = name_limit_map_upper.get(name)
    lower_limit = name_limit_map_lower.get(name)
    row = [name, upper_limit, lower_limit]
    for config in configs:
        name_config_key = '{}_{}'.format(name, config)
        row.extend([upper_ng_dict.get(name_config_key, 0) if upper_limit != 'NA' else 0, lower_ng_dict.get(name_config_key, 0) if lower_limit != 'NA' else 0])
    out_data.append(row)

with open(statistic_file_path, 'w') as f:
    statistic_writer = csv.writer(f)
    # 写入column name, total input, ng count
    total_inputs_row = ['Total Input'] + [''] * (len(statistic_column_names) - 1)
    ng_counts_row = ['NG'] + [''] * (len(statistic_column_names) - 1)
    upper_lower_limit_ng = [''] * len(statistic_column_names) + ['Upper Limit_NG', 'Lower Limit_NG'] * len(configs)
    for config in configs:
        statistic_column_names.extend([config, ''])
        total_inputs_row.extend([total_inputs.get(config, 0), ''])
        ng_counts_row.extend([ng_counts.get(config, 0), ''])
    statistic_writer.writerows([statistic_column_names, total_inputs_row, ng_counts_row, upper_lower_limit_ng])

    # 写入检测项目NG个数
    statistic_writer.writerows(out_data)

read_f.close()
ng_write_f.close()
print('处理完成')
