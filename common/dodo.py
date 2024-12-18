# https://pydoit.org/ tasks file
# This is symlinked in every problem directory to provide a common set of tasks
# please update the file at common/dodo.py

import glob
import os
import doit
import doit.action
import doit.tools
import tempfile

INPUT_FILE = doit.get_var("input", "input.txt")
LANG_EXTS = ["py", "cc", "go"]
DOIT_CONFIG = {"default_tasks": ["exe"]}


def lang_files(lang):
    for src in glob.glob(f"*.{lang}"):
        if src == "dodo.py":
            continue
        name = src.removesuffix(f".{lang}")
        built = f"{lang}_{name}"
        yield src, built, name


def task_build_py():
    for src, built, name in lang_files("py"):
        yield {
            "name": name,
            "file_dep": [src],
            "actions": [
                "(echo '#!/usr/bin/env python' && cat %(dependencies)s) > %(targets)s && chmod +x %(targets)s"
            ],
            "targets": [built],
            "clean": True,
        }


def task_py():
    for _, built, name in lang_files("py"):
        yield {
            "name": name,
            "file_dep": [built],
            "actions": [f"python %(dependencies)s {INPUT_FILE} < {INPUT_FILE}"],
            "verbosity": 2,
            "uptodate": [False],
        }


def task_build_cc():
    for src, built, name in lang_files("cc"):
        yield {
            "name": name,
            "file_dep": [src],
            "actions": ["g++ -O3 -o %(targets)s %(dependencies)s"],
            "targets": [built],
            "clean": True,
        }


def task_cc():
    for _, built, name in lang_files(lang="cc"):
        yield {
            "name": name,
            "actions": [f"./%(dependencies)s {INPUT_FILE} < {INPUT_FILE}"],
            "file_dep": [built],
            "verbosity": 2,
            "uptodate": [False],
        }


def task_build_go():
    def build_isolated(src, target):
        abs_src = os.path.abspath(src)
        abs_target = os.path.abspath(target)
        base_target = os.path.basename(target)
        with tempfile.TemporaryDirectory(prefix=base_target) as tmp_dir:
            tmp_src = os.path.join(tmp_dir, "src.go")
            os.symlink(abs_src, tmp_src)
            os.system(
                command=f"cd {tmp_dir}"
                f" && go build -tags {base_target} -o {abs_target} src.go"
            )

    for src, built, name in lang_files("go"):
        yield {
            "name": name,
            "file_dep": [src],
            "actions": [(build_isolated, [src, built])],
            "targets": [built],
            "clean": True,
        }


def task_go():
    for _, built, name in lang_files("go"):
        yield {
            "name": name,
            "actions": [f"./%(dependencies)s {INPUT_FILE} < {INPUT_FILE}"],
            "file_dep": [built],
            "verbosity": 2,
            "uptodate": [False],
        }


def task_exe():
    return {
        "actions": None,
        "task_dep": LANG_EXTS,
    }


def task_build():
    return {
        "actions": None,
        "task_dep": [f"build_{lang}" for lang in LANG_EXTS],
    }


def hyperfine_action(cmds, report=False):
    return doit.tools.Interactive(
        f"cd {os.getcwd()} && hyperfine --shell=none"
        + (" --export-markdown=bench.md" if report else "")
        + f" --input {INPUT_FILE} "
        + " ".join(f'"{cmd} {INPUT_FILE}"' for cmd in cmds)
    )


def task_bench():
    all_file_dep = []
    all_bench_cmds = []

    for lang in LANG_EXTS:
        bench_cmds = []
        file_dep = []
        for _, built, name in lang_files(lang):
            cmd = f"./{built}"
            yield {
                "basename": "sol_bench",
                "name": f"{lang}:{name}",
                "file_dep": [built],
                "actions": [hyperfine_action([cmd])],
                "verbosity": 2,
                "uptodate": [False],
            }
            bench_cmds.append(cmd)
            file_dep.append(built)
        yield {
            "basename": "lang_bench",
            "name": lang,
            "actions": [hyperfine_action(bench_cmds)],
            "file_dep": file_dep,
            "verbosity": 2,
            "uptodate": [False],
        }
        all_bench_cmds.extend(bench_cmds)
        all_file_dep.extend(file_dep)

    yield {
        "name": "all",
        "actions": [hyperfine_action(all_bench_cmds, report=True)],
        "file_dep": all_file_dep,
        "verbosity": 2,
        "uptodate": [False],
    }
