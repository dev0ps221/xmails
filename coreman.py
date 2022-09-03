#!/usr/bin/env python3
from managers.credsmanager import CredsManager

credsman = CredsManager()
credsprofiles = []
for profile in credsman.get_creds_profiles():
    if profile not in credsprofiles:
        credsprofiles.append(profile)
print(credsprofiles)