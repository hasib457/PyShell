import os

def init_shell():
    os.system('cls||clear')
    

def takeInput():
    command = input(f"{os.environ.get('USER')}:{os.getcwd()}$ ").strip()
    if len(command):
        return command
    else:
        return 0

# process user input
def processString(command):
    
    commands = [0,0,0] # first value command flag, second simple command and third pipe command
    builtInCommands = ["cd", "exit"]

    pipe = command.split("|")
    if len(pipe)>1:
        commands[0] = 2 # 1 if it's including a pipe.
        commands[1] = pipe[0].split(maxsplit=1)
        commands[2] = pipe[1].split(maxsplit=1)
        return commands
    else:
        commands[0] = 0
        commands[1] = pipe[0].split(maxsplit=1)

        #handel built-in commands
        if commands[1][0] == builtInCommands[0]: 
            os.chdir(os.path.expanduser(commands[1][1]))
        elif commands[1][0] == builtInCommands[1]:
            os._exit(0) #exit the process

        else:
            commands[0] = 1 # 1 if it is a simple command
            commands[1] = pipe[0].split(maxsplit=1)

        return commands

# execute simple commands
def execArgs(command):
    # Create a child process
    # using os.fork() method 
    pid = os.fork()
    if pid == -1:
        print("\nFailed forking child..")
        return
    elif pid == 0:
        try:
            # Usually, the first parameter of an argument list (sys.argv) is the command 
            os.execvp(command[0], command)
            os._exit(0) #exit the process
        except:
            print("\nCould not execute command..")
    else:
        #  waiting for child to terminate
        os.wait()

    
# execute the pipe system commands
def execArgsPiped(command):
   
    # Create a pipe
    r, w = os.pipe() # The returned file descriptor r and w

    p1 = os.fork()
    if p1 == -1:
        print("\nFailed forking child..")
        return
    elif p1 == 0:
        #  Child 1 executing..
		#  It only needs to write at the write end
        os.close(r)
        os.dup2(w, 1)
        os.close(w)
        try:
            os.execvp(command[1][0], command[1])
            os._exit(0) #exit the process
        except:
            print("\nCould not execute command..")
    else:
        # Parent executing
        p2 = os.fork()
        #  Child 2 executing..
		#  It only needs to read at the read end
        # Closes file descriptor w
        if p2 == -1:
            print("\nFailed forking child..")
            return
        elif p2 == 0:
            # Child 2 executing..
		    # It only needs to read at the read end
            os.close(w)
            os.dup2(r, 0)
            os.close(r)
            try:
                os.execvp(command[2][0], command[2])
                os._exit(0) #exit the process
            except:
                print("\nCould not execute command..")
        else:
            # parent executing, waiting for  children
            os.wait()
            os.wait()

            
# main func   
def main():
    init_shell() #init shell

    while True:
        try:
            command = takeInput()
            if command:
                 # return list of command first value 1 for a simple command, 2 for a pipe.
                commands = processString(command)
                if commands[0]==1:
                    execArgs(commands[1])

                elif commands[0] == 2:
                    execArgsPiped(commands)
        except KeyboardInterrupt:
            os.system('cls||clear')
            os._exit(0)


if __name__=="__main__":
    main()
