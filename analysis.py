import dircache
from operator import itemgetter
DATA_PATH = "Z:\\golinteresting"

files = dircache.listdir(DATA_PATH)
files = [f for f in files if "py" not in f]

rule_absgrowth = {}
rule_avgsize = {}
rule_avgdistance = {}
rule_maxdistance = {}
rule_avgrepetition = {}
rule_timedeath = {}


board_absgrowth = {}
board_avgsize = {}
board_avgdistance = {}
board_maxdistance = {}
board_avgrepetition = {}
board_timedeath = {}


rule                        = 0
abs_growth                  = 1
average_size                = 2
avg_distance_travelled      = 3
max_distance_travelled      = 4
avg_repetition              = 5
time_to_death               = 6
board_number                = 7



def record(dictionary, key, value):
    value = float(value)
    if dictionary.has_key(key):
        dictionary[key] += value
    else:
        dictionary[key] = value





def normalize_sort(dictionary, num_records):
    # NOT NORMALIZED
    records = [(key, value) for key, value in dictionary.iteritems()]
    records.sort(key=itemgetter(1), reverse=True)
    return records


def writeout(filename, header, tuples):
    f = open(filename, "w")
    f.write(header + "\n")
    for key, value in tuples:
        f.write( str(key) + "," + str(value) + "\n")
        
    f.close()
            


num_records = 0.0
for f in files:
    fopen = open(DATA_PATH + "\\" + f, "r")
    
    firstline = True
    
    for line in fopen.readlines():
        if firstline:
            firstline = False
            continue
        
        num_records += 1
        vals = line.split(",")
        
        record(rule_absgrowth       , vals[rule], vals[abs_growth             ])
        record(rule_avgsize         , vals[rule], vals[average_size           ])
        record(rule_avgdistance     , vals[rule], vals[avg_distance_travelled ])
        record(rule_maxdistance     , vals[rule], vals[max_distance_travelled ])
        record(rule_avgrepetition   , vals[rule], vals[avg_repetition         ])
        record(rule_timedeath       , vals[rule], vals[time_to_death          ])
        
        record(board_absgrowth      , vals[board_number], vals[abs_growth             ])
        record(board_avgsize        , vals[board_number], vals[average_size           ])
        record(board_avgdistance    , vals[board_number], vals[avg_distance_travelled ])
        record(board_maxdistance    , vals[board_number], vals[max_distance_travelled ])
        record(board_avgrepetition  , vals[board_number], vals[avg_repetition         ])
        record(board_timedeath      , vals[board_number], vals[time_to_death          ])
        
        




writeout("rule_absgrowth.csv", "rule,absolutegrowth", normalize_sort( rule_absgrowth  , 2040.0))
writeout("rule_avgsize.csv", "rule,averagesize", normalize_sort( rule_avgsize   , 2040.0))
writeout("rule_avgdistance.csv", "rule,averagedistance", normalize_sort( rule_avgdistance  , 2040.0))
writeout("rule_maxdistance.csv", "rule,maxdistance", normalize_sort( rule_maxdistance  , 2040.0))
writeout("rule_avgrepetition.csv", "rule,averagerepetition", normalize_sort( rule_avgrepetition  , 2040.0))
writeout("rule_timedeath.csv", "rule,timetodeath", normalize_sort( rule_timedeath , 2040.0))
writeout("board_absgrowth.csv", "board,absolutegrowth", normalize_sort(  board_absgrowth , 512.0))
writeout("board_avgsize.csv", "board,averagesize", normalize_sort(  board_avgsize , 512.0))
writeout("board_avgdistance.csv", "board,averagedistance", normalize_sort( board_avgdistance  , 512.0))
writeout("board_maxdistance.csv", "board,maxdistance", normalize_sort( board_maxdistance  , 512.0))
writeout("board_avgrepetition.csv", "board,averagerepetition", normalize_sort( board_avgrepetition  , 512.0))
writeout("board_timedeath.csv", "board,timetodeath", normalize_sort(  board_timedeath , 512.0))


