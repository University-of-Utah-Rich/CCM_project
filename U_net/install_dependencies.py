import sys
import subprocess

def install_dependencies():
    call = None
    if "conda" in sys.executable:
        call = ['conda', 'install', '--yes', '--prefix', sys.prefix, '--file', 'requirements.txt', '--channel=conda-forge']
    else:
        call = [sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt']
    subprocess.check_call(call)
    
if __name__ == "__main__":
    print('Installing requirements')
    install_dependencies()