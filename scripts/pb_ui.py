import dialog
import os
import time

mydate = str(time.time())

d = dialog.Dialog(dialog="dialog")
def pb_list(pb_dir):
    files = os.listdir(pb_dir)
    pb_list=[]
    for i in files:
        pb_list+=[(i,"",False)]


    code, tags = d.checklist("Please, select pbs",
                             choices=pb_list,
                             title="Playbooks list")
    return sort_pb(tags, pb_dir)

def hosts_list(h_dir):

    code, tag = d.menu("What do you doing?",
                       choices=[("1", "Enter hosts"),
                                ("2", "Select hosts from inventary")])
    if tag == '1':
        c,list = d.inputbox("Enter servername or many split ',' or space", height=None, width=None, init='')
        if ',' in list:
            list=list.split(",")
        else:
            list=list.split()

        return generate_inv(list,h_dir)
    if tag =='2':
        files = os.listdir(h_dir)
        h_list = []
        for i in files:
            h_list += [(i,"")]

        code, tags = d.menu("Please, select host file",
                                 choices=h_list,
                                 title="inventary list")
        i_file = h_dir+tags
        i_list=[]
        with open(i_file, 'r') as inv:
            i_list = [(line,"dd",False) for line in inv.readlines() if line.strip() and not line.startswith("[")]

        c, list = d.checklist("Select hosts",
                             choices=i_list,
                             title="inventory")
        list = [x for x in list if x is not '']
        return generate_inv(list,h_dir)
    return tag

def show_sort_pb(tags,mess="sort by"):
    x,y = d.form(mess,
                 width=50,
                 elements=tags,
                 )
    return y

def sort_pb(list,pb_dir):
    tags = []
    n = 1
    for i in list:
        k = str(n)
        tags += [(i, n, 0, k, n, 20, 5, 0)]
        n = n + 1

    b = show_sort_pb(tags)
    for i in range(len(b)):
        if b[i] in b[i + 1::]:
            b = show_sort_pb(tags, "no dublicate sort key")
    u = {}
    j=0
    for j in range(len(list)):
        u[b[j]] = list[j]
    m = []
    for k in sorted(u.keys()):
        m += [u[k]]
    for i in range(len(m)):
        m[i] = pb_dir + m[i]
    return m

def new_inv(file,h_dir):
    _,f_name = d.inputbox("enter file name",
                          height=8,
                          width=40)
    os.rename(file,h_dir+f_name)


def generate_inv(list, h_dir):
    f_name = h_dir + 'inv_' + mydate
    with open(f_name, 'w') as file:
        for str in list:
            file.write(str)
            file.write('\n')
    return f_name