
f1 = open('/mnt/vdb/data/BOARDING_BUS_STOP_ALL_SORT_FOR_ALIGHTING.csv', 'r')
f2 = open('/mnt/vdb/data/BOARDING_BUS_STOP_SCENARIO_2.csv', 'r')
f3 = open('/mnt/vdb/data/RESULT_ALIGHT_LIST_SCENARIO_2.csv', 'w')

line_tmp = f1.readline()
[card_id_tmp, route_id_tmp, day_tmp, time_tmp, bus_id_tmp, guid_tmp, lon_real_tmp, lat_real_tmp, stop_id_tmp, seq_tmp, lon_stop_tmp, lat_stop_tmp, distance_tmp, direction_id_tmp, null] = line_tmp.split(',')

while True:
	line = f2.readline()

	if len(line) == 0:
		break

	[card_id, route_id, day, time, bus_id, guid, lon_real, lat_real, stop_id, seq, lon_stop, lat_stop, distance, direction_id, null] = line.split(',')

	while True:
		line_new = f1.readline()

		if len(line_new) == 0:
			break

		[card_id_new, route_id_new, day_new, time_new, bus_id_new, guid_new, lon_real_new, lat_real_new, stop_id_new, seq_new, lon_stop_new, lat_stop_new, distance_new, direction_id_new, null] = line_new.split(',')

		if card_id == card_id_tmp and route_id == route_id and day == day_tmp and time == time_tmp:
			f3.write('%s\t%s\t%s\t%s\t%s\n' %(guid, stop_id_new, seq_new, lon_stop_new, lat_stop_new))

			[card_id_tmp, route_id_tmp, day_tmp, time_tmp, bus_id_tmp, guid_tmp, lon_real_tmp, lat_real_tmp, stop_id_tmp, seq_tmp, lon_stop_tmp, lat_stop_tmp, distance_tmp, direction_id_tmp] = [card_id_new, route_id_new, day_new, time_new, bus_id_new, guid_new, lon_real_new, lat_real_new, stop_id_new, seq_new, lon_stop_new, lat_stop_new, distance_new, direction_id_new]
			break

		else:
			[card_id_tmp, route_id_tmp, day_tmp, time_tmp, bus_id_tmp, guid_tmp, lon_real_tmp, lat_real_tmp, stop_id_tmp, seq_tmp, lon_stop_tmp, lat_stop_tmp, distance_tmp, direction_id_tmp] = [card_id_new, route_id_new, day_new, time_new, bus_id_new, guid_new, lon_real_new, lat_real_new, stop_id_new, seq_new, lon_stop_new, lat_stop_new, distance_new, direction_id_new]

f1.close()
f2.close()
f3.close()
print('done...')
