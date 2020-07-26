# format data from the experiments to plots or tables
import matplotlib

matplotlib.use('Qt5Agg')


def visualise(detection_data):
    thresholds = sorted(list(detection_data.keys()))

    observed_ips = list(detection_data[thresholds[0]].keys())

    colors = {"1.1.1.10": "red", "1.1.1.11": "forestgreen"}
    linewidths = {"1.1.1.10": 5, "1.1.1.11": 2}
    alphas = {"1.1.1.10": 0.8, "1.1.1.11": 1.0}

    ips_raw_detections = {ip: [detection_data[t][ip][0] for t in thresholds] for ip in observed_ips}

    for ip in observed_ips:
        matplotlib.pyplot.plot(thresholds,
                               ips_raw_detections[ip],
                               color=colors[ip],
                               linewidth=linewidths[ip],
                               alpha=alphas[ip],
                               label=ip)
    matplotlib.pyplot.ylim(-1.05, 1.05)
    matplotlib.pyplot.xticks(list(range(0, 20)))
    matplotlib.pyplot.grid(True)
    matplotlib.pyplot.gca().set_aspect(4.5)
    matplotlib.pyplot.xlabel('Algorithm rounds')
    matplotlib.pyplot.ylabel('IPS detection')
    matplotlib.pyplot.legend()
    matplotlib.pyplot.show()



def find_best_threshold_wide_table(observation_results: dict):
    thresholds = sorted(list(observation_results.keys()))
    first_threshold = thresholds[0]
    observed_ips = list(observation_results[first_threshold].keys())

    lines = {observed_ip: str(observed_ip) + " & " for observed_ip in observed_ips}

    lines["all"] = "All & "

    thresholds_line = "".join([str(t) + " & " for t in thresholds])


    for threshold in thresholds:
        success_t = 0
        total_t = 0
        for observed_ip in observed_ips:
            x = observation_results[threshold][observed_ip]  # alias
            success_i = x["TP"] + x["TN"]
            total_i = x["TP"] + x["TN"] + x["FP"] + x["FN"]
            success_t += success_i
            total_t += total_i
            accuracy = success_i/total_i
            lines[observed_ip] += str(accuracy) + " & "

        accuracy = success_t / total_t
        lines["all"] += str(accuracy) + " & "

    print("Thresholds" + thresholds_line[:-2] + "\\\\")
    print("\\hline")
    for ip in lines.keys():
        print(lines[ip][:-2] + "\\\\")
        print("\\hline")


def find_best_threshold_long_table(observation_results: dict):
    thresholds = sorted(list(observation_results.keys()))
    first_threshold = thresholds[0]
    observed_ips = list(observation_results[first_threshold].keys())

    lines = {observed_ip: str(observed_ip) + " & " for observed_ip in observed_ips}
    lines["all"] = "All & "

    top_line = "Threshold & " + "".join([ip + " & " for ip in observed_ips]) + "All \\\\"
    print(top_line)
    print("\\hline")
    print("\\hline")

    for threshold in thresholds:
        success_t = 0
        total_t = 0

        t_line = ""
        t_line += str(threshold) + " & "
        for observed_ip in observed_ips:
            x = observation_results[threshold][observed_ip]  # alias
            success_i = x["TP"] + x["TN"]
            total_i = x["TP"] + x["TN"] + x["FP"] + x["FN"]
            success_t += success_i
            total_t += total_i
            accuracy = success_i/total_i
            t_line += str(accuracy) + " & "

        accuracy = success_t / total_t
        t_line += str(accuracy) + " \\\\"
        print(t_line)
        print("\\hline")


def create_enormous_table(data):
    # expected input is data[ip1, ip2, all] = accuracy
    thresholds = list(data.keys())
    weights = list(data[thresholds[0]].keys())
    ips = ["1.1.1.10", "1.1.1.11", "all"]
    ip_names = {"1.1.1.10": "1.1.1.10", "1.1.1.11": "1.1.1.11", "all": "All"}
    cline = "\\cline{2-" + str(len(thresholds) + 2) + "}"
    thickhline = "\\thickhline"

    # prepare table width
    column_specs = "|c|c\"" + ("c|" * len(thresholds))
    print(column_specs)

    print(thickhline)

    # make header
    header = "\multicolumn{2}{|c\"}{\\backslashbox{$w$}{$T$}} & " + "".join([str(t) + " & " for t in thresholds])[:-2] + "\\\\"
    print(header)

    print(thickhline)

    for w in weights:
        lines = {ip: "" for ip in ips}

        # initialize multiline headers
        lines[ips[0]] += "\multirow{3}{*}{" + str(w) + "} & " + ip_names[ips[0]]
        for ip in ips[1:]:
            lines[ip] += " & " + ip_names[ip]

        # fill lines with data
        for t in thresholds:
            for ip in ips:
                lines[ip] += " & " + str(data[t][w][ip])

        # end lines and print them
        for ip in ips[:-1]:
            lines[ip] += "\\\\" + cline
            print(lines[ip])

        # print last line with a thick separator
        ip = ips[-1]
        lines[ip] += "\\\\" + thickhline
        print(lines[ip])
