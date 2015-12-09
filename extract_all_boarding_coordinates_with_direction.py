fname1 = '/home/user/data/GPS_DATA_UNIQ_LABELED.csv'
fname2 = '/home/user/data/AFC_DATA_UNIQ.csv'
fname3 = '/home/user/data/BUS_STOP_ALL_estimate.csv'

f1 = open(fname1, 'r')
f2 = open(fname2, 'r')
f3 = open(fname3, 'w')

f3.write('route_id1,route_id2,bus_id1,bus_id2,day1,day2,time1,time2,lon,lat,card_id,guid,direction\n')

size_training = 7376352
size_gps = 35186221

j = 0
lines = f1.readlines()

for i in range(size_training):
	[route_id, bus_id, day, time, card_id, guid, null] = f2.readline().split(',')

	route_id = int(route_id)
	bus_id = int(bus_id)
	day = int(day)
	time = int(time)

#	print(i)

	s = 10000000

	while j < len(lines):

		#print(j, lines[j])
		[direction, route_id_new, bus_id_new, day_new, time_new, lon, lat, trip_id] = lines[j].replace('\n', '').split(',')

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
						[direction_tmp, guid_tmp, card_id_tmp, route_id_tmp,bus_id_tmp, day_tmp, time_tmp, lon_tmp, lat_tmp] = [direction, guid, card_id, route_id_new, bus_id_new, day_new, time_new, lon, lat]
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


	if s <= 5:
		f3.write('%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n' %(route_id, route_id_tmp, bus_id, bus_id_tmp, day, day_tmp, time, time_tmp, lon_tmp, lat_tmp, card_id_tmp, guid_tmp, direction_tmp))

f1.close()
f2.close()
f3.close()
print('done...')
