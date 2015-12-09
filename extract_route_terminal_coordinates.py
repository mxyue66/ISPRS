fname1 = '/home/user/data/GPS_DATA_UNIQ.csv'
fname2 = '/home/user/data/ROUTE_TERMINAL.csv'

f1 = open(fname1, 'r')
f2 = open(fname2, 'w')

size_gps = 35196621

[route_id, bus_id, day, time, lon, lat, null] = f1.readline().replace('\n', '').split(',')
if int(time) < 3600 * 24:
	f2.write('%s,%s,%s,%s,%s,%s\n' % (route_id, bus_id, day, time, lon, lat))

for i in range(size_gps - 1):
	[route_id_new, bus_id_new, day_new, time_new, lon_new, lat_new, null] = f1.readline().replace('\n', '').split(',')

	if route_id == route_id_new and bus_id == bus_id_new and day == day_new:
		[route_id, bus_id, day, time, lon, lat] = [route_id_new, bus_id_new, day_new, time_new, lon_new, lat_new]
	else:
		if int(time) > 3600 * 0:
			f2.write('%s,%s,%s,%s,%s,%s\n' % (route_id, bus_id, day, time, lon, lat))
		[route_id, bus_id, day, time, lon, lat] = [route_id_new, bus_id_new, day_new, time_new, lon_new, lat_new]
		if int(time) < 3600 * 24:
			f2.write('%s,%s,%s,%s,%s,%s\n' % (route_id, bus_id, day, time, lon, lat))

f1.close()
f2.close()
print('done...')
