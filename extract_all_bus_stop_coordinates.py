import numpy as np

from sklearn.cluster import DBSCAN

import csv

def load_data(fin_path):
    files = file(fin_path,'r')
    reader = csv.reader(files)

    reader.next()     
    res_0 = []
    for id,route_id1,route_id2,bus_id1,bus_id2,day1,day2,time1,time2,lon,lat,card_id,guid in reader:
        temp_0 = []
        
        temp_0.append(int(route_id1))
        temp_0.append(float(lon))
        temp_0.append(float(lat))
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
        if len(X_0)<=300:
            e = 20
            m = 2
			
	elif 300 < len(X_0)<= 1000:
        	e = 15
		m = 3
            
        else:
            e = 10
            m = 4
                
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
            f_new.write("%s,%s,%s,%s,%s\n" %(k,route_id,sequence,float(lon),float(lat)))
            k = k+1
    f_new.close()

if __name__ == "__main__":
    fin = "/home/user/data/BUS_STOP_ALL_estimate.csv"
    fout = "/home/user/data/BUS_STOPS.csv"
	
    route_id = range(1,271)
    my_fun(fin, fout, route_id)
 
 
 
 
 
 
 
 
#     
