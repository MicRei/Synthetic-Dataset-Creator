import subprocess as sp

#   TODO: Extract case_id's from database as binary string
# In[91]: sp_out = sp.run(mutaccDB_args, stdout=sp.PIPE)
#   TODO: Decode binary string to UTF-8 string
# In[92]: sp_out_decoded = sp_out.stdout.decode('UTF-8')
#   TODO: find all case_id's
# In[93]: cases = re.findall("'case_id.*[1-9A-Za-z]'", sp_out_decoded)
#   TODO: split out the ID of the case OR used each case string in the list
#    to create a new dataset for the synthetic dataset database
# In[116]: case_id = cases[9].split("'")[2] OR sp.run(mutacc_import_args with case_id file)

