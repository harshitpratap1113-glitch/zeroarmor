"""
Layer 11: Zip Slip & Tar Bomb Jail
Hooks zipfile and tarfile extract operations to stop directory traversal via malicious archives.
"""

import os
from pathlib import Path
import tarfile
import zipfile

def is_path_safe(target_dir: str, member_path: str) -> bool:
    resolved_target = Path(target_dir).resolve()
    resolved_dest = (resolved_target / member_path).resolve()
    return resolved_dest.is_relative_to(resolved_target)

def arm_zip_slip(core):
    # 1. Hook zipfile
    orig_zip_extract = zipfile.ZipFile.extract
    orig_zip_extractall = zipfile.ZipFile.extractall

    def armored_zip_extract(self, member, path=None, pwd=None):
        target_dir = path or os.getcwd()
        member_name = member.filename if hasattr(member, "filename") else str(member)
        if not is_path_safe(target_dir, member_name):
            core.record_threat(
                rule_name="Zip Slip Archive Traversal",
                reason=f"Archive contains malicious relative path escape: {member_name}",
                payload=member_name,
                block=True
            )
        return orig_zip_extract(self, member, path=path, pwd=pwd)

    def armored_zip_extractall(self, path=None, members=None, pwd=None):
        target_dir = path or os.getcwd()
        items = members or self.infolist()
        for item in items:
            item_name = item.filename if hasattr(item, "filename") else str(item)
            if not is_path_safe(target_dir, item_name):
                core.record_threat(
                    rule_name="Zip Slip Archive Traversal",
                    reason=f"Archive contains malicious relative path escape: {item_name}",
                    payload=item_name,
                    block=True
                )
        return orig_zip_extractall(self, path=path, members=members, pwd=pwd)

    zipfile.ZipFile.extract = armored_zip_extract
    zipfile.ZipFile.extractall = armored_zip_extractall

    # 2. Hook tarfile
    orig_tar_extract = tarfile.TarFile.extract
    orig_tar_extractall = tarfile.TarFile.extractall

    def armored_tar_extract(self, member, path="", *args, **kwargs):
        target_dir = path or os.getcwd()
        member_name = member.name if hasattr(member, "name") else str(member)
        if not is_path_safe(target_dir, member_name):
            core.record_threat(
                rule_name="Tar Slip Archive Traversal",
                reason=f"Tar archive contains malicious path escape: {member_name}",
                payload=member_name,
                block=True
            )
        return orig_tar_extract(self, member, path=path, *args, **kwargs)

    tarfile.TarFile.extract = armored_tar_extract
