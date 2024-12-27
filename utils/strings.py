import yaml

class Strings:
    def __init__(self, locale, project=None):
        self.locale = locale
        self.project = project
        with open('assets/strings.yaml', 'r') as file:
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