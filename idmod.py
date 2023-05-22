
def main():
    with(open("id2.txt", "r")) as f:
        lns=f.readlines()
    with(open("idargs.txt", "w")) as f:
        f.writelines(map(lambda l: "'"+l[:-1]+"'\n", lns))
if __name__=='__main__':
    main()
