import time
import aexpect

import utils_misc
import process


def handle_prompts(session, username, password, prompt, timeout=10):
    """
    Connect to a remote host (guest) using SSH or Telnet or else.
    Wait for questions and provide answers.  If timeout expires while
    waiting for output from the child (e.g. a password prompt or
    a shell prompt) -- fail.
    :param session: An Expect or ShellSession instance to operate on
    :param username: The username to send in reply to a login prompt
    :param password: The password to send in reply to a password prompt
    :param prompt: The shell prompt that indicates a successful login
    :param timeout: The maximal time duration (in seconds) to wait for each
            step of the login procedure (i.e. the "Are you sure" prompt, the
            password prompt, the shell prompt, etc)
    :raise LoginTimeoutError: If timeout expires
    :raise LoginAuthenticationError: If authentication fails
    :raise LoginProcessTerminatedError: If the client terminates during login
    :raise LoginError: If some other error occurs
    :return: If connect succeed return the output text to script for further
             debug.
    """
    password_prompt_count = 0
    login_prompt_count = 0

    output = ""
    while True:
        try:
            match, text = session.read_until_last_line_matches(
                [r"[Aa]re you sure", r"[Pp]assword:\s*",
                 # Prompt of rescue mode for Red Hat.
                 r"\(or (press|type) Control-D to continue\):\s*$",
                 r"[Gg]ive.*[Ll]ogin:\s*$",  # Prompt of rescue mode for SUSE.
                 r"(?<![Ll]ast )[Ll]ogin:\s*$",  # Don't match "Last Login:"
                 r"[Cc]onnection.*closed", r"[Cc]onnection.*refused",
                 r"[Pp]lease wait", r"[Ww]arning", r"[Ee]nter.*username",
                 r"[Ee]nter.*password", r"[Cc]onnection timed out", prompt,
                 r"Escape character is.*"],
                timeout=timeout, internal_timeout=0.5)
            output += text
            if match == 0:  # "Are you sure you want to continue connecting"
                session.sendline("yes")
                continue
            elif match in [1, 2, 3, 10]:  # "password:"
                if password_prompt_count == 0:
                    session.sendline(password)
                    password_prompt_count += 1
                    continue
                else:
                    raise ValueError("Got password prompt twice",
                                                   text)
            elif match == 4 or match == 9:  # "login:"
                if login_prompt_count == 0 and password_prompt_count == 0:
                    session.sendline(username)
                    login_prompt_count += 1
                    continue
                else:
                    if login_prompt_count > 0:
                        msg = "Got username prompt twice"
                    else:
                        msg = "Got username prompt after password prompt"
                    raise ValueError(msg, text)
            elif match == 5:  # "Connection closed"
                raise ValueError("lient said 'connection closed'", text)
            elif match == 6:  # "Connection refused"
                raise ValueError("Cient said 'connection refused'", text)
            elif match == 11:  # Connection timeout
                raise ValueError("Client said 'connection timeout'", text)
            elif match == 7:  # "Please wait"
                timeout = 30
                continue
            elif match == 8:  # "Warning added RSA"
                continue
            elif match == 12:  # prompt
                break
            elif match == 13:  # console prompt
                session.sendline()
        except aexpect.ExpectTimeoutError as e:
            raise ValueError(e.output)
        except aexpect.ExpectProcessTerminatedError as e:
            raise ValueError(e.status, e.output)

    return output


def remote_login(client, host, port, username, password, prompt, linesep="\n",
                 timeout=10, interface=None,
                 status_test_command="echo $?", verbose=False, use_key=False):
    """
    Log into a remote host (guest) using SSH/Telnet/Netcat.
    :param client: The client to use ('ssh', 'telnet' or 'nc')
    :param host: Hostname or IP address
    :param port: Port to connect to
    :param username: Username (if required)
    :param password: Password (if required)
    :param prompt: Shell prompt (regular expression)
    :param linesep: The line separator to use when sending lines
            (e.g. '\\n' or '\\r\\n')
    :param timeout: The maximal time duration (in seconds) to wait for
            each step of the login procedure (i.e. the "Are you sure" prompt
            or the password prompt)
    :interface: The interface the neighbours attach to (only use when using ipv6
                linklocal address.)
    :param status_test_command: Command to be used for getting the last
            exit status of commands run inside the shell (used by
            cmd_status_output() and friends).
    :raise LoginError: If using ipv6 linklocal but not assign a interface that
                       the neighbour attache
    :raise LoginBadClientError: If an unknown client is requested
    :raise: Whatever handle_prompts() raises
    :return: A ShellSession object.
    """
    if host and host.lower().startswith("fe80"):
        if not interface:
            raise ValueError("When using ipv6 linklocal an interface must "
                             "be assigned")
        host = "%s%%%s" % (host, interface)

    verbose = verbose and "-vv" or ""
    if client == "ssh":
        if not use_key:
            cmd = ("ssh %s -o UserKnownHostsFile=/dev/null "
                   "-o StrictHostKeyChecking=no "
                   "-o PreferredAuthentications=password -p %s %s@%s" %
                   (verbose, port, username, host))
        else:
            cmd = ("ssh %s -o UserKnownHostsFile=/dev/null "
                   "-o StrictHostKeyChecking=no "
                   "-p %s %s@%s" %
                   (verbose, port, username, host))
    elif client == "telnet":
        cmd = "telnet -l %s %s %s" % (username, host, port)
    elif client == "nc":
        cmd = "nc %s %s %s" % (verbose, host, port)
    else:
        raise ValueError(client)

    if verbose:
        print("Login command: '%s'", cmd)
    session = aexpect.ShellSession(cmd, linesep=linesep, prompt=prompt,
                                   status_test_command=status_test_command)
    if use_key and not password:
        password = ""

    try:
        handle_prompts(session, username, password, prompt, timeout)
    except Exception:
        session.close()
        raise

    return session


