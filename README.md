# Compiler for Nintendo EventFlow flowcharts

Tool to compile a readable, code-like format into eventflow flowcharts (bfevfl) for *Animal Crossing: New Horizons*.

This project is the counterpart of [acnh-eventflow-decompiler](https://github.com/asteriation/acnh-eventflow-decompiler).

This project is still a work in progress, and currently compiles all 562/562 of the decompiled flows
from v1.11.0, with 561/562 recompiled flows being no larger than the original bfevfl file (558/562
smaller, 3/562 same size) when using `--optimize`.

## Usage

The decompiler may be run through `main.py` using Python 3.7.

You will need to supply a `functions.csv` file containing typing information for EventFlow functions; this can be done for ACNH by downloading the 'Actions/Queries' sheet from [this
spreadsheet](https://docs.google.com/spreadsheets/d/1AYM-UeRkbJuGy_nKv7AMngevwBtMdZPtfoHEQev8BhM/edit) as a CSV file.

You will also need to supply the evfl files to be compiled.

```bash
mkdir -p out/

python3 main.py --functions functions.csv \
                --version 1.0.0 \
                -d output_directory \
                file1.evfl file2.evfl ...
```

This outputs the compiled bfevfls into `output_directory`.

If compiling only a single file, `-o` can be used instead of `-d` to specify the output file name.

There are some flags starting with `--f` to optimize for output file size (at the expense of a
readable decompile), and `--optimize` enables them all.

## License

This software is licensed under the terms of the MIT License.
