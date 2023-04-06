#!/usr/bin/python3
"""
Fabric script to distribute an archive to web servers
"""

import os
from fabric.api import env, put, run
from datetime import datetime

env.hosts = ['54.162.46.10', '54.146.92.4']


def do_deploy(archive_path):
    """
    Distributes an archive to web servers
    """
    if not os.path.exists(archive_path):
        return False

    try:
        # Upload the archive to the /tmp/ directory of the web server
        put(archive_path, "/tmp/")

        # Uncompress the archive to the folder
        # /data/web_static/releases/<archive filename without extension>
        archive_filename = os.path.basename(archive_path)
        archive_folder = archive_filename.split(".")[0]
        release_folder = "/data/web_static/releases/" + archive_folder
        run("sudo mkdir -p {}".format(release_folder))
        run("sudo tar -xzf /tmp/{} -C {}"
            .format(archive_filename, release_folder))

        # Delete the archive from the web server
        run("sudo rm /tmp/{}".format(archive_filename))

        # Move the files out of the release folder
        run("sudo mv {}/web_static/* {}".format(release_folder, release_folder))

        # Remove the empty web_static directory
        run("sudo rm -rf {}/web_static".format(release_folder))

        # Delete the symbolic link /data/web_static/current from the web server
        run("sudo rm -rf /data/web_static/current")

        # Create a new the symbolic link /data/web_static/current on the web server,
        # linked to the new version of your code
        run("sudo ln -s {} /data/web_static/current"
            .format(release_folder))

        print("New version deployed!")
        return True

    except Exception as e:
        print(e)
        return False

