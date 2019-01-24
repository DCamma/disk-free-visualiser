import subprocess
import re


class bcolors:
    green = '\033[92m'
    grey = '\033[90m'
    end = '\033[0m'
    black = '\033[30m'


def get_subprocess_out(command):
    p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    (output, err) = p.communicate()
    p_status = p.wait()
    return [output, err, p_status]


def parse_df(output):
    cleanLine = []
    output = output.split("\n")
    maxname = 0

    for line in output:
        if line != "" and "Filesystem" not in line:
            name = line.split()[0]
            maxname = max(len(name), maxname)
            percentage = re.search(
                '([0-9]{1,3})%',
                line
            ).group(0).replace("%", "")
            cleanLine.append([name, percentage])

    return maxname, cleanLine


def show_bar(maxname, cleanLine):
    for line in cleanLine:
        percentage = int(line[1])
        print("{:{}}{}{}{}{}{}".format(
            line[0],
            maxname+2,
            bcolors.green,
            chr(9724)*percentage,
            bcolors.grey,
            chr(9724)*(100-percentage),
            bcolors.end)
        )  # 9608 full block; 9607 seventh eight block; 9724 smaller rectangle


def main():
    output = get_subprocess_out("df -h")[0].decode("utf-8")
    maxname, cleanLine = parse_df(output)
    show_bar(maxname, cleanLine)


if __name__ == "__main__":
    main()
