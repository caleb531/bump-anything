from dataclasses import dataclass


# The result of a version bump operation on a particular file; each result
# represents an individual file along with the details of its version change
@dataclass
class FileResult(object):
    file_path: str
    current_version: str
    new_version: str
