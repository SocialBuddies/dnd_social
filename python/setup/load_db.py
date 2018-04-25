from django.core.management import call_command

# load core
exec(open("setup/core.py").read())
# call_command('update_core_from_api')


# load npc_data
print("adding npcs")
exec(open("setup/npcs.py").read())
