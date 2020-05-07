import logging
from pathlib import Path
from subprocess import CompletedProcess


def report_to_shell(file: Path, status: CompletedProcess):
    # log_level_by_status = logging.ERROR if status.returncode else logging.INFO
    print('-' * 80)
    file_str = 'File: %s' % file.name
    # logging.log(log_level_by_status, file_str)
    print(file_str)
    result_str = 'Result: %s' % _to_result(status.returncode)
    # logging.log(log_level_by_status, result_str)
    print(result_str)
    logging.debug('Command: %s', status.args)
    if logging.getLogger().isEnabledFor(logging.INFO):
        print('stdout:')
        print(status.stdout)
    if status.returncode:
        print('stderr:')
        logging.error('the following error occured during processing: %s', status.stderr)

def _to_result(returncode) -> str:
    return 'error' if returncode else 'success'
