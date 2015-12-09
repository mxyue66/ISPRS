from numpy import math

fname1 = '/mnt/vdb/data/ALL_STOPS.csv'
fname2 = '/mnt/vdb/data/BOARDING_LOCATION_ALL_FOR_TASK_2.csv'
fname3 = '/mnt/vdb/data/BOARDING_BUS_STOP_ALL.csv'

f1 = open(fname1, 'r')
f2 = open(fname2, 'r')
f3 = open(fname3, 'w')

size_training = 17345170 
size_bus_stop = 31705 ## number of bus stops

j = 0
tmp = 0
lines = f1.readlines()

for i in range(size_training):
#	[route_id, direction_id, stop_id, lon, lat, null] 
	[guid, card_id, route_id, direction_id, bus_id, day, time, lon, lat, null] = f2.readline().split(',')

	route_id = int(route_id)
	direction_id = int(direction_id)
#	stop_id = int(stop_id)
	lon = float(lon)
	lat = float(lat)

	#print(i)

	s = 10000000

	j = tmp
	while j < len(lines):

		[route_id_new, direction_id_new, stop_id_new, seq_new, lon_new, lat_new, null] = lines[j].split(',')

		route_id_new = int(route_id_new)
		direction_id_new = int(direction_id_new)
		lon_new = float(lon_new)
		lat_new = float(lat_new)

		if route_id > route_id_new:
			tmp = j 
			j = j + 1

		elif route_id == route_id_new:

			if direction_id > direction_id_new:
				j = j + 1

			elif direction_id == direction_id_new:

		 		ds = abs(math.sqrt(pow(lon - lon_new, 2) + pow(lat - lat_new, 2)))
				#print(route_id, route_id_new, bus_id, bus_id_new, day, day_new, time, time_new, s, dt)

				if ds < s:
					s = ds
					[guid_tmp, card_id_tmp, route_id_tmp, direction_id_tmp, bus_id_tmp, day_tmp, time_tmp, lon_tmp, lat_tmp, stop_id_tmp,seq_temp, lon_tmp_2,lat_tmp_2, distance] = [guid, card_id, route_id_new, direction_id, bus_id, day, time, lon, lat, stop_id_new,seq_new, lon_new, lat_new, s]
					j = j + 1

				else:
					#print(route_id, route_id_tmp, bus_id, bus_id_tmp, day, day_tmp, time, time_tmp, s)
					j = j - 1
					break

			else:
				break

		else:
			break

	f3.write('%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n' % (card_id_tmp, route_id_tmp, day_tmp, time_tmp, bus_id_tmp, guid_tmp, lon_tmp, lat_tmp, stop_id_tmp, seq_temp,lon_tmp_2, lat_tmp_2, distance, direction_id_tmp))

f1.close()
f2.close()
f3.close()
print('done...')
