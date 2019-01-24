import subprocess


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

    for line in output:
        if "Filesystem" not in line:
            line = line.split()
            if len(line) >= 4 and line[4].find('%') != -1:
                cleanLine.append([line[0], line[4].replace("%", "")])

    return cleanLine


def show_bar(cleanLine):
    for line in cleanLine:
        percentage = int(line[1])
        print("{:25}{}{}{}{}{}".format(line[0], bcolors.green,
                                       chr(9724)*percentage, bcolors.grey, chr(9724)*(100-percentage), bcolors.end))
        # 9608 full block; 9607 seventh eight block; 9724 smaller rectangle


def main():
    output = get_subprocess_out("df -h")[0].decode("utf-8")
    show_bar(parse_df(output))


if __name__ == "__main__":
    main()
