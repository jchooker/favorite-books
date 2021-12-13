def title_strip(newtitlestr, dbstr):
        newtitlestr = (newtitlestr.casefold()).replace(" ","")
        dbstr = (dbstr.casefold()).replace(" ","")
        # for title_test in dbstr:
        #     if title_test
        #how to test all of the titles specif in the db against em
        return newtitlestr == dbstr