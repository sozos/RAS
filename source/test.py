# unit tests
from assigning import *
from reassign import *

# test index_free
assert index_free([[4, 6, 9, 6, 9]], [2, 3, 5, 2, 6]) >= 0
assert index_free([[1, 1, 3, 1, 3], [3, 5, 7, 5, 7]], [5, 10, 13, 3, 6]) == -1

# test assign
# deprecated
# assert assign([[None,1,2],[None,5,6],[None,10,12]],[None,3,4]) == [[None,1,2],[None,3,4],[None,5,6],[None,10,12]]
# assert assign([],[None,3,4]) == [[None,3,4]]

# test reassign
intervals = [[1,1,3,1,3],[2,3,5,2,6],[3,5,7,4,7],[4,6,9,6,9],[5,10,13,3,6]]
gates = assigning(intervals)
results = reassign(gates, intervals)
for i, gate in enumerate(results[0]):
	print "Gate", i, ":", gate
print "Overflow gates: ", results[1]

#test buffer gates
new_gates = assign_max_slack(gates, intervals, 3)
print 'Buffer gates'
for i, gate in enumerate(new_gates):
	print "Gate", i, ":", gate
print 'End buffer gates'

# test delay
interval = [None, 1000, 1045, None, None]
delay(interval, 60)
assert interval == [None, 1000, 1045, 1000, 1145]

interval = [None, 830, 1030, None, None]
delay(interval, 60)
assert interval == [None, 830, 1030, 830, 1110]

intervals = [[None, 1000, 1045, 0, 0],[None, 1200, 1245, 0, 0], [None, 1400, 1600, 0, 0]]
delay_intervals(intervals, 0.5, -100, 100)
print intervals

intervals = [[None, 1, 5, 1, 10], [None, 10, 15, 8, 15]]
gates = assigning(intervals)
assert count_collisions(gates, intervals) == 1