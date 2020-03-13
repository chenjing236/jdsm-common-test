
class CmdError(Exception):

    def __init__(self, command=None, result=None, additional_text=None):
        self.command = command
        self.result = result
        self.additional_text = additional_text

    def __str__(self):
        if self.result is not None:
            if self.result.interrupted:
                msg = "Command '%s' interrupted by %s"
                msg %= (self.command, self.result.interrupted)
            elif self.result.exit_status is None:
                msg = "Command '%s' failed and is not responding to signals"
                msg %= self.command
            else:
                msg = "Command '%s' failed (rc=%d)"
                msg %= (self.command, self.result.exit_status)
            if self.additional_text:
                msg += ", " + self.additional_text
            return msg
        else:
            return "CmdError"


class CmdResult(object):

    """
    Command execution result.
    :param command: String containing the command line itself
    :param exit_status: Integer exit code of the process
    :param stdout: String containing stdout of the process
    :param stderr: String containing stderr of the process
    :param duration: Elapsed wall clock time running the process
    :param pid: ID of the process
    """

    def __init__(self, command="", stdout="", stderr="",
                 exit_status=None, duration=0, pid=None):
        self.command = command
        self.exit_status = exit_status
        self.stdout = stdout
        self.stderr = stderr
        self.duration = duration
        self.interrupted = False
        self.pid = pid

    def __repr__(self):
        cmd_rep = ("Command: %s\n"
                   "Exit status: %s\n"
                   "Duration: %s\n"
                   "Stdout:\n%s\n"
                   "Stderr:\n%s\n"
                   "PID:\n%s\n" % (self.command, self.exit_status,
                                   self.duration, self.stdout, self.stderr,
                                   self.pid))
        if self.interrupted:
            cmd_rep += "Command interrupted by %s\n" % self.interrupted
        return cmd_rep
