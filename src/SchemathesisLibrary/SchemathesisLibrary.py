import subprocess
import yaml

class SchemathesisLibrary:
    ROBOT_LIBRARY_SCOPE = 'SUITE'

    def __init__(self, schema_path):
        self.schema_path = schema_path
        self.cassette_path = ""
 
    def run_fuzzing(self, **kwargs):
        output = self.run_command("run", **kwargs)
        return output.decode()
    
    def replay_testcase(self, **kwargs):
        output = self.run_command("replay", **kwargs)
        return output.decode()
    
    def run_command(self, command, **kwargs):
        """
        Run a command-line command with optional keyword arguments.

        Args:
        - command (str): The command to run.
        - kwargs: Keyword arguments to pass to the command.

        Returns:
        - str: Output of the command.
        """
        if command == "run":
            full_command = ["st", command, self.schema_path]
        else:
            full_command = ["st", command, self.cassette_path]

        for key, value in kwargs.items():
            if key == "cassette-path":
                self.cassette_path = value
            full_command.extend([f"--{key}", str(value)])
        print(full_command)

        # return str(full_command).encode()

        try:
            result = subprocess.run(full_command, stdout = subprocess.PIPE, stderr = subprocess.STDOUT,)
            return result.stdout
        except subprocess.CalledProcessError as e:
            return None
        
    def get_failed_interactions(self):
        # Parse the YAML content
        with open(self.cassette_path, 'r', errors='ignore') as file:
            yaml_content = file.read()
                
            data = yaml.safe_load(yaml_content)

            # Initialize a dictionary to store failed interactions' IDs by endpoint
            failed_interactions = {}

            # Iterate over each interaction
            for interaction in data.get('http_interactions', []):
                status = interaction.get('status')
                if status == 'FAILURE':
                    # Extract endpoint and interaction ID
                    endpoint = interaction.get('request', {}).get('uri')
                    interaction_id = interaction.get('id')

                    # Add the interaction ID to the dictionary
                    if endpoint:
                        if endpoint not in failed_interactions:
                            failed_interactions[endpoint] = []
                        failed_interactions[endpoint].append(interaction_id)

            return failed_interactions