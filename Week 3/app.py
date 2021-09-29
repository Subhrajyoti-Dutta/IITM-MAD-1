import sys
import pyhtml as h
import matplotlib.pyplot as plt

def count(arr):
    dictionary = dict()
    for i in arr:
        dictionary[i] = dictionary.setdefault(i,0) + 1

    return dictionary.keys(), dictionary.values()

def s(data):
    t = h.html(
        h.head(
            h.title(
                'Student Data'
            )
        ),
        h.body(
            h.h1(
                "Course Details"
            ),
            h.table(border = '1')(
                h.tr(
                    h.th(i) for i in ["Student id","Course id","Marks"]
                ),
                (h.tr(
                    h.td(j) for j in i
                ) for i in data[1:]),
                h.tr(
                    h.td(colspan='2')(
                        'Total Marks'
                    ),
                    h.td(
                        str(sum(int(i[2]) for i in data[1:]))
                    )
                )
            )
        )
    )
    return t.render()

def c(mean, high, plot):
    t = h.html(
        h.head(
            h.title(
                "Course Data"
            )
        ),
        h.body(
            h.h1(
                "Course Details"
            ),
            h.table(border='1')(
                h.tr(
                    h.th("Average Marks"),
                    h.th("Maximum Marks")
                ),
                h.tr(
                    h.td(mean),
                    h.td(high)
                )
            ),
            h.img(
                src='fig.png'
            )
        )
    )

    return t.render()
    

def wrong():
    t = h.html(
        h.head(
            h.title(
                "Something Went Wrong"
            )
        ),
        h.body(
            h.h1(
                "Wrong Inputs"
            ),
            h.p(
                "Something went wrong"
            )
        )
    )
    return t.render()

req = sys.argv[1]
req_id = sys.argv[2]
with open('data.csv', 'r') as fl:
    data = [i[:-1].split(', ') for i in fl]
    res = list()
    if req == '-s':
        res.extend([ i for i in data if req_id == i[0] ])
        if res:
            html = s(res)
        else:
            html = wrong()
    elif req == '-c':
        res.extend([ int(i[2]) for i in data if req_id == i[1] ])
        plt.bar(*count(res),width=5)
        plt.ylabel("Frequency")
        plt.xlabel("Marks")
        figname = "fig.png"
        plt.savefig(figname)
        if res:
            avg, maxm = sum(res)/len(res), max(res)
            html = c(avg, maxm, figname)
        else:
            html = wrong()
    else:
        html = wrong()
    with open('index.html', 'w') as webpage:
        webpage.write(html)