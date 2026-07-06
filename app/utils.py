import os
from datetime import datetime
from pathlib import Path
from typing import Any

import orjson


def write_report(report_type: str, content: Any):
    script_path = Path(__file__).absolute().parent
    json_path = script_path / (
                f'reports/{report_type}/report-' + datetime.now().strftime('%Y-%m-%d-%H-%M-%S') + '.ndjson')
    chunk_size = 10000
    os.makedirs(json_path.parent, exist_ok=True)
    with open(json_path, 'wb', buffering=8 * 1028 * 1028) as f:
        batch = []

        for row in content if not isinstance(content, dict) else content.items():
            batch.append(orjson.dumps(row))

            if len(batch) >= chunk_size:
                f.write(b'\n'.join(batch) + b'\n')
                batch.clear()

        if batch:
            f.write(b'\n'.join(batch) + b'\n')
            batch.clear()


def jinja_safe_print(*x, sep: str = " "):
    print("\033[1;31;40m DEBUG:", *x, "\033[0m", sep=sep)
    return ""
