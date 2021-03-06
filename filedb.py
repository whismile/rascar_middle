class fileDB(object):
    """A file based database.

    A file based database, read and write arguments in the specific file.
    """
    def __init__(self, db=None):
        """Init the db_file is a file to save the data."""
        # Check if db_file is defined
        if db is not None:
            self.db = db

        else:
            self.db = "config"

    def get(self, name: str, default_value=None):
        """Get value by data's name. Default value is for the arguments do not exist"""
        conf = open(self.db, 'r')
        lines = conf.readlines()
        conf.close()
        file_len = len(lines)
        flag = False
        # Find the argument and set the value
        for i in range(file_len):
            if lines[i][0] != '#':
                if lines[i].split('=')[0].strip() == name:
                    value = lines[i].split('=')[1].replace(' ', '').strip()
                    flag = True

        if flag:
            return value

        else:
            return default_value

    def set(self, name: str, value: int):
        """Set value by data's name. Or create one if the argument does not exist"""
        # Read the file
        conf = open(self.db, 'r')
        lines = conf.readlines()
        conf.close()
        file_len = len(lines) - 1
        flag = False
        # Find the argument and set the value
        for i in range(file_len):
            if lines[i][0] != '#':
                if lines[i].split('=')[0].strip() == name:
                    lines[i] = '%s = %s\n' % (name, value)
                    flag = True
        # If argument does not exist, create one
        if not flag:
            lines.append('%s = %s\n\n' % (name, value))

        # Save the file
        conf = open(self.db, 'w')
        conf.writelines(lines)
        conf.close()
