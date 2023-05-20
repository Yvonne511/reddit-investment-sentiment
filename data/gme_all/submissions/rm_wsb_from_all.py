import os

wsb = set()
with open("gme_submissions_wsb.csv", "r") as f:
    f.readline()
    line = f.readline()
    while line:
        wsb.add(line.strip())
        line = f.readline()
        
with open("gme_no_wsb.csv", "w") as f_out:
    with open("gme_submissions_allreddit.csv", "r") as f:
        title = f.readline()
        f_out.write(title)
        line = f.readline()
        while line:
            if line.strip() in wsb:
                line = f.readline()
            else:
                f_out.write(line)
                line = f.readline()

    