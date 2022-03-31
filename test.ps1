# SPDX-FileCopyrightText: 2013-2022 Jonathan Hartley & Arnon Yaari
#
# SPDX-License-Identifier: BSD-3-Clause

$ve="$HOME\.virtualenvs\colorama"
$bin="$ve\Scripts"

& $bin\python.exe -m unittest discover -p *_test.py

