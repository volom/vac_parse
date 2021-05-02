import datetime
def fill_base(base, write, link=None):
    with open(str(base), 'a') as b:
        b.write(''.join([str(datetime.datetime.now()),'\n',link,'\n', write, '\n-------------------------------------', '\r\n']))
    b.close

def drop_dupl_base(base, newline='\r\n'):
    with open(base, newline = newline) as result:
            uniqlines = set(result.readlines())
            with open(base, 'w', newline = newline) as rmdup:
                rmdup.writelines(set(uniqlines), newline=newline)
