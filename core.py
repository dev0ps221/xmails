#!/usr/bin/env python3
from managers.credsmanager import CredsManager

credsman = CredsManager()
credsprofiles = credsman.get_creds_profiles()
