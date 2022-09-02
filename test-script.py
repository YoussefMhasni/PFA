from browserstack.local import Local
  
# Creates an instance of Local
bs_local = Local()
  
# You can also use the environment variable - "BROWSERSTACK_ACCESS_KEY".
bs_local_args = { "key": "hyXbU5Nx84xKUxyXzjYu" }
  
# Starts the Local instance with the required arguments
bs_local.start(**bs_local_args)
  
# Check if BrowserStack local instance is running
print(bs_local.isRunning())
  
# Your test code goes here, from creating the driver instance till the end.
  
# Stop the Local instance after your test run is completed. 
bs_local.stop()