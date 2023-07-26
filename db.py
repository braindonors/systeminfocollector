from flask_sqlalchemy import SQLAlchemy


sqldb = SQLAlchemy()
class database:
    

    class SystemInfo(sqldb.Model):
        id = sqldb.Column(sqldb.Integer, primary_key=True)
        machine_name = sqldb.Column(sqldb.String(50))
        operating_system = sqldb.Column(sqldb.String(50))
        version = sqldb.Column(sqldb.String(50))
        manufacturer = sqldb.Column(sqldb.String(50))
        model = sqldb.Column(sqldb.String(50))
        total_memory = sqldb.Column(sqldb.Float)
        
        disks = sqldb.Column(sqldb.Text)
        system_type = sqldb.Column(sqldb.String(100))
        hostname = sqldb.Column(sqldb.String(50))
        python_version = sqldb.Column(sqldb.String(50))
        processor_type = sqldb.Column(sqldb.String(100))
        processor_cores = sqldb.Column(sqldb.Integer)
        processor_threads = sqldb.Column(sqldb.Integer)
        network_adapters = sqldb.Column(sqldb.Text)
        dell_service_tag = sqldb.Column(sqldb.String(50))


    def initialize_sqldb(app):
        sqldb.init_app(app)
        with app.app_context():
            sqldb.create_all()


    