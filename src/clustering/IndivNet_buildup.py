import pandas as pd
import numpy as np

#Get ranks for each gene
def getRanks(i):
    d = df.iloc[i]
    s = sorted(range(len(d)), key = lambda k: -d[k])
    return s[1:11] #First value is the index

#Returns the top three genes connected to the given gene
def NextThreeGenes(new_cluster,gene):
    close_genes = np.array(Ranks.iloc[gene, :3])
    if sum(gene in new_cluster for gene in close_genes) == 3:
        return new_cluster, []
    else:
        newGenes = [gene for gene in close_genes if not gene in new_cluster]
        new_cluster = np.append(new_cluster, newGenes)
        return new_cluster,newGenes

#Greedily incorporates genes into clusters until no more connections can be made
def AddGenes(new_cluster,gene):
    nextGenes = []
    while True:
        new_cluster, newGenes = NextThreeGenes(new_cluster,gene)
        if len(newGenes) == 0:
            if len(nextGenes) == 0:
                return new_cluster
            else:
                while True:
                    gene = nextGenes[0]
                    nextGenes = nextGenes[1:]
                    if gene not in new_cluster:
                        break
                    elif len(nextGenes) == 0:
                        return new_cluster
        else:
            gene = newGenes[0]
            next = newGenes[1:len(newGenes)]
            nextGenes = np.append(nextGenes,np.array(next))
            nextGenes = nextGenes.astype(int)


#Take the first available gene and start making clusters based on it's top three connections, etc
def makeSmallCluster(genes_remaining,clusters):
    start_gene = genes_remaining[0]
    close_genes = np.array(Ranks.iloc[start_gene,:3])
    new_cluster = np.append(start_gene,close_genes)
    for gene in close_genes:
        #Add genes until the cluster can't get larger
        new_cluster = AddGenes(new_cluster,gene)

    #Add to existing cluster if applicable
    if sum(gene in genes_remaining for gene in new_cluster) < len(new_cluster):
        for i in range(len(clusters)):
            if sum(gene in clusters[i] for gene in new_cluster) > 0:
                clusters[len(clusters)] = np.append(new_cluster,clusters[i])
                clusters[i] = [] #Remove old cluster
    else:
        clusters.append([new_cluster])
    genes_remaining = [gene for gene in genes_remaining if not gene in new_cluster]
    return genes_remaining, clusters


def ConstructInitialClusters():
    genes_remaining = np.array(range(Ranks.shape[0]))
    clusters = [[] for x in range(1)]
    #while len(genes_remaining) > 0:
    genes_remaining,clusters = makeSmallCluster(genes_remaining,clusters)
    genes_remaining,clusters = makeSmallCluster(genes_remaining,clusters)

    return clusters

def main(argv):
    #inputfile, outputfile = InOut(argv)
    inputfile = "~/Data/devnetwork/beeShortTestpCor.csv"
    outputfile = "~/Data/devnetwork/beesOne.txt"

    global start_d
    start_d = 3 #Start building small graphs with connections of three genes at a time

    #Read in dataframe of pearson correlations
    global df, Ranks, TopGenes,d
    df = pd.read_csv(inputfile)
    df = abs(df) #Make networks based on magnitude of correlation ('unsigned')
    Ranks = pd.DataFrame([getRanks(i) for i in range(df.shape[0])])
    df = None

    clusters = ConstructInitialClusters()
    print clusters

    # Giant = False
    # d = start_d
    # while not Giant:
    #     d = d+1
    #     CombineClusters() #Use the extra connection to combine clusters
    #     Giant = CheckGiant() #Check if the graph is giant

    # #Get the network two steps ago
    # net = getNet(d+2)
    # print "final" + str(d+2)
    # net.to_csv(outputfile,sep="\t",index=None,header=False)

if __name__ == "__main__":
    main("2")