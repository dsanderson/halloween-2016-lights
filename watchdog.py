import subprocess

while True:
	command = "arecord -t raw -c 1 -r 8000 -D sysdefault:CARD=C170 -f s8 | python ~/halloween/halloween-2016-lights/fft_vis.py"
	#command = command.split(" ")
	subprocess.call(command, shell=True)
	
