# This file is part of grammar-to-md
# Copyright (C) 2021  Natan Junges <natanajunges@gmail.com>
#
# grammar-to-md is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# grammar-to-md is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with grammar-to-md.  If not, see <https://www.gnu.org/licenses/>.

def generate(input, terminals = {}, title = None):
    input = input.replace("\r\n", "\n")
    input = input.replace("\n\r", "\n")
    input = input.replace("\r", "\n")
    input = input.replace("_", "\\_")
    input = input.replace("*", "\\*")
    lines = input.split("\n")
    production = ""

    for l in range(len(lines)):
        line = lines[l]

        if line == "--":
            line += "-"
            lines[l] = line
        elif len(line) > 1 and line[-1] == ":":
            production = line[:-1]
            line = ("## " if title != None else "# ") + line
            lines[l] = line
        elif ((len(line) > 8 and line[0:8] == " " * 8 and line[8].isprintable() and line[8] != " ") or
              (len(line) > 4 and line[0:4] == " " * 4 and line[4].isprintable() and line[4] != " ") or
              (len(line) > 2 and line[0:2] == " " * 2 and line[2].isprintable() and line[2] != " ") or
              (len(line) > 1 and line[0] in [" ", "\t"] and line[1].isprintable() and line[1] != " ")):
            line = line.lstrip(" \t")

            if line == "(one of)":
                line = "_" + line + "_  "
            else:
                i = 0

                while i < len(line):
                    if line[i] == "\\":
                        i += 2
                    elif line[i] == "\"":
                        i += 1

                        while i < len(line):
                            if line[i] == "\\":
                                i += 2
                            elif line[i] == "\"":
                                i += 1
                                break
                            else:
                                i += 1
                    elif line[i].isalpha():
                        j = i + 1

                        while j < len(line) and line[j].isalnum():
                            j += 1

                        symbol = line[i:j]

                        if symbol == production or symbol in terminals:
                            symbol = "_" + symbol + "_"
                            line = line[:i] + symbol + line[j:]

                        i += len(symbol)
                    else:
                        i += 1

                i = 0

                while i < len(line):
                    if line[i] == "\\":
                        i += 2
                    elif line[i] == "\"":
                        i += 1

                        while i < len(line):
                            if line[i] == "\\":
                                i += 2
                            elif line[i] == "\"":
                                i += 1
                                break
                            else:
                                i += 1
                    elif line[i] in ["[", "]", "{", "}"]:
                        if (((i == 0 or line[i - 1] not in ["*", "\"", "_"]) and
                             (i < len(line) - 1 and line[i + 1] == "_")) or
                            ((i > 0 and line[i - 1] == "_") and
                             (i == len(line) - 1 or line[i + 1] not in ["*", "\""]))):
                            symbol = "*" + line[i] + "*"
                        else:
                            symbol = "_" + line[i] + "_"

                        line = line[:i] + symbol + line[i + 1:]
                        i += 3
                    else:
                        i += 1

                i = 0

                while i < len(line):
                    if line[i] == "\\":
                        i += 2
                    elif line[i] == "\"":
                        i += 1

                        while i < len(line):
                            if line[i] == "\\":
                                i += 2
                            elif line[i] == "\"":
                                i += 1
                                break
                            else:
                                i += 1
                    elif line[i].isalpha():
                        j = i + 1

                        while j < len(line) and line[j].isalnum():
                            j += 1

                        symbol = line[i:j]

                        if symbol != production and symbol not in terminals:
                            symbol = "[_" + symbol + "_](#" + symbol + ")"
                            line = line[:i] + symbol + line[j:]

                        i += len(symbol)
                    else:
                        i += 1

                line = line.replace("\"", "**")
                line += "  "

            lines[l] = line

    if title != None:
        lines = ["# " + title, ""] + lines

    return "\n".join(lines)
