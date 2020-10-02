import argparse
import json
from azure.common.credentials import ServicePrincipalCredentials
from azure.mgmt.compute import ComputeManagementClient
from azure.mgmt.subscription import SubscriptionClient


def extra_api(client_id,client_secret, tenant_id, env, verbose=False):
    # utc_timestamp = datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc).isoformat()

    # check if it's prod or dev account
    region_vm_dict={}
    credentials = ServicePrincipalCredentials(
        client_id=client_id,
        secret=client_secret,
        tenant=tenant_id
    )

    sub_groups = []
    count = 0
    # grab all all subscriptions that the credential are associated to
    sub_client = SubscriptionClient(credentials)
    sub_interator = sub_client.subscriptions.list()
    for sub in sub_interator:
        sub_groups.append(sub.subscription_id)

    # grab all vm in all subs and sort them by region
    for sub_id in sub_groups:
        compute_client = ComputeManagementClient(credentials, sub_id)
        vms_by_subs = compute_client.virtual_machines.list_all()
        for vm in vms_by_subs:
            count = count + 1
            if vm.location not in region_vm_dict:
                region_vm_dict[vm.location]=[vm.name]
            else:
                region_vm_dict[vm.location].append(vm.name)

        # grab all vm in all the Azure VM scale sets
        vms_scale_sets = compute_client.virtual_machine_scale_sets.list_all()
        for vm_s_set in vms_scale_sets:
            id_list = vm_s_set.id.split('/')
            resource_group = id_list[4]
            scale_set_name = vm_s_set.name
            vmss = compute_client.virtual_machine_scale_set_vms.list(resource_group,scale_set_name)
            for vm in vmss:
                count = count + 1
                if vm.location not in region_vm_dict:
                    region_vm_dict[vm.location] = [vm.name]
                else:
                    region_vm_dict[vm.location].append(vm.name)

    #print vms
    if verbose:
        for region in region_vm_dict:
            for vm in region_vm_dict[region]:
                print('{0}: {1}'.format(region,vm))
    print('Total number of VM in {0} Azure environment: {1}'.format(env, count))

def parse_cred_file(cred_file, env='dev'):
    with open(cred_file) as f:
        data = json.load(f)

    return(data[env]["AZURE_CLIENT_ID"],data[env]["AZURE_CLIENT_SECRET"],data[env]["AZURE_TENANT_ID"] )


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Get list of all VMs in Azure regions')
    parser.add_argument('--client-id', help='azure client Key',dest='client_id')
    parser.add_argument('--client-secret', help='azure client secret', dest='client_secret')
    parser.add_argument('--tenant-id', help='azure tenant id',dest='tenant_id')
    parser.add_argument('--env', help='azure environment (prod or dev)', dest='env')
    parser.add_argument('--cred-file', help='credential file', dest='cred_file')
    parser.add_argument('--verbose', help='verbose output', action='store_true')
    args = parser.parse_args()

    client_key = None
    client_secret = None
    tenant_id = None
    cred_file = None
    verbose = False
    total_number_of_instances = 0

    if args.client_id is not None:
        client_id = args.client_id
    if args.client_secret is not None:
        client_secret = args.client_secret
    if args.tenant_id is not None:
        tenant_id = args.tenant_id
    if args.cred_file is not None:
        cred_file = args.cred_file
    if args.env is not None:
        env = args.env
    else:
        env = 'dev'
    if args.verbose:
        verbose = True

    # extract the cred from the credential file from sercret server
    client_id, client_secret, tenant_id = parse_cred_file(cred_file, env)
    # extract vm from api
    extra_api(client_id,client_secret,tenant_id,env,verbose)
