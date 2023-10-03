'''
Yaml Parser
Version 0.0.1
Authors: Joseph Langford
Release: 10/12/2018

Purpose of this script is to be able to create, update, and read settings and user credentials in the Remote Support HelpDesk Helper tool
'''

import yaml

"""Example code, needs to be customized to meet Helper needs"""

def yaml_loader(filepath):
    '''Loads a yaml file'''
    with open(filepath, "r") as file_descriptor:
        data = yaml.load(file_descriptor)
    return data

def yaml_dump(filepath, data):
    '''Dumps data into a yaml file'''
    with open(filepath, "w") as file_descriptor:
        yaml.dump(data, file_descriptor)


print(yaml_loader('./config.example.yaml'))
