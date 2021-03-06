from gettext import find
from importlib.resources import path
from math import atan2, cos, sin, sqrt, pi
from sys import maxsize
from itertools import permutations
from typing import Mapping
import gmplot
#---------------------------------------------------------------------------------------------------------------------------------------

#calculate distance from one store to another store (first store, second store)
def distance(first,second):

    r = 6371
    dlat = degToRad(second[1] - first[1])
    dlong = degToRad(second[0] - first[0]) 
    x = sin (dlat/2) * sin (dlat/2)
    y = cos (degToRad(first[1]) * cos(degToRad(second[1])))
    z = sin(dlong/2) * sin(dlong/2)
    a = x+y*z
    c = 2 * atan2(sqrt(a),sqrt(1-a))
    d = r*c
    return d

# convert degree to radian
def degToRad(deg):
    return deg * (pi/180)

#-------------------------------------------------------------------------------------------------------------------------------

v = 5
# center = 0
def computeShortestPath(listdistance,center):
    vertex = []
    for i in range(v):
        if i!=center:
            vertex.append(i)

    # print("vertex: ", vertex)
    mindistance = maxsize
    # print ("max size: ",maxsize)

    # listPermute = list(permutations(vertex))
    # print("total permutation",len(listPermute))
    # print()
    vertexPermute = permutations(vertex)

    
    # print("path: \t\t\t  total distance: ")
    for i in vertexPermute:
        currentdistance = 0
        k=center
        for j in i:
            currentdistance += listdistance[k][j]
            k = j 
        currentdistance += listdistance[k][center] #add distance from last node to the initial node
        # print(i," \t ", currentdistance)    

        if(currentdistance<=mindistance):
            mindistance = min(mindistance, currentdistance)
            path = i

    return {'mindistance':mindistance, 'path':path, 'center':center}

#------------------------------------------------------------------------------------------------------------------------

def plot(text):

    #read path.txt file
    # with open("path.txt") as textFile:
    #     line_array = textFile.read().splitlines()
    #     # line_array = textFile.read()
    #     location = [line.split(' ,') for line in line_array]
    # location = re.split(',|(|)', line_array)

    path = [[0,4,2,1,3],[3,0,1,2,4],[0,4,1,3,2],[3,4,0,1,2],[0,3,4,2,1]]
    # print(path)
    for i in text:
        country = text[i]
        coordinate = readFile(country)
        # print("original coordinate ",coordinate)
        # print(coordinate)

        location = [[0 for i in range(len(coordinate))] for j in range (len(coordinate))]
        #susun coordinate ikut path[]
        k=0
        for j in path[i]:
            location[k] = coordinate[j] #to sort the stores location (long,lat) according to the sorted path
            k=k+1
        # print("sorted location ",location)
        
        #transfer long and lat from 2d array to 1d array
        lat=[]
        long=[]
        for m in range(len(location)):
            long.append(location[m][1])
            lat.append(location[m][0]) 

        # print("latitude ", lat)
        # print("longitude ",long,"\n")

        mapping = gmplot.GoogleMapPlotter(lat[0],long[0],zoom=10,apikey="")
        mapping.plot(lat,long,'red',edge_width = 2.5) # to connect the location from 1 store to another store\

        # to connect the last store to deliver to the starting store
        lastPath = zip(*[
            (lat[len(lat)-1],long[len(long)-1]),
            (lat[0],long[0])
        ])
        mapping.plot(*lastPath,'red',edge_width = 2.5)

        # to mark the stores according to their original number
        j=0
        for m in range(len(coordinate)):
            if (m==path[i][0]):
                mapping.marker(lat[m],long[m], label=path[i][0], color="green")
            else:
                mapping.marker(lat[m],long[m], label=path[i][j], color="green")
                j=j+1

        mapping.draw("Problem 2\\map %d.html" %(i))

#------------------------------------------------------------------------------------------------------------------------

#read location(lat,long) from text file
def readFile(file):
    with open(file) as textFile:
        line_array = textFile.read().splitlines()
        location = [line.split(",") for line in line_array]

    floatLocation = [[0 for i in range (len(location[0]))] for j in range (len(location))]
    for i in range(len(location)):
        for j in range (len(location[0])):
            floatLocation[i][j] = float(location[i][j])
    
    return floatLocation

#------------------------------------------------------------------------------------------------------------------------

#find center of the stores
def findCenter(listdistance):
    
    temp = maxsize
    # print("temp", temp)
    for i in range(len(stores)):
        average=0
        for j in range(len(stores)):
            average = average + listdistance[i][j]
        average = average/5
        if average<temp:
            # print("average",average)
            temp = average
            center = i
            # print("average ",average, " center ", i)

    return center

#------------------------------------------------------------------------------------------------------------------------

#to sort rank
def sortDeliveryRank(allShortest,countries):
    pairlist = dict(zip(countries, allShortest))
    sortedDeliveryRank = sorted(pairlist.items(), key=lambda x: x[1])

    return sortedDeliveryRank

#------------------------------------------------------------------------------------------------------------------------

#driver code
if __name__ == "__main__":

    text = {
        0 : "Problem 2\\canada stores.txt",
        1 : "Problem 2\\uae stores.txt",
        2 : "Problem 2\\china stores.txt",
        3 : "Problem 2\\singapore stores.txt",
        4 : "Problem 2\\philippines stores.txt"
    }
    
    allShortest = []
    countries = ['Canada','UAE','China','Singapore','Phillipines']    

    j=0
    for i in text:
        country = text[i]
        stores = readFile(country)
        # print("text: ", stores)     
        # print stores
        print("\n*****************",countries[i],"*****************\n")
        print("Store\tLatitude\tLongitude")
        for i in range(len(stores)):
            print(i,"\t",stores[i][0],"\t",stores[i][1])
        print()

        #calculate distance from one store to another store
        listdistance = [[0 for i in range(len(stores))] for j in range (len(stores))] #matrix representation graph
        # center = stores[0]
        for i in range (len(stores)):
            for j in range (len(stores)):
                listdistance[i][j] = float(distance(stores[i],stores[j]))

        #print all dinstance
        print("Matrix representation distance (km): \n")
        print("Eg:")
        print("[ 03 ] means distance from Store 0 to Store 3\n")
        for i in range(len(stores)):
            for j in range(len(stores)):
                print("[ ",i,j," ]", end=" ")
            print()

        print()
        for i in range (len(stores)):
            print(listdistance[i])
        print("\n")

        #find center of the stores
        # center = 0
        center = findCenter(listdistance)

        print("---------- Computing Shortest Path For Delivery ----------")
        ret = computeShortestPath(listdistance, center)
        print("\nCenter (starting and ending): ",ret['center'])
        print("Shortest Path: ", ret['path'])
        print("Total Distance: %.4f" % (ret['mindistance']),"km\n")
        # plot(ret['path'], stores,ret['center'])
        allShortest.insert(i,ret['mindistance'])
        f = open("path.txt","a")
        # write = ret['center'],ret['path'],"\n"
        f.write(str(ret['center']))
        # for i in range(len(ret['path'])):
        f.write(str(ret['path']))
        f.write("\n")
        f.close()
        plot(text)

    rank = sortDeliveryRank(allShortest,countries)
    print("-----------------------------------------------------------------------")
    print("\n\nRank of countries based on the shortest delivery")
    print("No\tCountry\t\tTotal Delivery")
    for i in range(len(rank)):
        # for i in range(len(rank[0])):
        print(i," \t",rank[i][0],"\t","%.4f" %(rank[i][1]))
    print("\n")