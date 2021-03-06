# This file is part of Alchemist grammar2md
# Copyright (C) 2021  Natan Junges <natanajunges@gmail.com>
#
# Alchemist grammar2md is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Alchemist grammar2md is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Alchemist grammar2md.  If not, see <https://www.gnu.org/licenses/>.

def skip_literal(line, i):
    if line[i] == "\"":
        j = 1

        while i + j < len(line):
            if line[i + j] == "\\":
                j += 2
            elif line[i + j] == "\"":
                j += 1
                break
            else:
                j += 1

        return j
    elif line[i:i+2] == "[^":
        j = 2

        while i + j < len(line):
            if line[i + j] == "]":
                j += 1
                break
            else:
                j += 1

        return j

    return 0

def process_non_terminal(line, i, production, terminals, link=False):
    if line[i].isalpha():
        j = i + 1

        while j < len(line) and line[j].isalnum():
            j += 1

        symbol = line[i:j]

        if link ^ (symbol == production or symbol in terminals):
            if link:
                symbol = "[_" + symbol + "_](#" + symbol + ")"
            else:
                symbol = "_" + symbol + "_"

            line = line[:i] + symbol + line[j:]

        return (line, len(symbol))

    return (None, 0)

def generate(input, level, terminals={}, semantics=None):
    input = input.replace("\r\n", "\n")
    input = input.replace("\n\r", "\n")
    input = input.replace("\r", "\n")
    input = input.replace("_", "\\_")
    input = input.replace("*", "\\*")
    lines = input.split("\n")
    production = ""

    for l in range(len(lines)):
        line = lines[l]

        if line == "---":
            line = "\\" + line
            lines[l] = line
        elif len(line) > 1 and line[-1] == ":":
            production = line[:-1]
            line = "#" * level + " "

            if semantics != None:
                line += "[" + production + "](" + semantics + "#" + production + "):"
            else:
                line += production + ":"

            lines[l] = line
        elif ((len(line) > 8 and line[0:8] == " " * 8 and line[8].isprintable() and line[8] != " ") or
              (len(line) > 4 and line[0:4] == " " * 4 and line[4].isprintable() and line[4] != " ") or
              (len(line) > 2 and line[0:2] == " " * 2 and line[2].isprintable() and line[2] != " ") or
              (len(line) > 1 and line[0] in {" ", "\t"} and line[1].isprintable() and line[1] != " ")):
            line = line.lstrip(" \t")

            if line == "(one of)":
                line = "&emsp;&emsp;_" + line + "_  "
            else:
                i = 0

                while i < len(line):
                    j = skip_literal(line, i)

                    if j > 0:
                        i += j
                    else:
                        line_i = process_non_terminal(line, i, production, terminals)

                        if line_i[1] > 0:
                            line = line_i[0]
                            i += line_i[1]
                        else:
                            i += 1

                i = 0

                while i < len(line):
                    j = skip_literal(line, i)

                    if j > 0:
                        i += j
                    elif line[i] in {"[", "]", "{", "}"}:
                        symbol = "_" + line[i] + "_"
                        line = line[:i] + symbol + line[i + 1:]
                        i += 3
                    else:
                        i += 1

                line = line.replace("__", "")
                line = line.replace("_ _", " ")
                i = 0

                while i < len(line):
                    j = skip_literal(line, i)

                    if j > 0:
                        i += j
                    else:
                        line_i = process_non_terminal(line, i, production, terminals, True)

                        if line_i[1] > 0:
                            line = line_i[0]
                            i += line_i[1]
                        else:
                            i += 1

                i = 0
                tag_opened = False

                while i < len(line):
                    j = skip_literal(line, i)

                    if j > 0:
                        i += j
                    elif line[i] == "`":
                        if tag_opened:
                            symbol = "</code>"
                            tag_opened = False
                        else:
                            symbol = "<code>"
                            tag_opened = True

                        line = line[:i] + symbol + line[i + 1:]
                        i += len(symbol)
                    else:
                        i += 1

                line = line.replace("\\\"", "\n")
                line = line.replace("\"", "**")
                line = line.replace("** **", " ")
                line = line.replace("\n", "\\\"")
                line = "&emsp;&emsp;" + line + "  "

            lines[l] = line

    return "\n".join(lines)
