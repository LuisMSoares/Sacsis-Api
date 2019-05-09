import flask_excel as excel
from app import app

excel.init_excel(app)


class Excel:
    @staticmethod
    def report_by_array(array_data, file_type="csv", file_name="export_data"):
        return excel.make_response_from_array(
            data,
            file_type,
            file_name=file_name
        )

    @staticmethod
    def report_from_records(dict_data, file_type="csv", file_name="export_data"):
        return excel.make_response_from_records(
            dict_data*2,
            file_type,
            file_name=file_name
        )