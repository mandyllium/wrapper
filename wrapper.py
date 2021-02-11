#! /usr/bin/python3

import subprocess
import os
import logging
import sys

# Getting list of input csv files and python file in specific directory 
def list_all_files_in_directory(fe, fo, path, ip_py_pattern, ip_csv_pattern):
    input_file = []
    py_file = []

    if not os.path.exists(path):
        fe.write("Path {} doesn't exsists.".format(path))
        fo.write("Path {} doesn't exsists.".format(path))
        fo.close()
        fe.close()
        raise Exception("Path {} doesn't exsists.".format(path))

    for file in os.listdir(path):
        if file.startswith(ip_csv_pattern) and file.endswith(".csv"):
            input_file.append(file)
        if file.startswith(ip_py_pattern) and file.endswith(".py"):
            py_file.append(file)

    if len(py_file) == 0:
        fe.write("No python executable files found at path {}".format(path))
        fo.write("No python executable files found at path {}".format(path))
        fo.close()
        fe.close()
        raise Exception("No python executable files found at path {}".format(path))

    if len(input_file) == 0:
        fe.write("No files found at path {}".format(path))
        fo.write("No files found at path {}".format(path))
        fo.close()
        fe.close()
        raise Exception("No pfiles found at path {}".format(path))

    return sorted(py_file),sorted(input_file)

def check_outputfile(fe, fo, path, op_csv_pattern, counter):

    if not os.path.exists(path):
        fe.write("Path {} doesn't exsists.".format(path))
        fo.write("Path {} doesn't exsists.".format(path))
        fo.close()
        fe.close()
        raise Exception("Path {} doesn't exsists.".format(path))
    else:
        os.chdir(path)
        if not os.path.isfile(op_csv_pattern + str(counter+1) + '.csv'):
            fe.write("Output file {} not created".format(op_csv_pattern + str(counter) + '.csv'))
            fo.write("Output file {} not created".format(op_csv_pattern + str(counter) + '.csv'))
            fo.close()
            fe.close()
            return False
        else:
            return True


def main(path, ip_py_pattern, ip_csv_pattern, op_csv_pattern):


    # Creating log files for output and error
    fo=open("out.log","w")
    fe=open("err.log","w")

    py_files, ip_files = list_all_files_in_directory(fe, fo, "./","file","ifile")

    for i in range(0,len(py_files)):
        fa=(os.path.exists(py_files[i]) and os.path.getsize(py_files[i])) 
        if not fa:
            fe.write("Error running the script\n")
            fo.write("Python file {} is not present or empty".format(py_files[i]))
            fo.close()
            fe.close()
            raise Exception("Python file {} is not present or empty".format(py_files[i]))
            #exit(1)
        #for i in range(1,len(ip_files)+1):
        #print(ip_py_pattern + str(i+1) + '.csv')
        fc=(os.path.isfile(ip_csv_pattern + str(i+1) + '.csv') and os.path.getsize(ip_csv_pattern + str(i+1) + '.csv'))
        if fc == False:
            fe.write("Error running the script\n")
            fo.write("Input file {} is not present or empty".format(ip_csv_pattern + str(i+1) + '.csv'))
            fo.close()
            fe.close()
            raise FileNotFoundError("Input file {} is not present or empty".format(ip_csv_pattern + str(i+1) + '.csv'))
        # except IndexError:
        #     fe.write("Input file {} is not present".format(ip_py_pattern + str(i+1) + '.csv'))
        #     fo.write("Input file {} is not present".format(ip_py_pattern + str(i+1) + '.csv'))
        #     fe.close()
        #     fo.close()
        #     print("Input file {} is not present".format(ip_py_pattern + str(i+1) + '.csv'))
        #     print("Exiting...")
        #     exit(1)
        
        response=subprocess.run([sys.executable,py_files[i]],capture_output=True)
        if response.returncode and response.stderr:
            #print("Error running the script {}. Exiting...\n".format(py_files[i]))
            for output in response.stdout.decode():
                fo.write(output)
            for error in response.stderr.decode():
                fe.write(error)
            fo.close()
            fe.close()
            raise Exception("Error running the script {}.\nCheck Error Logs.\nExiting...\n".format(py_files[i]))

        result = check_outputfile(fe, fo, path, op_csv_pattern, i)
        if result == False:
            raise Exception(("Output file {} not created".format(op_csv_pattern + str(i+1) + '.csv')))
        else:
            fo.write("Completed script {} and out as below:\n".format(py_files[i]))
            for o in response.stdout.decode():
                fo.write(o)

        # fb=(os.path.exists(op_files[i]) and os.path.getsize(op_files[i]))
        # if not fb:
        #     fe.write("Error running the script\n")
        #     fe.write("Output file {} is not present or empty".format(op_files[i]))
        #     fo.close()
        #     fe.close()
        #     exit(1)

    fo.close()
    fe.close()
    print("Script executed successfully")
    exit(0)


if __name__ == "__main__":

    main(os.getcwd(), 'file', 'ifile', 'ofile')