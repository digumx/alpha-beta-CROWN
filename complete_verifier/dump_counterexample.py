"""
Some code written by Sanaa to dump out cex
"""
import torch
import os


def dump_cex_to_file(file_name, cex):
    try:
        os.system("rm /home/testing/oct22/semantic-neuron-merge/cex.txt")
        with open(file_name, 'w') as file:
            for i, cex_i in enumerate(cex):
                if i == 0:
                    file.write("((X_{} {})\n".format(i, cex_i))
                elif i==len(cex)-1:
                    file.write("(X_{} {}))\n".format(i, cex_i))
                else:
                    file.write("(X_{} {})\n".format(i, cex_i))
    except:
        print("File could not be opened")
