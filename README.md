# ISPRS

2015 ISPRS-Scientific Initiative Open Data Challenge 

codes for qualification round


———— 数据准备 ————

原始(输入)数据： 

1 - BUS_ROUTE_DIC.csv 
2 - GPS_DATA.csv
3 - AFC_DATA.csv 

** 利用Bash关联数据集1和2，得到

5 - GPS_DATA_UNIQ.csv： <route_id, bus_id, day, time, lon, lat>

awk 'BEGIN {FS=OFS=","} NR==FNR {a[$1]=$2;next} {if(a[$1]) print a[$1],$1,$2,$3,$4,$5}' BUS_ROUTE_DIC.csv GPS_DATA.csv | sed -e "s/^M//" | tail -n +2 | sort -t $',' -k1,1n -k2,2n -k3,3n -k4,4n > GPS_DATA_UNIQ.csv 

该数据集按前4个字段排序，反映了各公交车的时空轨迹。


** 利用Bash关联数据集1和3，得到

6 - AFC_DATA_UNIQ.csv： <route_id, bus_id, day, time, card_id, guid>

tail -n +1 AFC_DATA.csv | sort -t, -k5,5n -k3,3n -k4,4n | awk 'BEGIN {FS=OFS=","}{print $5,$3,$4,$2,$1}' | sed -e "s/^M//" > AFC_DATA_SORT.csv
awk 'BEGIN {FS=OFS=","} NR==FNR {a[$1]=$2;next} {if(a[$1]) print a[$1],$1,$2,$3,$4,$5}' BUS_ROUTE_DIC.csv AFC_DATA_SORT.csv | sed -e "s/^M//" | tail -n +2 | sort -t $',' -k1,1n -k2,2n -k3,3n -k4,4n > AFC_DATA_UNIQ.csv

该数据集按前4个字段排序，反映了各公交车乘客按先后顺序上车的时间。

——————————————————


————— TASK 1 ————-

** 利用 extract_all_boarding_coordinates_for_task_1.py 关联数据集5和6，得到

7 - BOARDING_LOCATION_ALL.csv： <guid, card_id, rotue_id, bus_id, day, time, lon, lat>

该程序的输入参数为 <乘客上车时间> 与 <公交车轨迹时间> 的 <<时间差>> 阈值: 5 秒  
结果数据按 <rotue_id, bus_id, day, time> 4个字段排序，反映了所有上车记录中能同车辆轨迹（少于5秒）匹配的上车点位置。


** 利用 extract_route_terminal_coordinates.py 提取各公交车每天 <第一个> 和 <最后一个> GPS记录
然后，利用extract_route_terminal_location.py 从中提取各条公家线路的 起点站 和 终点站位置（使用了DBSCAN聚类方法，参数为 距离 e = 20 和 最小点数 m = 2）

在运行第一个程序后用Bash对结果数据按字段 <route_id, lon，lat> 排序

Sort -t $',' -k2,2n -k4,4n -k5,5n ROUTE_TERMINAL_LOCATION_TMP_NEW.csv > ROUTE_TERMINAL_LOCATION_TMP.csv

最终生成各公交线路 rout_id 的 起点站 和 终点站 数据：

8 - ROUTE_TERMINAL_LOCATION.csv： <rotue_id, lon_1, lat_1, lon_2, lat_2>


** 利用 extract_route_direction.py 关联数据8和5，得到

9 - GPS_DATA_UNIQ_LABELED.csv: <direction_id, route_id, bus_id, day, time, lng, lat>

在该数据集中我们用 0-999 分别标识了各公交车的行驶方向，同过该数据可以查找各公交车任意时刻的行驶方向。


** 利用 extract_all_boarding_coordinates_with_direction.py 关联数据集9和6，得到所有上车记录中能同车辆轨迹（少于5秒）匹配的上车点位置和方向，得到

10 - BUS_STOP_ALL_estimate.csv

然后，利用 extract_all_bus_stop_coordinates.py 提取各条线路（分方向）的公交站台位置，具体采用了DBSCAN点聚类算法，根据数据集10中各条线路和方向上匹配上车点数量，分为三种情形设置DBSCAN的参数： 距离 e 和 最小点数 m

-- 点数 <= 300: e = 20, m = 2
-- 300 < 点数 <= 1000: e = 15, m = 3
-- 点数 > 1000: e = 10, m = 4

以上，task 1处理完毕。

——————————————————

————— TASK 2 ————-

** 利用 extract_all_boarding_coordinates_for_task_2.py 关联数据集5和6，得到

11 - BOARDING_LOCATION_ALL_FOR_TASK_2.csv： <guid, card_id, rotue_id, bus_id, day, time, lon, lat>

该程序与extract_all_boarding_coordinates_for_task_1.py类似，但是无需输入参数 <乘客上车时间> 与 <公交车轨迹时间> 的 <<时间差>> 阈值。 结果数据按 <rotue_id, bus_id, day, time> 4个字段排序，反映了所有上车记录中同车辆轨迹匹配的 <最近上车点位置>。


** 利用 extract_all_boarding_bus_stop_for_task_2.py 关联数据集11和与Task 1提取的公交站台位置数据，得到

12 - BOARDING_BUS_STOP_ALL.csv： <card_id, rotue_id, day, time, bus_id, guid, lon_real, lat_real, stop_id, lon_stop, lat_stop, distance>

该数据按前4个字段 <card_id, route_id, day, time> 排序, 反映了所有上车记录匹配的公交站位置，以及各 card_id 持有者在各条公交线上的上车时空序列。


