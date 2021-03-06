#!/usr/bin/env python3
import itertools
import os, sys
import glob
import re
import numpy as np
import xml.etree.ElementTree as ET

# ***************************************************************************
# Knobs
# ***********

PARTITION_FACTOR =[2,4,8,16]
SUBDIM_X =[1,2,4,8,16]
SUBDIM_Y =[1,2,4,8,16]
UNROLL_FACTOR1= [1,2,4,8]
UNROLL_FACTOR2=[1,2,4,8]
UNROLL_FACTOR3=[1,2,4,8]
allCombinations = list(itertools.product(
    PARTITION_FACTOR,        # 0
    SUBDIM_X,
    SUBDIM_Y,
    UNROLL_FACTOR1,UNROLL_FACTOR2,UNROLL_FACTOR3    ))
# ***************************************************************************


def parse_resources(resources_node):
    tags = ['BRAM_18K','DSP48E','FF','LUT']
    resources = [ resources_node.find(t).text for t in tags ]
    return list(map(int, resources))


def parse_xml(filename1,filename2):
    tree = ET.parse(filename1)
    root = tree.getroot()

    #resources_node       = root.find('AreaEstimates/Resources')
    #avail_resources_node = root.find('AreaEstimates/AvailableResources')
    est_clk_period = root.find('TimingReport/AchievedClockPeriod').text
    slices=root.find('AreaReport/Resources/SLICE').text
    tree=ET.parse(filename2)
    root=tree.getroot()
    slices=int(slices)
    avg_latency = root.find('PerformanceEstimates/SummaryOfOverallLatency/Average-caseLatency').text
    #resources       = parse_resources(resources_node)
    #avail_resources = parse_resources(avail_resources_node)
    throughput="{0:.3f}".format(((int(avg_latency)*float(est_clk_period))/1000000000))
    #resources_util = np.divide(resources, avail_resources)*100
    #for i in range(4):
        #resources_util[i]="{0:.2f}".format(resources_util[i])
    return slices,throughput



def removeCombinations(combs):

    finalList = []

    for c in combs:
        copyit = True
	
        #if c[2]>c[0] or c[2]>c[1]:
            #copyit =False

        if copyit:
            finalList.append(c)

    return finalList


def main():

    finalCombinations = removeCombinations(allCombinations)
    file1=open('final_result_impl_matrixmul.csv','w')
    file1.write("n"+","+"knob_PARTITION_FACTOR"+","+"knob_SUBDIM_X"+","+"knob_SUBDIM_Y"+","+"knob_UNROLL_FACTOR1"+","+"knob_UNROLL_FACTOR2"+","+"knob_UNROLL_FACTOR3"+","+"obj1"+","+"obj2\n")
    for d in sorted(glob.glob('impl_reports/matrix_mul_export*.xml')):
        m = re.search('matrix_mul_export(\d+)', d)
        num = m.group(1)
        synth_path=os.path.join('syn_reports/csynth'+num+'.xml')
        slices,lat=parse_xml(d,synth_path)
        file1.write(num+",")
        for j in range(6):
            file1.write(str(finalCombinations[int(num)][j])+",")
        file1.write(str(lat)+","+str(slices)+"\n")

if __name__ == "__main__":
    main()
        
