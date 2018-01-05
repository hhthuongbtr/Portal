from MySQL_Database import Database

class Event():
    def get_event_monitor_list(self):
        sql = """select evm.id, evm.pid, ev.name as event_name, ev.start_date, ev.end_date, en.name as encoder, svc.id as service_check_id, svc.name as service_check_name, en.ip_monitor, en.source_main, en.source_backup, evm.status, evm.last_update, evm.active
                from event_monitor as evm, event as ev, encoder as en, service_check as svc 
                where ev.active = 1 and evm.active = 1 and en.active = 1 and svc.active = 1 and evm.event_id = ev.id and evm.encoder_id = en.id and evm.service_check_id = svc.id
                ORDER BY ev.start_date DESC"""
        db = Database()
        event_monitor_list = db.execute_query(sql)
        return event_monitor_list

    def get_running_event_monitor_list(self):
        sql = """select evm.id, evm.pid, ev.name as event_name, ev.start_date, ev.end_date, en.name as encoder, svc.id as service_check_id, svc.name as service_check_name, en.ip_monitor, en.source_main, en.source_backup, evm.status, evm.last_update, evm.active
                from event_monitor as evm, event as ev, encoder as en, service_check as svc 
                where ev.start_date < unix_timestamp(now()) and ev.end_date > unix_timestamp(now()) and ev.active = 1 and evm.active = 1 and en.active = 1 and svc.active = 1 and evm.event_id = ev.id and evm.encoder_id = en.id and evm.service_check_id = svc.id
                ORDER BY ev.start_date DESC"""
        db = Database()
        event_monitor_list = db.execute_query(sql)
        return event_monitor_list

    def get_waiting_event_monitor_list(self):
        sql = """select evm.id, evm.pid, ev.name as event_name, ev.start_date, ev.end_date, en.name as encoder, svc.id as service_check_id, svc.name as service_check_name, en.ip_monitor, en.source_main, en.source_backup, evm.status, evm.last_update, evm.active
                from event_monitor as evm, event as ev, encoder as en, service_check as svc 
                where ev.start_date > unix_timestamp(now()) and ev.end_date > unix_timestamp(now()) and ev.active = 1 and evm.active = 1 and en.active = 1 and svc.active = 1 and evm.event_id = ev.id and evm.encoder_id = en.id and evm.service_check_id = svc.id
                ORDER BY ev.start_date DESC"""
        db = Database()
        event_monitor_list = db.execute_query(sql)
        return event_monitor_list

    def get_completed_event_monitor_list(self):
        sql = """select evm.id, evm.pid, ev.name as event_name, from_unixtime(ev.start_date), from_unixtime(ev.end_date), en.name as encoder, svc.id as service_check_id, svc.name as service_check_name, en.ip_monitor, en.source_main, en.source_backup, evm.status, evm.last_update, evm.active
                from event_monitor as evm, event as ev, encoder as en, service_check as svc 
                where ev.start_date < unix_timestamp(now()) and ev.end_date < unix_timestamp(now()) and ev.active = 1 and evm.active = 1 and en.active = 1 and svc.active = 1 and evm.event_id = ev.id and evm.encoder_id = en.id and evm.service_check_id = svc.id
                ORDER BY ev.start_date DESC"""
        db = Database()
        event_monitor_list = db.execute_query(sql)
        return event_monitor_list

    def get_event_monitor(self, pk):
        sql = """select evm.id, evm.pid, ev.name as event_name, ev.start_date, ev.end_date, en.name as encoder, svc.id as service_check_id, svc.name as service_check_name, en.ip_monitor, en.source_main, en.source_backup, evm.status, evm.last_update, evm.active
                from event_monitor as evm, event as ev, encoder as en, service_check as svc 
                where evm.id = %d and ev.active = 1 and evm.active = 1 and en.active = 1 and svc.active = 1 and evm.event_id = ev.id and evm.encoder_id = en.id and evm.service_check_id = svc.id
                ORDER BY ev.start_date DESC"""%(int(pk))
        db = Database()
        event_monitor_list = db.execute_query(sql)
        return event_monitor_list
        