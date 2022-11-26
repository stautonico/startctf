---
title: startctf
section: 1
header: User Commands
footer: startctf 2.0.0
date: November 26, 2022
---
# NAME
startctf - Create a CTF template and automate some common tasks

# SYNOPSIS
**startctf** [OPTION(s)]... \[NAME\] [\-\-version] [\-\-help, \-h] [\-\-install\-manpage]

# DESCRIPTION
**startctf** is a small utility that creates template directory/file structures to help you organize your CTF
challenges. It also automates some common tasks such as running network scans (using tools like nmap, rustscan, etc.)
and fuzzing web applications (using tools like ffuf, gobuster, etc.).

# OPTIONS
**\-\-install\-manpage**
: Download and installs the manpage (from the GitHub repository). Requires root privileges.

**\-f, \-\-force**
: Forcefully overwrite existing files/directories. (Caution: This option is dangerous and can cause data loss.)

**\-\-ip \<IP\>**
: Specify the IP address of the target machine. This option isn't required, but scanning/fuzzing/running tools won't
work.

**\-nS, \-\-nmap\-scan**
: Run a nmap scan on the target machine. Requires the **\-\-ip** option.

**\-as, \-\-auto\-scan**
: Try to detect which services are running on the target machine and run the appropriate scan. Requires the
: **\-\-ip** and either **\-nS** or **\-nSA** options.

**\-s, \-\-silent**
: Don't show any output from any of the tools or the script itself.

**\-st, \-\-silent\-tools**
: Only silence output from tools, but still show status messages. Will also prevent xterm windows from opening
: containing tool output.

**\-nw \-\-no\-warnings**
: Don't show any warnings.


**\-h, \-\-help**
: Show the help message and exit

**\-V, \-\-version**
: Show version information and exit

## NMAP OPTIONS
Options specific to nmap scans. These options are only used if the **\-nS** or **\-nSA** options are used. **\-\-ip** is
required.

**\-nSA, \-\-nmap\-all**
: Run a full nmap scan on the given IP (all ports, slow.)

**\-\-nmap\-Pn**
: Don't ping the target (pass the **\-Pn** option to nmap)

**\-nSV, \-\-no\-sV**
: Don't detect the version of services running on the target machine (don't pass the **\-sV** option to nmap.)

**\-nmap-ep, \-\-nmap\-exclude\-ports \<PORTS\>**
: Ports to exclude from the nmap scan. **\<PORTS\>** should be a comma-separated list of ports or port ranges (or a
: single number.)

**\-\-nmap\-args \<NMAP_ARGS\>**
: Pass additional arguments to nmap. **\<NMAP_ARGS\>** should be a string of arguments.

## FFUF OPTIONS
Options specific to ffuf scans. These options are only used if the **\-as** option is used.

**\-\-ffuf\-args \<FFUF_ARGS\>**
: Pass additional arguments to ffuf. **\<FFUF_ARGS\>** should be a string of arguments.

## GOBUSTER OPTIONS
Options specific to gobuster scans. These options are only used if the **\-as** option is used.

**\-\-gobuster\-args \<GOBUSTER\>**
: Pass additional arguments to gobuster. **\<GOBUSTER_ARGS\>** should be a string of arguments.

# EXAMPLES
**TODO: Add examples**

# AUTHOR
**startctf** was written by **stautonico**. You can find the source code on [GitHub](https://github.com/stautonico/startctf)

# BUGS
If you find any bugs, please report them on [GitHub issues](https://github.com/stautonico/startctf/issues).

# LICENSE
**startctf** is licensed under the MIT license. See the LICENSE file for more information. (https://github.com/stautonico/startctf/blob/main/LICENSE)