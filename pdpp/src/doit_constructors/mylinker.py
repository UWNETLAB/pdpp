from os import link, remove

def mylinker(link_start, link_end):
    try:
        link(link_start, link_end)
    except FileExistsError:
        remove(link_end)
        link(link_start, link_end)   

