import numpy as np

from sklearn.cluster import DBSCAN

import csv

def load_data(fin_path):
    files = file(fin_path,'r')
    reader = csv.reader(files)

    reader.next()
    res_0 = []

    for route_id, bus_id, day, time, lon, lat in reader:
        temp_0 = []

        temp_0.append(int(route_id))
        temp_0.append(float(lon))
        temp_0.append(float(lat.replace('\n', '')))
        res_0.append(temp_0)

    X_0 =  np.array(res_0)
    return X_0

def my_fun(fin_path, fout_path, route_id):

    X = load_data(fin_path)

    # print X
    # Compute DBSCAN

    fout = fout_path
    f_new = open(fout,'w')
    f_new.write('stop_id,route_id,sequence,lon,lat\n')
    k = 1

    for ii in route_id:

        X_0 = X[np.where(X[:,0] == ii), :][0,:]
        if len(X_0) <=500:
            e = 20
            m = 2

            #       elif 200 < len(X_0) <= 2000:
           # e = 30
           # m = 2

        else:
            e = 20
            m = 5

        if len(X_0) > 0:
            db_0 = DBSCAN(float(e)/100000, int(m)).fit(X_0[:,[1,2]])
            core_samples_mask = np.zeros_like(db_0.labels_, dtype=bool)
            core_samples_mask[db_0.core_sample_indices_] = True
            labels_0 = db_0.labels_
        # Number of clusters in labels, ignoring noise if present.
            n_clusters_0 = len(set(labels_0)) - (1 if -1 in labels_0 else 0)

            central_points_0 = []

            for i in range(1, n_clusters_0):
                idx = np.where(labels_0 == i)

                temp_route_id_0 = np.mean(X_0[idx,0])
                temp_central_lon_0 = np.mean(X_0[idx,1])
                temp_central_lat_0 = np.mean(X_0[idx,2])

                temp = []
                temp.append('')
                temp.append(temp_route_id_0)
                temp.append(i)
                temp.append(temp_central_lon_0)
                temp.append(temp_central_lat_0)
                central_points_0.append(temp)



        for stop_id,route_id,sequence,lon,lat in central_points_0:
            f_new.write("%s,%s,%s,%s,%s\n" %(k,int(route_id),sequence,float(lon),float(lat)))
            k = k+1
    f_new.close()

if __name__ == "__main__":
    fin = "/home/user/data/ROUTE_TERMINAL.csv"
    fout = "/home/user/data/ROUTE_TERMINAL_LOCATION_TMP_NEW.csv"

    route_id = range(1,271)
    my_fun(fin, fout, route_id)

    f3 = open('/home/user/data/ROUTE_TERMINAL_LOCATION_TMP.csv', 'r')
    f4 = open('/home/user/data/ROUTE_TERMINAL_LOCATION.csv', 'w')

    lines = f3.readlines()

    [stop_id, route_tmp, squence, lon_tmp, lat_tmp] = lines[0].replace('\n', '').split(',')

    for i in range(1, 2383):
        [stop_id, route_id, sequence, lon, lat] = lines[i].replace('\n', '').split(',')

        if route_id != route_tmp:
            [stop_id, route_id, sequence, lon, lat] = lines[i-1].replace('\n', '').split(',')
            f4.write('%s,%s,%s,%s,%s\n' % (route_tmp, lon_tmp, lat_tmp, lon, lat))
            [stop_id, route_tmp, sequence, lon_tmp, lat_tmp] = lines[i].replace('\n', '').split(',')

    f4.write('%s,%s,%s,%s,%s\n' % (route_tmp, lon_tmp, lat_tmp, lon, lat))
    f3.close()
    f4.close()