def wait_for_login(client, host, port, username, password, prompt,
                   linesep="\n", timeout=240,
                   internal_timeout=10, interface=None, use_key=False):
    """
    Make multiple attempts to log into a guest until one succeeds or timeouts.
    :param timeout: Total time duration to wait for a successful login
    :param internal_timeout: The maximum time duration (in seconds) to wait for
                             each step of the login procedure (e.g. the
                             "Are you sure" prompt or the password prompt)
    :interface: The interface the neighbours attach to (only use when using ipv6
                linklocal address.)
    :see: remote_login()
    :raise: Whatever remote_login() raises
    :return: A ShellSession object.
    """

    end_time = time.time() + timeout
    verbose = False
    while time.time() < end_time:
        try:
            return remote_login(client, host, port, username, password, prompt,
                                linesep, internal_timeout,
                                interface, verbose=verbose, use_key=use_key)
        except Exception:
            verbose = True
        time.sleep(2)
    # Timeout expired; try one more time but don't catch exceptions
    return remote_login(client, host, port, username, password, prompt,
                        linesep, internal_timeout, interface, use_key=use_key)


class RemoteRunner(object):
    """
    Class to provide a utils.run-like method to execute command on
    remote host or guest. Provide a similar interface with utils.run
    on local.
    """

    def __init__(self, client="ssh", host=None, port="22", username="root",
                 password=None, prompt=r"[\#\$]\s*$", linesep="\n",
                 timeout=240, internal_timeout=10,
                 session=None, use_key=False):
        """
        Initialization of RemoteRunner. Init a session login to remote host or
        guest.
        :param client: The client to use ('ssh', 'telnet' or 'nc')
        :param host: Hostname or IP address
        :param port: Port to connect to
        :param username: Username (if required)
        :param password: Password (if required)
        :param prompt: Shell prompt (regular expression)
        :param linesep: The line separator to use when sending lines
                (e.g. '\\n' or '\\r\\n')
        :param timeout: Total time duration to wait for a successful login
        :param internal_timeout: The maximal time duration (in seconds) to wait
                for each step of the login procedure (e.g. the "Are you sure"
                prompt or the password prompt)
        :param session: An existing session
        :see: wait_for_login()
        :raise: Whatever wait_for_login() raises
        """
        self.host = host
        self.username = username
        self.password = password
        if session is None:
            if host is None:
                raise ValueError(
                    "Neither host, nor session was defined!")
            self.session = wait_for_login(client, host, port, username,
                                          password, prompt, linesep,
                                          timeout,
                                          internal_timeout, use_key=use_key)
        else:
            self.session = session
        # Init stdout pipe and stderr pipe.
        random_pipe = utils_misc.generate_random_string(6)
        self.stdout_pipe = '/tmp/cmd_stdout_%s' % random_pipe
        self.stderr_pipe = '/tmp/cmd_stderr_%s' % random_pipe

    def run(self, command, timeout=60, ignore_status=False, internal_timeout=None):
        """
        Method to provide a utils.run-like interface to execute command on
        remote host or guest.
        :param timeout: Total time duration to wait for command return.
        :param ignore_status: If ignore_status=True, do not raise an exception,
                              no matter what the exit code of the command is.
                              Else, raise CmdError if exit code of command is not
                              zero.
        """
        # Redirect the stdout and stderr to file, Deviding error message
        # from output, and taking off the color of output. To return the same
        # result with utils.run() function.
        command = "%s 1>%s 2>%s" % (
            command, self.stdout_pipe, self.stderr_pipe)
        status, _ = self.session.cmd_status_output(command, timeout=timeout,
                                                   internal_timeout=internal_timeout)
        output = self.session.cmd_output("cat %s;rm -f %s" %
                                         (self.stdout_pipe, self.stdout_pipe))
        errput = self.session.cmd_output("cat %s;rm -f %s" %
                                         (self.stderr_pipe, self.stderr_pipe))
        cmd_result = process.CmdResult(command=command, exit_status=status,
                                       stdout=output, stderr=errput)
        if status and (not ignore_status):
            raise process.CmdError(command, cmd_result)
        return cmd_result