** 利用数据集12估计task 2中各个guid的下车公交站，我们考虑了两种情形：

-* 1 *- 假设，用户 card_id 在某公交线 R 上的某个公交站 n <最频繁> （次数至少为 2 ）上车，如果 待估计的 guid 位于 R 上：
            
        如果 该上车位置 不是 n , 那么估计其对应的下车位置为 n ; 
        如果 该上车位置 是 n ，那么估计其对应的下车位置为 第二频繁上车的公交站 m;

-* 2 *- 假设，用户 card_id 在某公交线 R 上的任何一个公交站 n 上车的次数都不超过 1 ，如果 待估计的 guid 位于 R 上，

        那么我们估计其对应的下车位置为其上车时刻下一个时刻在该公交线路上的上车车站。


>> 具体处理过程如下：

首先，用Bash统计各 card_id 在给定公交线 route_id 上各 bus_stop 的上车次数，得到

13 - BOARDING_BUS_STOP_FREQUENCY.csv: <card_id_route_id, stop_id, frequency, lon, lat>

tail -n +1 BOARDING_BUS_STOP_ALL.csv | awk 'BEGIN {FS=OFS=","} {print $1, $2, $9, $10, $11}' | sort -t $',' -k1,1n -k2,2n -k3,3n | uniq -c | sed -i 's/     //' | sed -i 's/      //' | awk 'BEGIN {FS=OFS=" "} {print $2"_"$3, $4, $1, $5, $6}' > BOARDING_BUS_STOP_FREQUENCY.csv

同时，可以用数据集12中直接得到各 guid 对应的信息： 某用户在某线路上的某个车站上车

tail -n +1 BOARDING_BUS_STOP_ALL.csv | awk 'BEGIN {FS=OFS=","} {print $1"_"$2, $9, $6}' | sort -t $',' -k1,1n -k2,2n -k3,3n > CARD_GUID_BOARDING_BUS_STOP.csv

14 - CARD_GUID_BOARDING_BUS_STOP.csv: <card_id_route_id, stop_id, guid> 反映了各 card_id 任意一次出行 guid 的上车车站。

利用数据集13和14，即可区分上述两种不同的 guid 类型：


——* 情形1 *——
 
join -1 1 -2 1 CARD_GUID_BOARDING_BUS_STOP.csv BOARDING_BUS_STOP_FREQUENCY.csv | awk 'BEGIN {FS=OFS=" "} {if($2 != $4) print $3,$5,$6,$7}' | sort -t $' ' -k1,1n -k2r,2n | awk 'BEGIN {FS=OFS=" "} {if($2 > 1) print $1,$2,$3,$4}' | awk '!a[$1]++' | awk 'BEGIN {FS=OFS=" "} {if(print $1,$3,$4}' | sort -t $' ' -k1,1n > RESULT_ALIGHT_LIST_SCENARIO_1.csv

## 通过判断某给定线路 route_id 之上 <上车车站> 与 <最频繁访问车站> 是否重合，!! 主键为 card_id 和 route_id 的组合 card_id_route_id !!

即可直接得到该情形下的 guid 的下车车站位置: RESULT_ALIGHT_LIST_SCENARIO_1.csv 和 guid 列表

cut -d , -f1 RESULT_ALIGHT_LIST_SCENARIO_1.csv > GUID_SCENARIO_1.csv


——* 情形2 *——

join -1 1 -2 1 CARD_GUID_BOARDING_BUS_STOP.csv BOARDING_BUS_STOP_FREQUENCY.csv | awk 'BEGIN {FS=OFS=" "} {if($2 != $4) print $3,$5,$6,$7}'  | awk 'BEGIN {FS=OFS=" "} {if($2 == 1) print $1}' | uniq > GUID_SCENARIO_2_TMP.csv

## GUID_SCENARIO_2_TMP.csv 包含只访问某个公交车站 1 次的所有 card_id 对应的 guid 记录，其包含部分 情形1 下的 guid，因此需进行进一步剔除

awk 'BEGIN {FS=OFS=","} NR==FNR {a[$1]=$1;next} {if($1 != a[$1]) print $1}' GUID_SCENARIO_1.csv GUID_SCENARIO_2_TMP.csv > GUID_SCENARIO_2.csv

然后，结合数据集12，找出该情形下的 guid 对应的完整记录信息：

awk 'BEGIN {FS=OFS=","} NR==FNR {a[$1]=$1;next} {if(a[$6]) print $1,$2,$3,$4,$5,$6,$7,$8,$9,$10,$11,$12}' GUID_SCENARIO_2.csv BOARDING_BUS_STOP_ALL.csv > BOARDING_BUS_STOP_SCENARIO_2.csv

将该结果和数据集12作为输入文件，利用 extract_alighting_coordinates_scenario_2.py 估计情形2下相应 guid 的下车点位置： RESULT_ALIGHT_LIST_SCENARIO_2.csv


** 最后，将以上两种情形下的结果 RESULT_ALIGHT_LIST_SCENARIO_1.csv 和 RESULT_ALIGHT_LIST_SCENARIO_2.csv 合并。

以上，task 2处理完毕。

——————————————————


————— 补充说明 ————-

因Bash内置函数如 join，awk，sort 等对输入文件的默认字段分割符要求不统一：如 逗号、空格和tab等，

在此代码说明文档中，在不影响处理逻辑的情况下，我们尽量省略了各个数据集字段分隔符的转换（替代）操作过程。

——————————————————
