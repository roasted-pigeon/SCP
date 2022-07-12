# This is a file of basic settings for all systems. After deploying and starting the operation of the systems,
# change the parameters in this file only if you know exactly what you are doing


# This parameter defines the path to the main database of the Foundation
# Default: "sqlite:///..\\SCPDatabase.db"
SCPDatabase: str = "sqlite:///SCPDatabase.db"

# This parameter defines the path to the Foundation's log database
# Default: "sqlite:///..\\SCPLogs.db"
SCPLogs: str = "sqlite:///SCPLogs.db"

# This parameter determines whether a separate object (dbController, logCollector, etc.) will be created if it is
# necessary to transfer it as a handler to the class constructor when creating the object. In high-load systems,
# this will allow the system to distribute the load, but may significantly increase system requirements
# Default: True
individualObjects: bool = True

# This parameter defines the salt, used in password hashing
# IMPORTANT: DO NOT CHANGE THIS PARAMETER AFTER DATABASE IS FILLED WITH USER'S LOGIN DATA
passwordSalt: str = "_sqlscp-rth5614"

# This parameter determines whether the systems are running in debug mode. When debugging mode is enabled,
# the console may display error messages containing sensitive data (for example, file paths and device
# characteristics)
# It is highly NOT recommended to set this parameter to True if the systems are deployed in production
# Default: False
debug: bool = True

# This parameter determines which error will be displayed when exceptions occur when setting the value False to the
# debug parameter
# Default: "Try again or contact technical support!"
veiledError: str = "Повторите попытку или обратитесь в техническую поддержку!"

# This parameter determines the encoding used in the systems.
# Attention! Changing the encoding during the operation of the system will affect, among other things,
# the encoding of password hashes, which may break the authentication system down
# Default: 'utf-8'
encoding: str = 'utf-8'
