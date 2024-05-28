import configparser
import re
import subprocess

config = configparser.ConfigParser()
config.read("misiones_exiliados.config")



git_folder='"{}"'.format(config["DEFAULT"]["directorio_repositorio"])
mission_folder='"{}"'.format(config["DEFAULT"]["directorio_misiones"])

DEBUG=""
if config["DEFAULT"].getboolean("debug") == True:
    DEBUG = "/L"


#handle -a -p DCS "\Users\Administrator\Saved Games\DCS.openbeta_server\Missions" -nobanner
#DCS.exe            pid: 6044   type: File           884: C:\Users\Administrator\Saved Games\DCS.openbeta_server\Missions\Practica_IADS&MOOSE_Caucaso_v2.0 Dia.miz
cmd = 'handle.exe'
result = subprocess.run([cmd,  'Missions', '-nobanner'], shell=False, capture_output=True, text=True, check=True)

exclude = ""
mission_actual = ""
for f in result.stdout.splitlines():
    n = f.replace('\\','/')
    m = re.match("^DCS.*(C:.*miz)$", n)
    if m:
        mission_actual = '"{}"'.format(m.group(1).split("/")[-1])
        exclude  = '/XF'
        
# una vez que hemos identificado la mision actual. 
robocopy = 'robocopy'

#por alguna razon extra;a subprocess esta agregando el path actual a mission_folder cuando ejecuta robocopy
#result = subprocess.run([robocopy, git_folder, mission_folder, "/R:1", "/W:1", "/NP", "/NJH", "/NJS", exclude, mission_actual, DEBUG],
#                     shell=True, capture_output=True, text=True, check=False)
#solucion crear un script nuevo y ejecutar este script
with open("copy_script.bat", "w") as file:
    print("@echo off", file=file)
    print('robocopy {} {} *.miz /R:1 /W:1 /S /NP /NJH /NJS /NDL {} {} {}'.format(git_folder, mission_folder, exclude, mission_actual, DEBUG), file=file)
