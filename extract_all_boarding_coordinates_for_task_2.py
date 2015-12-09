fname1 = '/home/user/data/GPS_DATA_UNIQ_LABELED.csv'
fname2 = '/home/user/data/AFC_DATA_UNIQ.csv'
fname3 = '/home/user/data/BOARDING_LOCATION_ALL_FOR_TASK_2.csv'

f1 = open(fname1, 'r')
f2 = open(fname2, 'r')
f3 = open(fname3, 'w')

size_training = 20036592 
size_gps = 57901061

j = 0

lines = f1.readlines()

for i in range(size_training):
	[route_id, bus_id, day, time, card_id, guid, null] = f2.readline().split(',')

	route_id = int(route_id)
	bus_id = int(bus_id)
	day = int(day)
	time = int(time)

	#print(i)

	s = 10000000

	while j < len(lines):

		[direction_id, route_id_new, bus_id_new, day_new, time_new, lon, lat,trip_id, null] = lines[j].split(',')

		route_id_new = int(route_id_new)
		bus_id_new = int(bus_id_new)
		day_new = int(day_new)
		time_new = int(time_new)

		if route_id > route_id_new:
			j = j + 1

		elif route_id == route_id_new:

			if bus_id > bus_id_new:
				j = j + 1

			elif bus_id == bus_id_new:

		 		if day > day_new:
		 			j = j + 1

		 		elif day == day_new:

		 			dt = abs(time_new - time)
					#print(route_id, route_id_new, bus_id, bus_id_new, day, day_new, time, time_new, s, dt)

					if dt < s:
						s = dt
						[direction_tmp, guid_tmp, card_id_tmp, route_id_tmp, bus_id_tmp, day_tmp, time_tmp, lon_tmp, lat_tmp] = [direction_id, guid, card_id, route_id_new, bus_id_new, day_new, time_new, lon, lat]
						j = j + 1

					else:
						#print(route_id, route_id_tmp, bus_id, bus_id_tmp, day, day_tmp, time, time_tmp, s)
						j = j - 1
						break

				else:
					break

			else:
				break

		else:
			break


	#if s <= 5:
	f3.write('%s,%s,%s,%s,%s,%s,%s,%s,%s\n' % (guid_tmp, card_id_tmp, route_id_tmp, direction_tmp, bus_id_tmp, day_tmp, time_tmp, lon_tmp, lat_tmp))

f1.close()
f2.close()
f3.close()
print('done...')
