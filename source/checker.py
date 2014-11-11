# A simple-minded nested loop to:
# (i) Step through all possible minutes in a day
# (ii) Consider all possible intervals
# Returns the highest number of collision in the entire day

# Note: Provided indices will determine whether we count for scheduled or delayed start/end
# Note: Intervals are considered as [a, b)
def calculate_max_collisions(interval_list, start_index, end_index):
	counter = [0] * 1440 # 24hrs * 60min = 1440 minutes
	for i in range(0, 1440):
		for row in interval_list:
			start = row[start_index]
			end = row[end_index]
			if (start <= i and i < end):
				counter[i] += 1
	return max(counter)
