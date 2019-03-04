import subprocess
import sys
import re


bashColor = {
    0: "\033[39m",   # Default
    1: "\033[30m",   # Black
    2: "\033[31m",   # Red
    3: "\033[32m",   # Green
    4: "\033[33m",   # Yellow
    5: "\033[34m",   # Blue
    6: "\033[35m",   # Magenta
    7: "\033[36m",   # Cyan
    8: "\033[37m",   # LightGray
    9: "\033[90m",   # DarkGray
    10: "\033[91m",  # LightRed
    11: "\033[92m",  # LightGreen
    12: "\033[93m",  # LightYellow
    13: "\033[94m",  # LightBlue
    14: "\033[95m",  # LightMagenta
    15: "\033[96m",  # LightCyan
    16: "\033[97m",  # White
    99: '\033[0m'    # end
}


class PartitionInfo:
    def __init__(self, name, percentage, avilable, total):
        self.name = name
        self.percentage = percentage
        self.avilable = avilable
        self.total = total


def get_subprocess_out(command):
    p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    (output, err) = p.communicate()
    p_status = p.wait()
    return [output, err, p_status]


def parse_df(output):
    clean_line = []
    output = output.split("\n")
    max_len = 0

    header = output[0].split()
    i_available = header.index('Avail')
    i_size = header.index('Size')

    len_header = len(header)

    for line in output:
        if line != "" and "Filesystem" not in line:
            pad = 0
            percentage = re.search(
                '([0-9]{1,3})%',
                line
            ).group(0).replace("%", "")
            line = line.split()
            name = line[0]
            if len(line) >= len_header:
                pad = 1
                name = name+" "+line[1]
            max_len = max(len(name), max_len)
            clean_line.append(PartitionInfo(
                name, int(percentage), line[i_available+pad], line[i_size+pad]))

    return max_len, clean_line


def show_bar(max_len, partitions_list, divis=1, color=0):
    print("{:{}} {:>6}{:>6}".format(
        "Name",
        max_len,
        "Total",
        "Avail",
    ))
    for partition in partitions_list:
        print("{:{}} {:>6}{:>6} {}{}{}{}{}".format(
            partition.name,
            max_len,
            partition.total,
            partition.avilable,
            bashColor[color],
            chr(9724)*(partition.percentage//divis),
            bashColor[9],
            chr(9724)*((100//divis)-(partition.percentage//divis)),
            bashColor[99])
        )  # 9608 full block; 9607 seventh eight block; 9724 smaller rectangle


def main():
    color = 0
    divisor = 1
    if len(sys.argv) > 1:
        try:
            color = int(sys.argv[sys.argv.index("-c")+1]) % 17
        except ValueError:
            print("{}Ignored invalid argument for \'color\'. Default set to {}{}".format(
                bashColor[4],
                color,
                bashColor[99]
            ))
        try:
            divisor = int(sys.argv[sys.argv.index("-l")+1])
        except ValueError:
            print("{}Ignored invalid argument for \'divisor\'. Default set to {}{}".format(
                bashColor[4],
                divisor,
                bashColor[99]
            ))

    output = get_subprocess_out("df -h")[0].decode("utf-8")
    max_len, clean_line = parse_df(output)
    show_bar(max_len, clean_line, divisor, color)


if __name__ == "__main__":
    main()
