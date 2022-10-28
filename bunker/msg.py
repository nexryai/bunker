import sys

def info(message):
    sys.stdout.write("\033[32m ✔ \033[0m " + str(message) + "\n")

def error(message):
    sys.stdout.write("\033[31m ✗ \033[0m " + str(message) + "\n")

def fetal_error(message ,e):
    exception = str(e)
    sys.stderr.write("\033[31m" + "=!=========FETAL ERROR=========!=" + "\n")
    sys.stderr.write(str(message) + "\n")
    sys.stderr.write("Exception >>> " + exception+ "\n")
    sys.stderr.write("================================="+ "\033[0m\n")
