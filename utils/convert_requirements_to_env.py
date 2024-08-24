import os
import subprocess
import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def is_conda_package(package_name):
    """
    Check if a given package is available in the Conda repository.

    Parameters:
    package_name (str): The name of the package to check. If the package has a version specified, only the package name will be used for the check.

    Returns:
    bool: True if the package is available in the Conda repository, False otherwise.
    """
    try:
        package_name_to_search = package_name.split('=')[0]
        result = subprocess.run(['conda', 'search', package_name_to_search], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode == 0:
            logging.info(f'Package {package_name} is available as a Conda package.')
        else:
            logging.info(f'Package {package_name} is not available as a Conda package.')
        return result.returncode == 0
    except Exception as e:
        logging.error(f'Error checking Conda package availability: {str(e)}')
        return False


def convert_requirements_to_yml(requirements_file, output_file, environment_name='env_genai_agent'):
    requirements_path = os.path.join(os.path.dirname(__file__), requirements_file)
    output_path = os.path.join(os.path.dirname(__file__), output_file)

    with open(requirements_path, 'r') as req_file:
        lines = req_file.readlines()

    with open(output_path, 'w') as yml_file:
        yml_file.write(f'name: {environment_name}\n')
        yml_file.write('channels:\n')
        yml_file.write('  - conda-forge\n')
        yml_file.write('  - defaults\n')
        yml_file.write('dependencies:\n')
        yml_file.write('  - python=3.10.8\n')  

        pip_packages = []

        for line in lines:
            package = line.strip()
            if package:
                if is_conda_package(package):
                    yml_file.write(f'  - {package.replace("==", "=")}\n')
                else:
                    pip_packages.append(package)

        if pip_packages:
            yml_file.write('  - pip:\n')
            for package in pip_packages:
                yml_file.write(f'    - {package}\n')

    logging.info(f'Successfully converted requirements to {output_file}')



if __name__ == "__main__":
    convert_requirements_to_yml('../requirements.txt', '../environment.yml')
