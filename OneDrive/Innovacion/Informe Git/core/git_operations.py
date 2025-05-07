from pathlib import Path
import subprocess

class GitOperator:
    @staticmethod
    def is_git_repo(path):
        try:
            result = subprocess.run(
                ['git', '-C', str(path), 'rev-parse', '--is-inside-work-tree'],
                capture_output=True, text=True
            )
            return result.stdout.strip() == 'true'
        except:
            return False