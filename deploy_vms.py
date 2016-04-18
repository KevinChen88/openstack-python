
import novaclient
import glanceclient
import neutronclient
import keystoneclient

#assuming this is run on controller node
#just login with admin/admin for testing purposes
host_ip='127.0.0.1'
keystone_port='5000'
target_url=host_ip+':'+keystone_port
login_name='admin'
login_pass='admin'
tenant='admin'

def main():
    
    #get parameters from ini files
    from script import config_files
    vm_list=config_files('openstack_ini/vm_list.ini')
    aggr_list=config_files('openstack_ini/aggregates.ini')
    flavor_list=config_files('openstack_ini/flavors.ini')
    image_list=config_files('openstack_ini/images.ini')
    net_list=config_files('openstack_ini/networks.ini')

    #establish credentials using keystone client session 
    sess=keystoneclient.client.Client(username=login_name, password=login_pass, tenant_name=tenant, auth_url=target_url)
    
    #glance session object
    glance=glanceclient.client.Client(version=2, session=sess)
    create_glance_image(glance, image_list)
    
    #nova session object
    nova=novaclient.client.Client(version=2, session=sess)
    create_vm_flavor(nova, flavor_list)
    create_aggregates(nova, aggr_list)
    
    #neutron session object
    neutron=neutronclient.client.Client(version=2, session=sess)
    create_network(neutron, net_list)
    
    #spawn VMs
    boot_vm(nova, vm_list)
        

def create_vm_flavor(nova, flavor_list):
#Function - define flavor for a vm
    for flavor_name in flavor_list:
        ram=vm_config.get(flavor_name,'mb_ram')
        vcpus=vm_config.get(flavor_name,'num_vcpus')
        disk=vm_config.get(flavor_name,'gb_space')
        nova.flavors.create(flavor_name, ram, vcpus, disk, flavorid='auto', ephemeral=0, swap=0, rxtx_factor=1.0, is_public='true')

def create_aggregates(nova, aggr_list):
#Function - create aggregates/zones and add hosts to it
    for aggr_name in aggr_list:
        zone_name=aggr_list.get(aggr_name,'zone')
        zone_hosts=aggr_list.get(aggr_name,'host_list')
        nova.aggregate.create(aggr_name,zone_name)
        for host_name in zone_hosts:
            nova.aggregate.add_host(aggr_name, host_name)
            
def boot_vm(nova, vm_list):
#Function - boot new VMs
    for vm_name in vm_list:
        zone_name=vm_list.get(vm_name,'zone')
        image_name=vm_list.get(vm_name,'image')
        flavor_name=vm_list.get(vm_name,'flavor')
        nics_add=vm_list.get(vm_name,'nics')
        nova.servers.create(name=vm_name, image=image_name , flavor=flavor_name, nics=nics_add, zone=zone_name)     

def create_network(neutron, net_list):
#Function - spawn virtual network
    for net_name in net_list
        subnet_name=net_list.get(net_name,'subnet')
        ip_range=net_list.get(net_name,'ip_addr')
        neutron.create_network({'network':net_name, subnet=subnet_name, ip=ip_range ,})
        
def create_glance_image(glance, image_list):
#Function - create glance image from qcow2 file
    for image_name in image_list
        file_name=image_list.get(image_name,'file_loc')
        disk_format=image_list.get(image_name,'disk_format')
        public=image_list.get(image_name,'is_public')
        container=image_list.get(image_name,'container')
        glance.images.create(name=image_name , file=file_name, disk-format=disk_format, container-format=container, is_public=public)
        
if __name__ == "__main__":
        main()
        

