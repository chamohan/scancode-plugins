# scancode-plugins
Plugins for Running scancode on RoCm

# To Install the Plugins
Go to the Plugin Directory
'''cd scancode-toolkit/plugins/scancode-licence-modifications'''

# Run following command
 '''pip install -e .'''




# Example : 

'''scancode -clpeui  --package --processes 64 --license-text --verbose --full-root --json-pp roctracer.json ../roctracer --license-policy ../amd_licence_policy.yml --classify --summary --summary-with-details  --license-diag --no-licenses --licence-modifications'''
