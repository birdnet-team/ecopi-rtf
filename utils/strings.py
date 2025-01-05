import os
import yaml

class Strings:
    def __init__(self, locale, project=None):
        self.locale = locale
        self.project = project
        
        # Get the absolute path to the YAML file
        base_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(base_dir, 'assets', 'strings.yaml')
        
        if not os.path.exists(file_path):
            base_dir = os.path.dirname(base_dir)
            file_path = os.path.join(base_dir, 'assets', 'strings.yaml')
        
        with open(file_path, 'r') as file:
            self.strings = yaml.safe_load(file)

    def get(self, key):
        if self.project:
            # Try to get the string from the project-specific section
            project_string = self.strings.get('projects', {}).get(self.project, {}).get(key, {}).get(self.locale)
            if project_string:
                return project_string
            # Fall back to the general section if not found in the project-specific section
            project_string = self.strings.get('projects', {}).get(self.project, {}).get(key, {}).get('en')
            if project_string:
                return project_string
        # Get the string from the general section
        return self.strings.get(key, {}).get(self.locale, self.strings.get(key, {}).get('en', ''))

# Usage example:
# strings = Strings(locale, project='swamp')
# project_main_title = strings.get('project_main_title')
# welcome_message = strings.get('welcome_message')