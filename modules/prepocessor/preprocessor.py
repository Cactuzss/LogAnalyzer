import os
import regex as re


STAGE_START_RE = re.compile(
    r'Executing\(%(prep|build|install|clean|check)\): .*')

FAILURE_MARKER_RE = re.compile(r'error: Bad exit status from .* \(%')

# Case-insensitive keywords, plus gcc/g++ error format
ERROR_LINE_RE = re.compile(
    r'(?i)(error|fail|not found|missing:|cmake error|gmake: \*\*\*|:\d+:\d+:)')


class Preprocessor:
    @staticmethod
    def extract_failure_info(log_lines: list[str], build_target: str | None, build_stage: str | None):
        error_snippet_lines = []
        full_log_text = "\n".join(log_lines)

        recent_lines_count = 100
        for line in reversed(log_lines[-recent_lines_count:]):
            if ERROR_LINE_RE.search(line):
                error_snippet_lines.insert(0, line)

        if not error_snippet_lines:
            marker_index = -1
            for i in range(len(log_lines) - 1, -1, -1):
                if FAILURE_MARKER_RE.search(log_lines[i]):
                    marker_index = i
                    break
            if marker_index != -1:
                snippet_start = max(0, marker_index - 50)
                error_snippet_lines = log_lines[snippet_start:marker_index]
            else:
                error_snippet_lines = log_lines[-50:]

        return {
            "target_platform": build_target,
            "build_stage": build_stage,
            "error_snippet": "\n".join(error_snippet_lines).strip(),
            "full_log": full_log_text.strip()
        }

    @staticmethod
    def process_log(filepath: str, data: str):
        failures = []
        current_build_lines = []
        current_target = None
        current_stage = None
        in_build_block = False
        failure_detected_in_block = False

        lines = data.splitlines()
        for i, line in enumerate(lines):
            line = line.rstrip()

            if "Building target platforms:" in line and lines[i+1].startswith("Building for target"):
                if in_build_block:
                    if failure_detected_in_block:
                        failure_info = Preprocessor.extract_failure_info(
                            current_build_lines, current_target, current_stage)
                        failure_info["log_file"] = os.path.basename(filepath)
                        failures.append(failure_info)

                in_build_block = True
                failure_detected_in_block = False
                current_build_lines = [line]
                current_target = lines[i +
                                       1].split("Building for target ")[1].strip()

            elif in_build_block:
                stage_match = STAGE_START_RE.search(line)
                if stage_match:
                    current_stage = "%" + stage_match.group(1)
                    current_build_lines.append(line)
                elif FAILURE_MARKER_RE.search(line) or "hsh-rebuild:" in line or "RPM build errors:" in line:
                    failure_detected_in_block = True
                    current_build_lines.append(line)
                else:
                    current_build_lines.append(line)

        if in_build_block and failure_detected_in_block:
            failure_info = Preprocessor.extract_failure_info(
                current_build_lines, current_target, current_stage)
            failure_info["log_file"] = os.path.basename(filepath)
            failures.append(failure_info)

        return failures
