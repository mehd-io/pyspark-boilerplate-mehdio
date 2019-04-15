import os
import shutil
import zipfile
from setuptools import setup, find_packages
from distutils.cmd import Command
from distutils.command.install import install

from pipenv.project import Project
from pipenv.utils import convert_deps_to_pip
import subprocess
import os

PACKAGE_NAME = 'pyspark_boilerplate_mehdio'
SRC_FOLDER_NAME = 'src'
VERSION = '0.2'

ARTIFACTORY_USER = os.environ['ARTIFACTORY_USER']
ARTIFACTORY_API_KEY = os.environ['ARTIFACTORY_API_KEY']
ARTI_URI = "https://my.jfrog.artifactory/artifactory"
REPOSITORY = "my-repo-name"

pfile = Project(chdir=False).parsed_pipfile
requirements = convert_deps_to_pip(pfile['packages'], r=False)
test_requirements = convert_deps_to_pip(pfile['dev-packages'], r=False)


def zip_dir(directory, zipname, delete_flag=False):
    """
    Compress a directory (ZIP file).
    """
    if os.path.exists(directory):
        outZipFile = zipfile.ZipFile(zipname, 'w', zipfile.ZIP_DEFLATED)

        # The root directory within the ZIP file.
        rootdir = os.path.basename(directory)

        for dirpath, dirnames, filenames in os.walk(directory):
            for filename in filenames:

                # Write the file named filename to the archive,
                # giving it the archive name 'arcname'.
                filepath   = os.path.join(dirpath, filename)
                parentpath = os.path.relpath(filepath, directory)
                arcname    = os.path.join(rootdir, parentpath)

                outZipFile.write(filepath, arcname)
    
    if delete_flag is True :
        print("deleting dir")
        print(directory)
        shutil.rmtree(directory)

    outZipFile.close()

class BdistSpark(Command):

    description = "create deps and project distribution files for spark_submit"
    user_options = [
        ('requirement=', 'r', 'Install from the given requirements file. [default: requirements.txt]'),
        ('wheel-dir=', 'w', 'Build deps into dir. [default: spark_dist]')
    ]

    def initialize_options(self):
        self.requirement = 'Pipfile'
        self.wheel_dir = PACKAGE_NAME+'-'+VERSION+'_spark_dist'

    def finalize_options(self):
        assert os.path.exists(self.requirement), (
            "requirements file '{}' does not exist.".format(self.requirement))

    def run(self):
        if os.path.exists(self.wheel_dir):
            shutil.rmtree(self.wheel_dir)

        temp_dir = os.path.join(self.wheel_dir, '.temp')
        os.makedirs(temp_dir)

        # Install deps from pipfile to spark dist folder
        print("Copying python deps as zip file")
        deps_name_folder = self.wheel_dir+"/"+PACKAGE_NAME+"-"+VERSION+"-deps"
        deps_install_cmd = "pipenv run pip install -r <(pipenv lock -r) --target "+deps_name_folder
        subprocess.call(deps_install_cmd, shell=True, executable='/bin/bash')
        zip_dir(deps_name_folder, deps_name_folder+".zip", True)

        # Copying Source files
        cmd = self.reinitialize_command('bdist_wheel')
        cmd.dist_dir = temp_dir
        self.run_command('bdist_wheel')
        
        # make final rearrangements
        for dirname, _, files in os.walk(self.wheel_dir):
            for fname in files:
                if not fname.startswith(PACKAGE_NAME):
                    os.remove(os.path.join(self.wheel_dir, fname))
                else:
                    if fname.endswith('whl'):
                        os.renames(os.path.join(temp_dir, fname),
                                   os.path.join(self.wheel_dir, '{}-{}.zip'.format(PACKAGE_NAME, VERSION)))
        
        # Copy the main.py file
        main_src_file = SRC_FOLDER_NAME+"/main.py"
        main_dest_file = self.wheel_dir+"/main.py"
        print("Copying main.py entry file in spark_dist from "+main_src_file+ " to "+main_dest_file)
        shutil.copyfile(main_src_file, main_dest_file)

        # Copy the jars
        jar_src = "jars"
        print("Copying jars... from /jars folder")
        subprocess.call("cp -r "+jar_src+" "+self.wheel_dir+"/", shell=True, executable='/bin/bash')
        zip_dir(self.wheel_dir, self.wheel_dir+".zip", False)

        # Removing cache and build folder
        print("Removing cache and build folders...")
        if os.path.exists("build"):
            shutil.rmtree("build")
        if os.path.exists(PACKAGE_NAME+".egg-info"):
            shutil.rmtree(PACKAGE_NAME+".egg-info")

        print("*** Spark build is available at : "+self.wheel_dir+ " and also as single zip file ! ***")
        
class PublishArtifact(install):
    description = "Publish Artifact"
    user_options = install.user_options + [
        ("foo=", None, "jfrog user token as myname@axa.be:mytoken"),
    ]

    def run(self):
        print("Publishing Artifact ...")
        wheel_dir_zip = PACKAGE_NAME+'-'+VERSION+'_spark_dist.zip'
        pre_path_build = PACKAGE_NAME+"/"+VERSION
        publish_cmd = ''' 
        curl -u {artifactory_user}:{artifactory_api_key} \
        -i -X PUT \
        -T {wheel_dir_zip} \
        {arti_uri}/{repository}/{pre_path_build}/{wheel_dir_zip}'''.format(artifactory_user=ARTIFACTORY_USER, artifactory_api_key=ARTIFACTORY_API_KEY, arti_uri=ARTI_URI, repository=REPOSITORY, pre_path_build=pre_path_build, wheel_dir_zip=wheel_dir_zip)
        subprocess.call(publish_cmd, shell=True, executable='/bin/bash')
        print("Publishing Artifact successful on {arti_uri}/{wheel_dir_zip}!".format(wheel_dir_zip=wheel_dir_zip, arti_uri=ARTI_URI))
        
setup(
    name=PACKAGE_NAME,

    version=VERSION,

    description='an example project that shows how to build spark_submit deps',

    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.7',
    ],

    author='Mehdi OUAZZA',

    author_email='mehdi@mehd.io',

    packages=find_packages(include=[SRC_FOLDER_NAME, SRC_FOLDER_NAME+'.*'],
                           exclude=['*.test.*', '*.test']),

    install_requires=requirements,

    tests_require=test_requirements,

    package_data={
        PACKAGE_NAME: ['../Pipfile']
    },

    cmdclass={
        "bdist_spark": BdistSpark,
        "publish_artifact": PublishArtifact
    }
)
