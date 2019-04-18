from model.host_model import host

import model.db_config
from psycopg2 import connect

class DB_Model:


    def __init__(self):
        #connect to real db here
        try:
            conn_string = "dbname='"+db_config.DB_NAME+"' user='"+db_config.DB_USER+"' password='"+db_config.DB_PASSWORD+"'"
            conn = connect(conn_string)
            self.cursor = conn.cursor()
            self.cursor.execute("SELECT table_name FROM information_schema.tables")
        except :
            print("DB connect failed")
            self.connected = False


        self.hosts = []
        self.view_toggle = 'ports'

    def get_hosts(self):
        if self.view_toggle == "ports":
            self.hosts.sort(key=lambda x: x.num_ports, reverse=True)
        else:
            self.hosts.sort(key=lambda x: x.num_ports, reverse=True)
        return self.hosts

    def get_view_toggle(self):
        return self.view_toggle

    #update from the DB
    def update_hosts(self):
        if not self.connected:
            print("DB not connected, use test_update_hosts")
            return False
        q_string = "SELECT id, address, os_family, service_count, purpose, comments FROM public.hosts"
        self.cursor.execute(q_string)
        rows = self.cursor.fetchall()
        for row in rows:
            host_ports = self.get_host_port_info(row[0]) #id
            self.hosts.append(host(ident=row[0],ip=row[1], OS=row[2], ports=host_ports, purpose=row[4], comments=row[5]))
        self.hosts.sort(key=lambda x: x.num_ports, reverse=True)
        return True

    def test_update_hosts(self, num=1):
        for i in range(0,num):
            self.hosts.append(host())

    def get_host_port_info(self, host_id):
        q_string = "SELECT port, name, info, state FROM public.services WHERE services.host_id = " + str(host_id)
        self.cursor.execute(q_string)
        port_list = self.cursor.fetchall()
        if port_list is None:
            port_list = []
        return port_list



if __name__ == '__main__':
    test_DB = DB_Model()
    test_DB.test_update_hosts(10)
    for host in test_DB.get_hosts():
        print(host.toString())
