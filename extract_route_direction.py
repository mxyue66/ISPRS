f1 = open('/mnt/vdb/data/GPS_DATA_UNIQ_NEW.csv', 'r')
f2 = open('/mnt/vdb/data/ROUTE_TERMINAL_LOCATION.csv', 'r')
f3 = open('/mnt/vdb/data/GPS_DATA_UNIQ_LABELED.csv', 'w')

line = f1.readline()
f3.write('direction,route_id,bus_id,day,time,lng,lat,trip_id\n')

line = f1.readline()
[route_id, bus_id, day, time, lng, lat, null] = line.replace('\n','').split(',')

## bus terminal coordinates
## bus terminal coordinates
route_id_new = [0 for col in range(486)]
start_lon_new = [0 for col in range(486)]
start_lat_new = [0 for col in range(486)]
end_lon_new = [0 for col in range(486)]
end_lat_new = [0 for col in range(486)]

#linenew = f2.readline()
for i in range(486):
    linenew = f2.readline()
    if len(linenew)!=0:
        [route_id_new[i], start_lon_new[i], start_lat_new[i], end_lon_new[i], end_lat_new[i], null] = linenew.replace('\n','').split(',')
    #print(route_id_new[i], start_lon_new[i], start_lat_new[i], end_lon_new[i], end_lat_new[i])

eps = 0.002
direction = 0
trip_id = 0
f3.write('%s,%s,%s,%s,%s,%s,%s,%s\n'%(direction,route_id,bus_id,day,time,lng,lat,trip_id))

while True:
    line = f1.readline()

    if len(line) == 0:
        break

    [route_id1, bus_id1, day1, time1, lng1, lat1, null] = line.replace('\n','').split(',')

    for i in range(486):
        if route_id1 == route_id_new[i] and bus_id1 == bus_id and day1 == day:

            if (abs(float(lng1) - float(start_lon_new[i])) <= eps and abs(float(lat1) - float(start_lat_new[i])) <= eps):

                direction = 2*(int(route_id1)-1)
		trip_id = trip_id + 1

            if (abs(float(lng1) - float(end_lon_new[i])) <= eps and abs(float(lat1) - float(end_lat_new[i])) <= eps):

                direction = 2*int(route_id1) - 1
		trip_id = trip_id + 1


    if direction == 2*int(route_id1) - 2 or direction == 2*int(route_id1) - 1:
         f3.write('%s,%s,%s,%s,%s,%s,%s,%s\n'%(direction, route_id1, bus_id1, day1, time1, lng1, lat1, trip_id))
    #else:
         #print(direction, route_id1, bus_id1, day1, time1, lng1, lat1, trip_id)    
    [route_id, bus_id, day, time, lng, lat, null] = line.replace('\n','').split(',')

f1.close()
f2.close()
f3.close()
print('done...')
