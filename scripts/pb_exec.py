from ansible import context
from ansible.cli import CLI
from ansible.module_utils.common.collections import ImmutableDict
from ansible.executor.playbook_executor import PlaybookExecutor
from ansible.parsing.dataloader import DataLoader
from ansible.inventory.manager import InventoryManager
from ansible.vars.manager import VariableManager
import yaml
import pb_ui
import os

def pb_exec():
    with open('/home/dmitryd/ansible_ui/scripts/config/conf.yml') as f:
        conf = yaml.safe_load(f)

    h_dir = conf['variables']['dirs']['inventory_dir']
    pb_dir = conf['variables']['dirs']['pb_dir']
    retry_dir = conf['variables']['dirs']['pb_retry_dir']

    user_name = conf['main']['ssh_config']['user']
    user_key = conf['main']['ssh_config']['key']
    if user_key == 'None':
        user_key = None

    pb_files = pb_ui.pb_list(pb_dir)
    host_file = pb_ui.hosts_list(h_dir)

    loader = DataLoader()

    context.CLIARGS = ImmutableDict(tags={}, listtags=False, listtasks=False, listhosts=False, syntax=False, connection='ssh',
                        module_path=None, forks=100, remote_user=user_name, private_key_file=user_key,
                        ssh_common_args=None, ssh_extra_args=None, sftp_extra_args=None, scp_extra_args=None, become=True,
                        become_method='sudo', become_user='root', verbosity=True, check=False, start_at_task=None, retry_files_enabled=True, retry_files_save_path=retry_dir)

    inventory = InventoryManager(loader=loader, sources=(host_file,))

    variable_manager = VariableManager(loader=loader, inventory=inventory, version_info=CLI.version_info(gitinfo=False))

    pbex = PlaybookExecutor(playbooks=pb_files, inventory=inventory, variable_manager=variable_manager, loader=loader, passwords={})
    results = pbex.run()

    print()
    #print("unreachable hosts:")
    #print(pbex._unreachable_hosts)
    print("are you want to save new Host file?(Yes,No)")
    y = str(input())
    if y in ['Yes', 'YES', 'yes', 'y', 'Y']:
        pb_ui.new_inv(host_file,h_dir)
    else:
        os.remove(host_file)
