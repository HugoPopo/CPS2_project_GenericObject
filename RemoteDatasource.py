from Datasource import Datasource

class RemoteDatasource(Datasource):
    
    def __init__(self, description):
        super().__init__(description)
        self.add_field(
            field_name="url_source",
            label="URL source",
            description="a URL providing a distant datasource",
            type="String"
        )
