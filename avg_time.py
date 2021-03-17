import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-mf', required=True)

args = parser.parse_args()
main_folder = args.mf



avg_det_time=0
avg_all_time=0
count = 0
max_det_time=0

with open(main_folder, "r") as file:
    for line in file:
        # print(line)
        # print(line)
        det_time = line.rsplit('(')[1].rsplit('/')[0]
        all_time = line.rsplit('(')[1].rsplit('/')[1][:5]
        # print(det_time)
        # print(all_time)
        avg_det_time+=float(det_time)
        avg_all_time+=float(all_time)
        if(float(det_time) > max_det_time):
            max_det_time = float(det_time)
        count +=1

print("avg det time {:.3f}\nmax det time {:.3f} \navg all time {:.3f}".format(avg_det_time/count,max_det_time, avg_all_time/count))
