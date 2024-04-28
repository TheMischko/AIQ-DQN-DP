import os
import subprocess

from genetics.context.TestSettings import TestSettings


def eval_function(genome, agent_name, test_settings: TestSettings):
    """
    Evaluation function for AIQ test.

    It runs AIQ.py file with set arguments.

    :param genome: Attributes for the agent in array.
    :type genome: list
    :param agent_name: Name of the AIQ agent.
    :type agent_name: string
    :param test_settings: Settings for the AIQ test.
    :type test_settings: TestSettings
    """
    script_string = "python " + build_script_string(genome, agent_name, test_settings)
    script_path = os.getcwd().split("genetics")[0]
    args = script_string.split(" ")
    process = subprocess.Popen(args, cwd=script_path, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()

    output = stdout.decode("utf-8")
    err = stderr.decode("utf-8")
    if err:
        print("Evaluation errors:" + err)
    parsed_value = parse_output(output)
    return parsed_value


def parse_output(output_str):
    """
    Parses the standard string output from AIQ test that was running in the virtual console and returns a value.

    Result is score minus positive part of variation.
    Note: If result values contains "nan" values the result will -9e10.
    """
    lines = output_str.split("\n")
    result_line = lines[len(lines) - 2]
    split_result_line = result_line.split(" ")
    values = list()
    for parts in split_result_line:
        # Filter out not necessary parts.
        if parts is None or parts == '' or parts == "\n" or parts == "\r":
            continue
        values.append(parts)

    # Handle NaN
    if len(values) != 4:
        return -9e10
    if values[1] == "nan" or values[3] == "nan":
        return -9e10

    # Calculate result
    # AIQ value - variation
    result = float(values[1])

    if result == float("nan"):
        result = -9e10
    return result


def build_script_string(genome, agent, test_settings: TestSettings):
    """
    Builds runnable script for python command.

    Script contains absolute path that is deviated from location of this file.
    """
    iterations = test_settings.iterations
    samples = test_settings.samples
    threads = test_settings.threads
    log = test_settings.log
    log_el = test_settings.log_el

    path_to_repo = os.path.normpath(os.getcwd().split("genetics")[0])
    a = os.path.normpath("./AIQ.py")
    path = os.path.join(path_to_repo, os.path.normpath("./AIQ.py"))

    script_arg_string = f"{path} -r BF -a {agent}"

    if genome is not None and len(genome) > 0:
        for gen in genome:
            script_arg_string += f",{gen}"

    script_arg_string += f" -l {iterations} -s {samples} -t {threads}"

    if log is True:
        script_arg_string += " --log"
    if log_el is True:
        script_arg_string += " --verbose_log_el"

    return script_arg_string
